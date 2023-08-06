import collections
import configparser
import logging
import pathlib
import pprint
import shutil
from typing import Iterable, List

import gnupg
import toposort
import XCPF
import XCPF.PacmanConfig

from .package import (
    Package,
)
from .utils import (
    _PathType,
    read_makepkg_conf_var,
    run_cmd,
    try_rmtree,
)


logger = logging.getLogger(__name__)

pkgcache_cache = {}


def find_satisfiers_in_dbs(dbs, reqs):
    '''
    Search for packages that satisfy all of the given version requirements in the
    given databases.

    This functions borrows code from XCPF.find_satisfiers_in_dbs() but uses a
    cache for pkgcache as there are apparently memory leaks when generating
    pkgcache objects. To ensure correctness, pacman databases shouldn't be
    updated in between.
    '''
    for db in dbs:
        if db.name not in pkgcache_cache:
            pkgcache_cache[db.name] = db.pkgcache
        for pkg in XCPF.find_satisfiers_in_pkgs(pkgcache_cache[db.name], reqs):
            yield pkg


class PacmanConfigOptions:
    # See: PacmanConfig.load_from_options
    _attrs_ = (
        'root', 'dbpath', 'gpgdir', 'arch', 'logfile', 'cachedir', 'debug',
    )

    def __init__(self, **kwargs):
        for attr in self._attrs_:
            setattr(self, attr, kwargs.get(attr))


class PackageBuilder:
    GPG_SERVER = 'pool.sks-keyservers.net'

    def __init__(self, topdir, debug=False):
        self.topdir = topdir
        self.build_root = topdir / 'build'
        self.build_root.mkdir(exist_ok=True)
        self.aur_remote = topdir / 'aur-remote'
        self.aur_remote.mkdir(exist_ok=True)
        self.pkg_dict = {}
        self.dependency_links = {}

        self.debug = debug

        self.read_makepkg_conf()

        # makechrootpkg does not provide a simple way to use alternative
        # homedir for gpg, so imported keys go to user's dir
        self.gpg = gnupg.GPG()

        existing_keys = self.gpg.list_keys()

        self.existing_key_fingerprints = [
            key['fingerprint'] for key in existing_keys]

        self.built_packages = {}

    def read_makepkg_conf(self):
        VAR_NAMES = ('SRCDEST',)

        class MakepkgConf:
            def __repr__(self):
                return '\n'.join(
                    f'{key}={getattr(self, key)}' for key in VAR_NAMES)

        self.makepkg_conf = MakepkgConf()
        for var_name in VAR_NAMES:
            setattr(self.makepkg_conf, var_name,
                    read_makepkg_conf_var(var_name))
        logger.debug(f'makepkg.conf variables: {self.makepkg_conf}')

    def determine_build_order(self) -> Iterable[Package]:
        for group in toposort.toposort(self.dependency_links):
            for pkgbase in sorted(group):
                yield from self.pkg_dict[pkgbase].values()

    def build_package(self, pkg: Package):
        pkgbase = pkg.pkgbase
        current_pkgdir = pkg.pkgdir

        if pkg.is_vcs:
            to_delete = current_pkgdir / 'src'
            logger.debug(f'Cleaning {to_delete}')
            shutil.rmtree(to_delete)

        srcinfo = pkg.get_srcinfo()

        run_cmd(['sudo', 'pacman', '-Sy'])

        alpm_handle = self.get_alpm_handle(pkg.repo_name)
        all_pkgs_built = True
        for pkgname in srcinfo['packages'].keys():
            try:
                spec = f'{pkgname}>={pkg.get_version()}'
                logger.debug(f'Checking {spec}')
                found = next(find_satisfiers_in_dbs(alpm_handle.get_syncdbs(), [spec]))
                logger.debug(f'Found {found}')
            except StopIteration:
                all_pkgs_built = False
        if all_pkgs_built:
            logger.info(f'All packages for {pkgbase} found. Skipping.')
            return

        validpgpkeys = srcinfo.get('validpgpkeys', [])
        if validpgpkeys:
            logger.info(f'Necessary GPG keys {validpgpkeys}')
            to_import = set(validpgpkeys) - set(self.existing_key_fingerprints)
            logger.info(f'Keys to import: {to_import}')
            if to_import:
                import_result = self.gpg.recv_keys(
                    self.GPG_SERVER, *list(to_import))
                logger.info(import_result.summary())

        self.remove_chroot()

        makepkg_cmd = [
            'aur', 'build', '-d', pkg.repo_name, '-c', '-s', '-R',
            '-C', f'/usr/share/devtools/pacman-{pkg.repo_name}.conf']
        logger.debug(f'Running command: {makepkg_cmd!r}')
        run_cmd(
            makepkg_cmd, cwd=current_pkgdir, umask=0o022)

        self.remove_chroot()

    def prepare_package(self, topdir, pkgbase, repo_names: List[str]):
        pkgdir_candidate = topdir / pkgbase
        pkgbuild_source = None
        if pkgdir_candidate.exists():
            pkgbuild_source = pkgdir_candidate
        else:
            logger.info(f'Clone or update {pkgbase}...')

            run_cmd(['aur', 'fetch', pkgbase], cwd=self.aur_remote)
            pkgbuild_source = self.aur_remote / pkgbase

        ret = []
        (self.build_root / pkgbase).mkdir(exist_ok=True)
        for repo_name in repo_names:
            pkgdir = self.build_root / pkgbase / repo_name
            try_rmtree(pkgdir)
            shutil.copytree(pkgbuild_source, pkgdir)
            pkg = Package(pkgbase, pkgdir, repo_name)
            ret.append(pkg)
            self.pkg_dict.setdefault(pkgbase, collections.OrderedDict())[repo_name] = pkg
        return ret

    @staticmethod
    def get_alpm_handle(repo_name):
        pacman_conf = XCPF.PacmanConfig.PacmanConfig(
            conf=f'/usr/share/devtools/pacman-{repo_name}.conf')
        return pacman_conf.initialize_alpm()

    def check_dependencies(self, pkgs):
        new_pkg_specs = []
        repo_name = pkgs[0].repo_name
        alpm_handle = self.get_alpm_handle(repo_name)
        sync_dbs = [db for db in alpm_handle.get_syncdbs() if db.name != repo_name]
        for pkg in pkgs:
            deps = pkg.all_depends()
            ver_reqs = XCPF.collect_version_requirements(deps)
            logger.debug(f'Version requirements for {pkg.pkgbase}: {ver_reqs}')

            local_deps = []
            for dep in ver_reqs.keys():
                try:
                    # Is this package available in existing repos?
                    next(find_satisfiers_in_dbs(sync_dbs, [dep]))
                    logger.debug(f'{dep} is available in existing repos')
                except StopIteration:
                    local_deps.append(dep)
                    if self.pkg_dict.get(dep, {}).get(repo_name):
                        logger.debug(f'{(dep, repo_name)} already prepared, skipping')
                        continue
                    new_pkg_specs.append((dep, [repo_name]))
                    logger.debug(f'Need to build {dep} for {repo_name}')
            self.dependency_links[pkg.pkgbase] = set(local_deps)

        return new_pkg_specs

    def prepare_packages(self, filename, sections=None):
        pkgs = []
        config = configparser.ConfigParser()
        config.read(filename)
        pkg_spec_queue = []
        sections_to_process = sections or config.sections()
        for pkgbase in sections_to_process:
            pkg_info = config[pkgbase]
            pkg_spec_queue.append((pkgbase, pkg_info['repo'].split(',')))
        while pkg_spec_queue:
            pkgbase, repo_names = pkg_spec_queue.pop()
            new_pkgs = self.prepare_package(
                self.topdir, pkgbase, repo_names)
            pkgs.extend(new_pkgs)
            new_pkg_specs = self.check_dependencies(new_pkgs)
            pkg_spec_queue.extend(new_pkg_specs)
        logger.debug(f'Dependency links: {pprint.pformat(self.dependency_links)}')
        for pkg in pkgs:
            pkg.update()
        return pkgs

    def build_package_list(self, pkg_list: _PathType, sections=None, print_only=False, skip_dep_check=False):
        pkgs = self.prepare_packages(pkg_list, sections)

        if not skip_dep_check:
            build_order = list(self.determine_build_order())
        else:
            build_order = [pkg.pkgbase for pkg in pkgs]

        logger.info(f'Building packages: {pkgs}')
        logger.info(f'Build order: {pprint.pformat(build_order)}')

        if print_only:
            return

        for pkg in build_order:
            self.build_package(pkg)

    def remove_chroot(self):
        chroot_path = pathlib.Path('/var/lib/aurbuild')
        if not chroot_path.exists():
            return
        logger.info(f'Remove chroot {chroot_path}')
        run_cmd(['sudo', 'rm', '-r', chroot_path])

    def clean_sources(self):
        if not self.makepkg_conf.SRCDEST:
            return

        srcdest = pathlib.Path(self.makepkg_conf.SRCDEST)
        for f in srcdest.iterdir():
            if f.is_dir():
                continue
            f.unlink()

import json
import logging
import os
import subprocess

from srcinfo.parse import parse_srcinfo

from .utils import (
    PathFriendlyJSONEncoder,
    pushd,
    run_cmd,
)

from .lilaclib_wrapper import update_pkgrel

logger = logging.getLogger(__name__)


class Package:
    def __init__(self, pkgbase, pkgdir, repo_name):
        self.pkgbase = pkgbase
        self.pkgdir = pkgdir
        self.repo_name = repo_name

        self._is_vcs = pkgbase.split('-')[-1] in ('git', 'svn', 'hg', 'bzr')
        logger.debug(f'{pkgbase} is a VCS package? {self._is_vcs!r}')

    def __repr__(self):
        return json.dumps({
            'pkgbase': self.pkgbase,
            'pkgdir': self.pkgdir,
            'repo_name': self.repo_name,
        }, cls=PathFriendlyJSONEncoder)

    @property
    def is_vcs(self):
        return self._is_vcs

    def get_srcinfo(self):
        srcinfo_file = self.pkgdir / '.SRCINFO'
        if not srcinfo_file.exists():
            logger.debug(f'Retrieving srcinfo for the package in {self.pkgdir}')
            with open(srcinfo_file, 'wb') as f:
                subprocess.check_call(
                    ['makepkg', '--printsrcinfo'], cwd=self.pkgdir, stdout=f)

        with open(srcinfo_file, 'r') as f:
            srcinfo, error = parse_srcinfo(f.read())

        assert not error

        return srcinfo

    def bump_pkgrel(self, tag, times):
        if tag in self.repo_name:
            with pushd(self.pkgdir):
                for _ in range(times):
                    update_pkgrel()
            return True

        return False

    def update(self):
        updated = False

        if self.is_vcs:
            run_cmd([
                'makepkg', '--nobuild', '--nodeps'
            ], cwd=self.pkgdir)
            updated = True

        updated = self.bump_pkgrel('testing', 1) or updated
        updated = self.bump_pkgrel('unstable', 2) or updated
        updated = self.bump_pkgrel('staging', 3) or updated

        if updated:
            # Force regeneration of .SRCINFO
            try:
                os.unlink(self.pkgdir / '.SRCINFO')
            except FileNotFoundError:
                pass

    def all_depends(self):
        srcinfo = self.get_srcinfo()
        ret = srcinfo.get('depends', []) + srcinfo.get('makedepends', []) + srcinfo.get('checkdepends', [])
        for split_pkg_srcinfo in srcinfo.get('packages', {}).values():
            ret.extend(split_pkg_srcinfo.get('depends', []))
        return ret

    def get_version(self):
        srcinfo = self.get_srcinfo()
        epoch = srcinfo.get('epoch')
        pkgver = srcinfo['pkgver']
        pkgrel = srcinfo['pkgrel']
        if epoch:
            return f'{epoch}:{pkgver}-{pkgrel}'
        else:
            return f'{pkgver}-{pkgrel}'

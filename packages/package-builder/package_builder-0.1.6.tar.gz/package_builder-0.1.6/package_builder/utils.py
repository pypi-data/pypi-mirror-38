import contextlib
import json
import logging
import os
import shutil
import subprocess
import tarfile
from typing import Union, Text

logger = logging.getLogger(__name__)

_PathType = Union[bytes, Text, os.PathLike]


def read_makepkg_conf_var(var_name):
    return subprocess.check_output([
        'bash', '-c', f'source /etc/makepkg.conf && echo "${var_name}"'
    ]).decode('utf-8').strip()


def get_file_content_in_tarball(tarball_path, filename):
    with tarfile.open(tarball_path) as f:
        for info in f:
            if info.name == filename:
                target_file = f.extractfile(info)
                return target_file.read().decode('utf-8')


def run_cmd(cmd, *args, **kwargs):
    umask = kwargs.pop('umask', None)
    msg = f'Running command {cmd}'
    if kwargs.get('cwd'):
        msg += f' in {kwargs["cwd"]}'
    logger.debug(msg)
    try:
        if umask:
            oldmask = os.umask(umask)
        subprocess.check_call(cmd, *args, **kwargs)
    finally:
        if umask:
            os.umask(oldmask)


@contextlib.contextmanager
def pushd(directory):
    old_path = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(old_path)


def try_rmtree(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


class PathFriendlyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            path = os.fspath(o)
        except TypeError:
            pass
        else:
            return path
        # Let the base class default method raise the TypeError
        return super().default(self, o)

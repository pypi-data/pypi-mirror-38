import json
import logging
import pathlib
import subprocess
import time

logger = logging.getLogger(__name__)


def kbfs_mountdir():
    p = subprocess.check_output([
        'keybase', 'config', 'get', 'mountdir']).decode('utf-8').strip()
    logger.debug(f'kbfs mountpoint = {p}')
    assert p[0] == '"' and p[-1] == '"'
    return pathlib.Path(p[1:-1])


class KeybaseStorage:
    ARCH_REPO_PATH = 'arch-repo'

    def __init__(self, username):
        self.username = username

    @property
    def storage_root(self):
        return kbfs_mountdir() / f'public/{self.username}/{self.ARCH_REPO_PATH}'

    def child(self, name):
        return self.storage_root / name

    def flush(self):
        while True:
            with open(kbfs_mountdir() / f'public/{self.username}/.kbfs_status') as f:
                kbfs_status = json.load(f)
                if (not kbfs_status.get('DirtyPaths') and
                        not kbfs_status['Journal'].get('UnflushedPaths')):
                    break
                logger.debug(f'Wait for KBFS flush...')
                time.sleep(1)

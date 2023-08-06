# flake8: noqa: F402
import os.path
import sys

topdir = os.path.dirname(__file__)
third_party = os.path.join(topdir, 'third_party')
sys.path.extend([
    os.path.join(third_party, 'lilac'),
    os.path.join(third_party, 'lilac', 'vendor'),
])

from lilaclib import update_pkgrel

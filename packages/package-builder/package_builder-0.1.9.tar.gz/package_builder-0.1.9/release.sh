#!/bin/bash

set -e
set -x

ver=$1

[ -z "$ver" ] && exit 1

rm -rv build dist

git tag -s "$ver" -m "Version $ver"
python setup.py build sdist
gpg --detach-sign -a "dist/package_builder-$ver.tar.gz"
twine upload --sign dist/*

#!/bin/bash

ver=$1

git tag -s $ver -m "Version $ver"
python setup.py build sdist
gpg --detach-sign -a dist/package_builder-$ver.tar.gz
twine upload dist/*

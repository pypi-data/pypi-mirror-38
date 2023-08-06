#!/bin/bash

ver=$1

git tag -s $ver -m "Version $ver"
python setup.py build sdist
twine upload dist/*

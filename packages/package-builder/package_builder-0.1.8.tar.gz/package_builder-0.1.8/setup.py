# coding: utf-8

from setuptools import setup


setup(
    name='package_builder',
    description='Yet another Arch Linux package builder',
    url='https://gitlab.com/yan12125/package-builder',
    author='Chih-Hsuan Yen',
    author_email='yan12125@gmail.com',
    license='GPLv3',
    packages=[
        'package_builder',
        'package_builder.third_party.lilac',
        'package_builder.third_party.lilac.lilac2',
        'package_builder.third_party.lilac.vendor',
    ],

    setup_requires=['setuptools_scm'],
    use_scm_version=True,

    install_requires=[
        'python-gnupg',
        'srcinfo',
        'toposort',
        'XCPF',
        # dependencies of lilac, see https://github.com/archlinuxcn/lilac#python-%E5%BA%93
        'requests',
        'lxml',
        'PyYAML',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
)

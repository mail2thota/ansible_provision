#!/usr/bin/python
# -*- coding: UTF-8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description:setup tool for packaging

"""Setuptools package definition"""

from setuptools import setup
from setuptools import find_packages
import os
import codecs


__version__  = None
version_file = "foreman_client/version.py"
with codecs.open(version_file, encoding="UTF-8") as f:
    code = compile(f.read(), version_file, 'exec')
    exec(code)


def find_data(packages, extensions):
    """Finds data files along with source.

    :param   packages: Look in these packages
    :param extensions: Look for these extensions
    """
    data = {}
    for package in packages:
        package_path = package.replace('.', '/')
        for dirpath, _, filenames in os.walk(package_path):
            for filename in filenames:
                for extension in extensions:
                    if filename.endswith(".%s" % extension):
                        file_path = os.path.join(
                            dirpath,
                            filename
                        )
                        file_path = file_path[len(package) + 1:]
                        if package not in data:
                            data[package] = []
                        data[package].append(file_path)
    return data


with open('README.md', 'r') as f:
    README_TEXT = f.read()

setup(
    name = "fmclient",
    version = __version__,
    packages = find_packages(),
    package_data=find_data(
        find_packages(), ["py"]
    ),
    data_files=[('/etc/foreman_client/config',['config/system.yml','config/user_import.yml'])],
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'fmclient = foreman_client.main:main',
        ]
    },
    install_requires = [
        "pyyaml",
        "requests",
        "python-foreman"
    ],
    author='Heri Sutrisno',
    author_email='harry.sutrison@baesystems.com',
    description = "Foreman restfull client",
    long_description = README_TEXT,
    keywords = "foreman, yaml, api",
    url = "https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/foreman",
    classifiers = [
        "Development Status :: Production/Beta",
        "Environment :: Console",
        "Intended Audience :: Developers/technicall IT",
        "Intended Audience :: @BaeSystemsAI",
        "License :: Proprietary under @BaeSystemsAI",
        "Natural Language :: English",
        "Operating System :: CentOS7",
        "Programming Language :: Python :: 2.7.5",
        "Topic :: System :: restfull foreman client",
    ],

)

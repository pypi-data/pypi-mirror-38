#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
the setup file of the project
"""

from setuptools import setup, find_packages
import sys
import os

ETC_PATH = "/usr/local/etc/irobot/"

setup(
    name="irobot",
    version="1.0.2",
    author="nobody",
    author_email="2273337844@qq.com",
    description="The irobot project",
    license="Apache",
    keywords="irobot robot",
    url="https://pypi.python.org/pypi/irobot",
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        (ETC_PATH, ['etc/irobot.conf', 'etc/logger.conf'])
    ],
    scripts=["scripts/daemon_irobot"],
    install_requires=[
        "flask",
        "xlrd",
        "pycparser",
        "flask_socketio",
        "configparser",
        "daemonpy3",
        "jieba",
        "pymysql"
    ],
    zip_safe=False,
    platforms=["Linux", "Unix"],
    classifiers = [
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        "console_scripts":[
            "irobot_start = irobot.app:serve_forever"
        ]
    }
)


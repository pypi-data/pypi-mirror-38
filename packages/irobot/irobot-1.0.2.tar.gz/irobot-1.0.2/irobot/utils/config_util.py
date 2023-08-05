#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
Util for parse *.conf file into <key, value> data structure
"""
import configparser
import os


def parse(filepath, section):
    if not os.path.isfile(filepath):
        raise Exception("file '%s' not exist" % filepath)
    parser = configparser.ConfigParser()
    parser.read(filepath)
    lists = parser.items(section)
    config = {}
    for ll in lists:
        if len(ll) != 2:
            raise Exception('the configuration of %s is illegal : %s' % (filepath, str(ll)))
        config[ll[0]] = ll[1]
    return config

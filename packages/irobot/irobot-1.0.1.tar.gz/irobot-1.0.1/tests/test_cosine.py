#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
The testcase of cosine.py
"""

import unittest
from irobot.core.cosine import Cosine

samples = [
"我很好",
"今天天气不错",
"我是谁",
"你是谁"
]
cosine = None

class TestCosine(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        global cosine
        cosine = Cosine(samples)

    def test_exist(self):
        text = "我是谁"
        result = cosine.get_similarity(text)
        assert result[0] == 2

    def test_similar1(self):
        text = "天气很好"
        result = cosine.get_similarity(text)
        assert result[0] == 0

    def test_similar2(self):
        text = "天气不错"
        result = cosine.get_similarity(text)
        assert result[0] == 1

    def test_not_exist(self):
        text = "快乐大本营"
        result = cosine.get_similarity(text)
        assert result is None

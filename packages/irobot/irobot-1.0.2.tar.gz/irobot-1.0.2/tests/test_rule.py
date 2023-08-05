#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
The test cases of Rule.py
"""

from irobot.core.rule import Rule
import unittest
import logging

rule = None

class TestRule(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global rule
        logger = logging.getLogger()
        logger.setLevel("DEBUG")
        rule = Rule("/usr/local/etc/irobot/xgamerule.txt", logger)

    @classmethod
    def tearDownClass(self):
        pass

    def test_exist(self):
        result = rule.get_standard_sentence("叫名")
        assert result is not None
        result = rule.get_standard_sentence("你叫做什么名字啊")
        assert result is not None

    def test_not_exist(self):
        result = rule.get_standard_sentence("你TM叫啥")
        assert result is None
        result = rule.get_standard_sentence("你叫做什么名字呢")
        assert result is None

if __name__== "__main__":
    unittest.main()

#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
The testcase of qa.py
"""

from irobot.core.qa import QA
import unittest

qa = None
answers_list = [
["my name is lafite", "call me lafite"],
["good day", "good whether"],
["interesting"]
]

class TestQA(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global qa
        qa = QA(answers_list)

    def test1(self):
        answer = qa.get_answer(0)
        assert answer in answers_list[0]

    def test2(self):
        answer = qa.get_answer(1)
        assert answer in answers_list[1]

    def test3(self):
        answer = qa.get_answer(2)
        assert answer == answers_list[2][0]

    def test_not_exist(self):
        answer = qa.get_answer(3)
        assert answer is None

if __name__ == "__main__":
    unittest.main()

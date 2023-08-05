#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
Contain the answer of all question
Constructor:
    QA(answers_list)
Interface:
    load(answers_list)
    get_answer(index)
"""

import random

class QA(object):
    """
    Contain the answer of all question
    """
    def __init__(self, answers_list):
        self.load(answers_list)

    def load(self, answers_list):
        self.answers_list = answers_list

    def get_answer(self, index):
        answers_list = self.answers_list
        if len(answers_list) <= index:
            return None
        answers = answers_list[index]
        if answers:
            return random.sample(answers, 1)[0]


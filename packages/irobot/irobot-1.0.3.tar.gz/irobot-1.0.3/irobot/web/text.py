#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
Web service of text interaction
"""
from traceback import format_exc
from irobot.web.response import *
from flask import Blueprint, request

class TextService(Blueprint):
    def __init__(self, logger, consine, rule, qa):
        super(TextService, self).__init__("text_service", __name__)
        self.logger = logger
        self.rule = rule
        self.consine = consine
        self.qa = qa

    def register_router(self):
        @self.route("/text", methods=["POST"])
        def answer():
            question = request.form.get("question")
            if question is None or question == "":
                return ErrorResponse(CODE_ILLEGAL_PARAMS, "illegal parameters").to_json()
            try:
                standard_question = self.rule.get_standard_sentence(question)
                if standard_question is None:
                    standard_question = question
                    self.logger.debug("no such kind of question (%s)" % question)
                ret = self.consine.get_similarity(standard_question)
                if ret is None:
                    self.logger.debug("no similar answer for the question (%s)" % question)
                    return ErrorResponse(CODE_NO_RESULT, "找不到答案哦，亲").to_json()
                answer = self.qa.get_answer(ret[0])
                if answer is None:
                    return ErrorResponse(CODE_SYS_ERROR, "系统异常，稍后再试").to_json()
                return SuccessResponse(answer).to_json()
            except Exception as e:
                self.logger.error("answer the question fail, question = %s\n%s" % (question, format_exc()))
                return ErrorResponse(CODE_SYS_ERROR, "系统异常，稍后再试")


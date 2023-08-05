#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
Response for web request
"""

CODE_SUCCESS = "SUCCESS"
CODE_SYS_ERROR = "SYS_ERROR"
CODE_ILLEGAL_PARAMS = "ILLEGAL_PARAMETERS"
CODE_NO_RESULT = "NO_RESULT"

class Response(object):
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data

    def to_json(self):
        return '{"code":"%s", "message":"%s", "data":"%s"' % (self.code, self.message, self.data)

class SuccessResponse(Response):
    def __init__(self, data):
        super(SuccessResponse, self).__init__(CODE_SUCCESS, None, data)

class ErrorResponse(Response):
    def __init__(self, code, message):
        super(ErrorResponse, self).__init__(code, message, None)

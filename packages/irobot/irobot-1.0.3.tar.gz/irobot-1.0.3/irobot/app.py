#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
Main process of the irobot
"""

import os
import logging
from flask import Flask
from flask_socketio import SocketIO
from traceback import format_exc
from logging import config
from irobot.utils import config_util
from irobot.utils import excel
from irobot.core.rule import Rule
from irobot.core.cosine import Cosine
from irobot.core.qa import QA
from irobot.web.text import TextService

ETC_PATH = '/usr/local/etc/irobot/'

def serve_forever(debug = False):
    # setup logger
    logger_config_path = os.path.join(ETC_PATH, "logger.conf")
    logging.config.fileConfig(logger_config_path)
    if debug:
        logger = logging.getLogger("debug")
    else:
        logger = logging.getLogger("release")
    # load settings
    config_path = os.path.join(ETC_PATH, "irobot.conf")
    if not os.path.isfile(config_path):
        logger.error("configuration file %s not exist" % config_path)
    try:
        config = config_util.parse(config_path, "irobot")
        rule_path = config["rule_path"]
        host = config["host"]
        port = int(config["port"])
        qa_path = config["qa_path"]
    except Exception as e:
        logger.error("config file '%s' error: %s" %(config_path, format_exc()))
        raise
    try:
        _start(logger, host, port, rule_path, qa_path)
    except Exception as e:
        logger.error("irobot start fail caused by %s" % format_exc())
        raise

def _start(logger, host, port, rule_path, qa_path):
    # init core services
    qa_reader = excel.Reader(qa_path)
    rows = qa_reader.readRaws()
    samples = list(map(lambda row : row[0], rows))
    answers_list = list(map(lambda row : row[1:], rows))
    rule = Rule(rule_path, logger)
    consine = Cosine(samples, logger)
    qa = QA(answers_list)
    # init web service
    app = Flask(__name__)
    text_service = TextService(logger, consine, rule, qa)
    text_service.register_router()
    app.register_blueprint(text_service)
    socketio = SocketIO(app)
    # start the web service
    socketio.run(app, host, port)


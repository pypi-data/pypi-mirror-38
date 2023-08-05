#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
Load the rule file and setup rule data structure
Constructor:
    Rule(path, logger)
Interface:
    get_standard_sentence(native_sentence)
    load()
"""
import re
from itertools import product
from irobot.core.SentenceFromRule import SentenceFromRule

reg = re.compile(r"s\(\?(\w)\)|\[(.*?)\]")
rule_dict = {
        "e": ["吃","喝"],
        "r": ["一"],
        "p": ["杯","瓶","顿"],
        "v": ["好喝","美味","级"],
        "d": ["咖啡", "茶","红酒","果汁","晚餐","午餐","早餐"],
        }

class Rule(object):
    """
    Load the rule file and setup rule data structure
    """

    def  __init__(self, path, logger):
        global rule_dict
        global reg
        self.path = path
        self.logger = logger
        self.mapper = {}
        try:
            self.load()
        except Exception as e:
            self.logger.exception("Rule.load fail, path = %s" % path)
            raise

    def get_standard_sentence(self, native_sentence):
        """
        Return standand sentence by the given native sentence
        Such as native_sentence = "I like you so much",
        returns "I love you"
        """
        return self.mapper.get(native_sentence)

    def load(self):
        """
        load or reload rule file
        """
        with open(self.path, "r", encoding='utf-8') as fd:
            mapper = {}
            for line in fd:
                # parse every line
                split = line.split("<-")
                if len(split) != 2:
                    continue
                # ignore illegal line
                standard_sentence = split[0].strip()
                reg_sentence = split[1].strip()
                # handle every line
                sentences = self._handle_reg_sentence(reg_sentence)
                if sentences is None:
                    self.logger.warn("Rule._handle_reg_sentence fail, reg_sentence = %s" % reg_sentence)
                    continue
                for sentence in sentences:
                    # setup mapper {native_sentence : standard_sentence, ...}
                    mapper[sentence] = standard_sentence
            # reset mapper safely
            self.mapper = mapper

    def _handle_reg_sentence(self, reg_sentence):
        """
        Return native_sentences by the given reg_sentence
        Such as if reg_sentence = "[I|][love|like]you[so much]",
        returns ["I love you", "I like you", "love you so much", ...]
        """
        result = []
        words_list = []
        matches = reg.findall(reg_sentence)
        for words in matches:
            if len(words) == 2:
                _words = self._match_word(words[0], words[1])
                if _words is None:
                    self.logger.warn("Rule._match_word fail, words = %s" % str(words));
                    return
                words_list.append(_words)
        if len(words_list) > 0:
            combines = product(*words_list)
            for combine in combines:
                sentence_rule = SentenceFromRule()
                native_sentence = reg_sentence
                for idx in range(len(matches)):
                    word = combine[idx]
                    mat = matches[idx][0]
                    if mat:
                        sentence_rule.setSentence(mat, word)
                        native_sentence = native_sentence.replace("s(?%s)" % mat, sentence_rule.getSentence(mat), 1)
                    else:
                        native_sentence = re.sub(r"\[.*?\]", word, native_sentence, 1)
                result.append(native_sentence)
            return result

    def _match_word(self, word1, word2):
        # 如果第一个元素不为空，就添加第一个元素
        if word1:
            return rule_dict[word1]
        # 如果第二个元素不为空
        else:
            # 如果"|"在其中，表示任选一个
            if "|" in word2:
                return word2.split("|")
            # 如果没有"|"在其中，表示可有可无
            else:
                return [word2, ""]



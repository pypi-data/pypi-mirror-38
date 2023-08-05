#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
Calculating distance between input text and samples
Constructor:
    Cosine(samples, logger)
Interface:
    get_similarity(text)
"""
import math
import jieba
from itertools import chain

class Cosine(object):
    """
    Calculating distance between input text and samples
    """
    def __init__(self, samples, logger):
        self.word_dict = None
        self.rows = None
        self.count = None
        self.logger = logger
        try:
            self.load(samples)
        except Exception as e:
            self.logger.error("Cosine.load fail, samples.size = %s" % len(samples))
            raise

    def load(self, samples):
        rows = list(map(lambda item : list(jieba.cut(str(item), cut_all=True)), samples))
        dup_words = chain(*rows)
        word_set = set(dup_words)
        self.word_dict = dict((word, idx) for idx, word in enumerate(word_set))
        self.rows = rows
        self.count = len(self.word_dict)
        self.logger.info("Cosine.load success samples.size = %s, words.size = %s" % (len(samples), self.count))

    def get_similarity(self, text):
        all_words = self.word_dict.copy()
        counter = self.count
        input_words = set(jieba.cut(text, cut_all=True))
        for word in input_words:
            num = all_words.get(word)
            if num is None:
                all_words[word] = counter
                counter += 1
        # init result
        max_similar = 0
        max_index = 0
        # calc eigenvectors of input text
        indexs = map(lambda word : all_words[word], input_words)
        input_vector = [0] * len(all_words)
        for index in indexs:
            input_vector[index] += 1
        # TODO calc row_vectors in loading process, rather than calc in runtime
        for idx, row_words in enumerate(self.rows):
            # calc eigenvectors of each samples
            indexs = map(lambda word : all_words[word], row_words)
            row_vector = [0] * len(all_words)
            for index in indexs:
                row_vector[index] += 1
            # calc distace between input data and row data
            similar = self._calc_similar(input_vector, row_vector)
            # get min distance
            if max_similar < similar:
                max_similar = similar
                max_index = idx
        if max_similar == 0:
            self.logger.info("no similar sample, input = %s" % text)
            return None
        return (max_index, max_similar)

    def _calc_similar(self, vector1, vector2):
        if len(vector1) != len(vector2):
            self.logger.error("different length vector1 = %s vector2 = %s" % (vector1, vector2))
            return 0
        sum = 0
        sq1 = 0
        sq2 = 0
        for i in range(len(vector1)):
            sum += vector1[i] * vector2[i]
            sq1 += vector1[i] ** 2
            sq2 += vector2[i] ** 2
        denominator = math.sqrt(sq1) * math.sqrt(sq2)
        if denominator == 0:
            return 0
        return sum / denominator



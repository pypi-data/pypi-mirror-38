#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 lafite <2273337844@qq.com>
# Distributed under terms of the MIT license.

"""
Read from excel file or write into excel file
"""
import xlrd

class Reader(object):
    """
    Reader from excel file
    """
    def __init__(self, filepath):
        self.filepath = filepath

    def readRaws(self):
        rows = []
        exl = xlrd.open_workbook(self.filepath)
        if not exl.sheets():
            return
        table = exl.sheets()[0]
        for i in range(table.nrows):
            row = table.row_values(i)
            cols = list(filter(None, row))
            if len(cols) > 0:
                rows.append(cols)
        return rows

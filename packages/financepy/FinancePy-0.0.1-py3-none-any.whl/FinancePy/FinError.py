# -*- coding: utf-8 -*-
"""
Created on Sun Feb 07 20:49:10 2016

@author: Dominic
"""


class FinError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

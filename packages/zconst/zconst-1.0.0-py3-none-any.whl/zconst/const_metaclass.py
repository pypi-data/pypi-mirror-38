# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zconst_metaclass.py
   Author :       Zhang Fan
   date：         18/11/08
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from zconst import ConstError


class const(type):
    def setattr(self, key, value):
        raise ConstError("Can't Chang const.%s" % key)

    def __new__(metacls, cls, bases, classdict):
        classdict['__setattr__'] = const.setattr
        return super().__new__(metacls, cls, bases, classdict)()

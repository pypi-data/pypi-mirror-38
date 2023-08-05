# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    const_decorator.py
   Author :       Zhang Fan
   date：         18/11/08
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from zconst import ConstError


def const(cls):
    def setattr(self, key, value):
        raise ConstError("Can't Chang const.%s" % key)

    cls.__setattr__ = setattr

    return cls()

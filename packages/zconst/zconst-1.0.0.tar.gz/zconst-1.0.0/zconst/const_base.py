# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    const_base.py
   Author :       Zhang Fan
   date：         18/11/08
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from zconst import ConstError


class const():
    def __setattr__(self, key, value):
        raise ConstError("Can't Chang const.%s" % key)

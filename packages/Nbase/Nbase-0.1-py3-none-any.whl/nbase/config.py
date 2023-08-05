#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/6 下午10:41

from helpers import get_root_path


class Config(dict):
    """
    Nbase config
    """
    def __init__(self, root_path=None, defaults=None):
        dict.__init__(self, defaults or {})
        if root_path is None:
            root_path = get_root_path()
        self.root_path = root_path



    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))

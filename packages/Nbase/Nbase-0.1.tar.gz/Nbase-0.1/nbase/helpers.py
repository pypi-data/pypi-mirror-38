#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/6 下午11:20

import os
import sys


def get_root_path():
    """
    Returns the path to a package
    :return:
    """
    # Module already imported and has a file attribute.  Use that first.
    mod = sys.modules.get(__name__)
    if mod is not None and hasattr(mod, '__file__'):
        return os.path.dirname(os.path.abspath(mod.__file__))

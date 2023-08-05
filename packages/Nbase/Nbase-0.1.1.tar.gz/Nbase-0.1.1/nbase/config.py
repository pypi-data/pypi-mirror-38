#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/6 下午10:41

from flask.helpers import get_root_path
from flask.config import Config

root_path = get_root_path(__name__)
config = Config(root_path)

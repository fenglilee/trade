# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: __init__.py
@time: 2019/11/8 5:00 下午
"""

import os
from yaml import SafeLoader
from yaml import load

config_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.yml'))
with open(config_yml, 'r') as f:
    Configs = load(f.read(), Loader=SafeLoader)

DATE_FORMAT = Configs.get('DATE_FORMAT', None)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

if __name__ == '__main__':
    pass

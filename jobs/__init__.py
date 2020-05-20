# -*- coding: utf-8 -*-

"""
@author: fengli
@file: __init__.py.py
@time: 2017/6/14 下午7:59
"""

import tushare as ts
from config import Configs
from flask_apscheduler import APScheduler

ts.set_token(Configs.get('TUASHARE_TOKEN', None))

scheduler = APScheduler()

if __name__ == '__main__':
    pass

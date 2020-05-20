# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: __init__.py
@time: 2019/11/8 5:19 下午
"""

import os
import yaml
import sys
import logging
from config import ROOT_DIR
from logging.config import dictConfig

log_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), 'log.yml'))

logs_directory = os.path.join(ROOT_DIR, 'logs')
if not os.path.exists(logs_directory):
    os.mkdir(logs_directory)

try:
    with open(log_yml, 'r') as f:
        Configs = yaml.load(f.read())
except FileNotFoundError as e:
    print("config file %s does not exist" % (log_yml,))
    sys.exit()

logging.config.dictConfig(Configs)

debug_logger = logging.getLogger('debug_logger')
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')


def debug_log(msg, *args, **kwargs):
    debug_logger.debug(msg, *args, **kwargs)


def info_log(msg, *args, **kwargs):
    info_logger.info(msg, *args, **kwargs)


def error_log(msg, *args, **kwargs):
    error_logger.error(msg, *args, **kwargs)


if __name__ == '__main__':
    pass

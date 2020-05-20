# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: __init__.py
@time: 2019/11/8 5:56 下午
"""

from flask_restplus import Api

api = Api(
    title='Stock Trade',
    version='1.0',
    description='doc for this project',
    doc='/api/doc'
)


if __name__ == '__main__':
    pass

# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: app.py
@time: 2019/11/8 5:24 下午
"""

from gevent import monkey
monkey.patch_all()

from flask import Flask
from config import Configs
from database import db
from apps import api
from jobs import scheduler
from jobs.big_deal import get_big_deal
from jobs.stock_basic import get_stock_basic
from jobs.week_data import load_week_data

app = Flask(__name__)
app.config.update(
    SECRET_KEY=Configs.get('SECRET_KEY', None),
    HOST_SECRET_KEY=Configs.get('HOST_SECRET_KEY', None),
    SESSION_COOKIE_HTTPONLY=Configs.get('SESSION_COOKIE_HTTPONLY', False),
    PERMANENT_SESSION_LIFETIME=Configs.get('PERMANENT_SESSION_LIFETIME', 300),
    SESSION_REFRESH_EACH_REQUEST=Configs.get('SESSION_REFRESH_EACH_REQUEST', False),
    SQLALCHEMY_DATABASE_URI=Configs.get('SQLALCHEMY_DATABASE_URI', None),
    SQLALCHEMY_TRACK_MODIFICATIONS=Configs.get('SQLALCHEMY_TRACK_MODIFICATIONS', False),
    SQLALCHEMY_POOL_SIZE=Configs.get('SQLALCHEMY_POOL_SIZE', 5),
    SQLALCHEMY_POOL_RECYCLE=Configs.get('SQLALCHEMY_POOL_RECYCLE', 300)
)

api.init_app(app)
db.init_app(app)

scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    app.run()

# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: manage.py
@time: 2019/11/10 2:28 下午
"""

from app import app
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from database.stock_basic import StockBasic
from database.big_deal import BigDeal
from database.week_data import WeekModel
from database import db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

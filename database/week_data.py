# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: week_data.py
@time: 2019/11/11 8:25 下午
"""


from database import db
from database import AttrModel
from database import MethodModel


class WeekModel(AttrModel, MethodModel):

    __tablename__ = 'week_data'

    ts_code = db.Column(db.String(32), index=True, nullable=False, comment='股票代码')
    close = db.Column(db.Float, nullable=False, comment='收盘价')
    date = db.Column(db.Date, index=True, nullable=False, comment='交易日')


if __name__ == '__main__':
    pass

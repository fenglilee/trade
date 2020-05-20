# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: big_deal.py
@time: 2019/11/10 4:56 下午
"""

from database import db
from database import AttrModel
from database import MethodModel


class BigDeal(AttrModel, MethodModel):

    __tablename__ = 'big_deal'

    ts_code = db.Column(db.String(32), index=True, nullable=False, comment='股票代码')
    price = db.Column(db.Float, nullable=False, comment='交易价格')
    volume = db.Column(db.Integer, nullable=False, comment='交易量')
    trade_type = db.Column(db.String(32), index=True, nullable=False, comment='交易类型')
    date = db.Column(db.Date, index=True, nullable=False, comment='交易日')


if __name__ == '__main__':
    pass

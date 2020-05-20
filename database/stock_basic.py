# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: stockbasic.py
@time: 2019/11/10 2:21 下午
"""

from database import db
from database import AttrModel
from database import MethodModel


class StockBasic(AttrModel, MethodModel):

    __tablename__ = 'stock_basic'

    ts_code = db.Column(db.String(32), index=True, nullable=False, comment='股票代码')
    name = db.Column(db.String(32), nullable=False, comment='股票名称')
    area = db.Column(db.String(32), nullable=False, comment='交易市场')
    industry = db.Column(db.String(32), nullable=False, comment='所属行业')



if __name__ == '__main__':
    pass

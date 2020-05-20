# -*- coding: utf-8 -*-

"""
@author: fengli
@file: models.py
@time: 2017/6/14 下午8:00
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from mongoengine import *
from mongoengine.fields import *
from datetime import datetime
from global_config import Database_Config
from mongoengine import connect
from mongoengine import connection

connection.disconnect()
connect(**Database_Config)


class User(DynamicDocument):

    username = StringField(required=True, max_length=256)
    email = EmailField(required=True, max_length=256)
    password = StringField(required=True, max_length=256)
    phone = StringField(max_length=256)
    occupation = StringField(max_length=256)
    address = StringField(max_length=256)

    @classmethod
    async def create(cls, **kwargs):
        return cls(**kwargs).save()


class TradingData(Document):

    name = StringField(required=True, max_length=256)
    code = StringField(required=True, max_length=256)
    date = DateTimeField(required=True, default=datetime.now)
    volume = IntField()
    nmc = FloatField()
    turnoverratio = FloatField()
    pb = FloatField()
    changepercent = FloatField()
    trade = FloatField()
    high = FloatField()
    amount = FloatField()
    low = FloatField()
    settlement = FloatField()
    open = FloatField()
    mktcap = FloatField()
    per = FloatField()

    def to_dict(self):
        return dict(
            name=self.name,
            code=self.code,
            date=self.date,
            volume=self.volume,
            nmc=self.nmc,
            turnoverratio=self.turnoverratio,
            pb=self.pb,
            changepercent=self.changepercent,
            trade=self.trade,
            high=self.high,
            amount=self.amount,
            low=self.low,
            settlement=self.settlement,
            open=self.open,
            mktcap=self.mktcap,
            per=self.per
        )


class DailyData(Document):

    code = StringField(required=True, max_length=256)
    date = DateTimeField(required=True, default=datetime.now)
    open = FloatField()
    high = FloatField()
    close = FloatField()
    low = FloatField()
    volume = IntField()
    price_change = FloatField()
    p_change = FloatField()
    ma5 = FloatField()
    ma10 = FloatField()
    ma20 = FloatField()
    v_ma5 = FloatField()
    v_ma10 = FloatField()
    v_ma20 = FloatField()
    turnover = FloatField()

    def to_dict(self):
        return dict(
            code=self.code,
            date=self.date,
            open=self.open,
            high=self.high,
            close=self.close,
            low=self.low,
            volume=self.volume,
            price_change=self.price_change,
            p_change=self.p_change,
            ma5=self.ma5,
            ma10=self.ma10,
            ma20=self.ma20,
            v_ma5=self.v_ma5,
            v_ma10=self.v_ma10,
            v_ma20=self.v_ma20,
            turnover=self.turnover
        )


if __name__ == '__main__':
    ss = User.objects.all()


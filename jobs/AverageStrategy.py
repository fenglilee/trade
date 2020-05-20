# -*- coding: utf-8 -*-

"""
@author: fengli
@file: AverageStrategy.py
@time: 2017/7/22 下午7:40
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from db.mongodb import Mongodb
import pymongo
from pandas import DataFrame
from pandas import Series
import pandas as pd
import tushare as ts
import json
import pytz
from datetime import date
from datetime import datetime
from datetime import timedelta
from utils.log import log_setting
from apscheduler.schedulers.blocking import BlockingScheduler

pd.set_option('display.max_columns', 6)
pd.set_option('display.max_rows', 30)


class AverageStrategy(object):

    def __init__(self):
        self.client = Mongodb()
        self.db = self.client.conn()
        self.logger = log_setting('average_strategy')

    @staticmethod
    def analyze_week_close(data):
        result = {'success': False, 'message': None, 'flag': False}
        try:
            row, column = data.shape
            ma5_now = data['ma5'].ix[row - 1]
            ma10_now = data["ma10"].ix[row - 1]
            ma5_last = data['ma5'].ix[row - 2]
            ma10_last = data["ma10"].ix[row - 2]
            if ma5_now >= ma10_now and ma5_last <= ma10_last:
                result['flag'] = True
            else:
                result['flag'] = False
            result['success'] = True
        except Exception, e:
            result['message'] = e

        return result

    @staticmethod
    def analyze_week_volume(data):
        result = {'success': False, 'message': None, 'data': None}
        try:
            row, column = data.shape
            two_week = data["volume"].ix[row - 2: row].mean()
            four_week = data["volume"].ix[row - 6: row - 2].mean()
            ratio = two_week / four_week - 1
            # ratio = "%.2f%%" % (ratio * 100)
            result['success'] = True
            result['data'] = ratio
        except Exception, e:
            result['message'] = e
        return result

    def calculate_all_data(self):
        end = datetime.now(pytz.timezone('Asia/Shanghai'))
        start = end - timedelta(days=365)
        stock_set = self.db.trading_data.find()
        self.db.average_result.remove()
        out_list = list()
        for stock in stock_set:
            code = stock['code']
            del stock['date']
            del stock['_id']
            try:
                query = {'code': code, "date": {"$gte": start, "$lte": end}}
                data_set = self.db.week_data.find(query).sort([('date', 1)])
                week_data = {}
                for item in data_set:
                    date_time = item['date']
                    del item['date']
                    del item['_id']
                    week_data[date_time] = item
                week_data = DataFrame(week_data)
                week_data = week_data.T
                close_result = self.analyze_week_close(week_data)
                if close_result['success']:
                    if close_result['flag']:
                        volume_result = self.analyze_week_volume(week_data)
                        if volume_result['success']:
                            stock['rate'] = volume_result['data']
                            out_list.append(stock)
                            self.logger.info('{} has been successfully to selected at {}'.format(code, date.today()))
            except Exception, e:
                self.logger.error('{} has failed to select for {} at {}'.format(code, e, date.today()))

        self.db.average_result.insert(out_list)


if __name__ == '__main__':
    selector = AverageStrategy()
    # selector.calculate_all_data()
    scheduler = BlockingScheduler()
    scheduler.add_job(selector.calculate_all_data, 'cron', day_of_week='sat', hour='9', timezone=pytz.timezone('Asia/Shanghai'))
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

# -*- coding: utf-8 -*-

"""
@author: fengli
@file: WeekData.py
@time: 2017/7/21 下午8:43
"""

import sys
import os
import pytz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from db.mongodb import Mongodb
import tushare as ts
import json
from datetime import datetime
from datetime import date
from datetime import timedelta
from utils.log import log_setting
from pandas import DataFrame
from bson import ObjectId
from apscheduler.schedulers.blocking import BlockingScheduler


class WeekLoader(object):

    def __init__(self):
        self.client = Mongodb()
        self.db = self.client.conn()
        self.logger = log_setting('week_data')

    def insert_history_data(self, data, code):
        result_set = data.to_json(orient='records')
        result_set = json.loads(result_set)
        try:
            for row_record in result_set:
                row_record['date'] = datetime.strptime(row_record['date'], '%Y-%m-%d')
                old_record = self.db.week_data.find_one({'code': code, 'date': row_record['date']})
                if old_record:
                    continue
                ss = self.db.week_data.insert_one(row_record).inserted_id
        except Exception, e:
            self.logger.error('{} has failed to inserted for {} at {}'.format(code, e, date.today()))
        else:
            self.logger.info('{} has been successfully inserted at {}'.format(code, date.today()))

    def loading_history_data(self):
        end = date.today()
        start = end - timedelta(days=7)
        end_str = datetime.strftime(end, '%Y-%m-%d')
        start_str = datetime.strftime(start, '%Y-%m-%d')
        records = self.db.trading_data.find()
        for record in records:
            try:
                code = record['code']
                df = ts.get_k_data(code, start=start_str, end=end_str, ktype='W', autype='qfq')
                self.insert_history_data(df, code)
            except Exception, e:
                self.logger.error('{} has failed to inserted for {} at {}'.format(record['code'], e, date.today()))

    def calculate_moving_average(self):
        records = self.db.trading_data.find()
        for record in records:
            try:
                data_dic = dict()
                data_set = self.db.week_data.find({'code': record['code']}).sort([('date', 1)])
                for row in data_set:
                    row_id = row.pop('_id')
                    data_dic[row_id] = row
                df = DataFrame(data_dic).T
                df = df.reset_index()
                df['ma5'] = df['close'].rolling(window=5, center=False).mean()
                df['ma10'] = df['close'].rolling(window=10, center=False).mean()
                df['ma20'] = df['close'].rolling(window=20, center=False).mean()
                df['v_ma5'] = df['volume'].rolling(window=5, center=False).mean()
                df['v_ma10'] = df['volume'].rolling(window=10, center=False).mean()
                df['v_ma20'] = df['volume'].rolling(window=20, center=False).mean()
                self.update_week_data(df, record['code'])
            except Exception, e:
                self.logger.error('{} has failed to update for {} at {}'.format(record['code'], e, date.today()))

    def update_week_data(self, data, code):
        try:
            m, n = data.shape
            for i in range(m):
                row_record = data.ix[i]
                row_index = ObjectId(row_record['index'])
                content = {
                        'ma5': row_record['ma5'],
                        'ma10': row_record['ma10'],
                        'ma20': row_record['ma20'],
                        'v_ma5': row_record['v_ma5'],
                        'v_ma10': row_record['v_ma10'],
                        'v_ma20': row_record['v_ma20'],
                     }
                self.db.week_data.update_one({'_id': row_index}, {'$set': content})
        except Exception, e:
            self.logger.error('{} has failed to update for {} at {}'.format(code, e, date.today()))
        else:
            self.logger.info('{} has been successfully updated at {}'.format(code, date.today()))


if __name__ == '__main__':
    week_loader = WeekLoader()
    scheduler = BlockingScheduler()
    scheduler.add_job(week_loader.loading_history_data, 'cron', day_of_week='sat', hour='7', timezone=pytz.timezone('Asia/Shanghai'))
    scheduler.add_job(week_loader.calculate_moving_average, 'cron', day_of_week='sat', hour='8', timezone=pytz.timezone('Asia/Shanghai'))
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


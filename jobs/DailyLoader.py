# -*- coding: utf-8 -*-

"""
@author: fengli
@file: TradingLoader.py
@time: 2017/6/25 下午1:45
"""

import sys
import os
import json
import pytz
import logging
import tushare as ts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from datetime import datetime
from datetime import date
from datetime import timedelta
from bson import ObjectId
from pandas import DataFrame
from models.models import TradingData
from models.models import DailyData
from apscheduler.schedulers.blocking import BlockingScheduler


class DailyLoader(object):

    def __init__(self):
        self.logger = logging.getLogger('developer.logger')

    def load_daily_data(self):
        end = date.today()
        begin = end - timedelta(days=1)
        end_str = datetime.strftime(end, '%Y-%m-%d')
        begin_str = datetime.strftime(begin, '%Y-%m-%d')
        records = TradingData.objects.all()
        for record in records:
            code = record.code
            df = ts.get_k_data(code, start=begin_str, end=end_str, ktype='D', autype='qfq')
            self.insert_daily_data(df)

    @staticmethod
    def insert_daily_data(data):
        result_set = data.to_json(orient='records')
        result_set = json.loads(result_set)
        for row_record in result_set:
            row_record['date'] = datetime.strptime(row_record['date'], '%Y-%m-%d')
            old_record = DailyData.objects(code=row_record['code'], date=row_record['date']).first()
            if old_record:
                continue
            daily_data = DailyData(**row_record)
            daily_data.save()

    def calculate_moving_average(self):
        records = self.db.trading_data.find()
        for record in records:
            try:
                data_dic = dict()
                data_set = self.db.daily_data.find({'code': record['code']}).sort([('date', 1)])
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
                self.update_daily_data(df, record['code'])
            except Exception as e:
                self.logger.error('{} has failed to update for {} at {}'.format(record['code'], e, date.today()))

    def update_daily_data(self, data, code):
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
                self.db.daily_data.update_one({'_id': row_index}, {'$set': content})
        except Exception as e:
            self.logger.error('{} has failed to update for {} at {}'.format(code, e, date.today()))
        else:
            self.logger.info('{} has been successfully updated at {}'.format(code, date.today()))


if __name__ == '__main__':
    loader = DailyLoader()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(loader.load_daily_data, 'cron', day_of_week='tue-sat', hour='6', timezone=pytz.timezone('Asia/Shanghai'))
    # scheduler.add_job(loader.calculate_moving_average, 'cron', day_of_week='tue-sat', hour='7', timezone=pytz.timezone('Asia/Shanghai'))
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     pass
    loader.load_daily_data()


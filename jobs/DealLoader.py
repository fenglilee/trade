# -*- coding: utf-8 -*-

"""
@author: fengli
@file: BigDeal.py
@time: 2017/7/22 下午9:28
"""


import sys
import os
import json
import pytz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from db.mongodb import Mongodb
import pandas as pd
import tushare as ts
from datetime import datetime
from datetime import timedelta
from datetime import date
from utils.log import log_setting
from apscheduler.schedulers.blocking import BlockingScheduler

pd.set_option('display.max_columns', 6)
pd.set_option('display.max_rows', 30)


class BigDeal(object):

    def __init__(self):
        self.client = Mongodb()
        self.db = self.client.conn()
        self.logger = log_setting('deal_loader')

    def big_deal_loader(self, code, vol=400):
        today = date.today()
        today_str = datetime.strftime(today, '%Y-%m-%d')
        try:
            df = ts.get_sina_dd(code, date=today_str, vol=vol)
            assert df is not None
            result_set = df.to_json(orient='records')
            result_set = json.loads(result_set)
            for record in result_set:
                volume = record['volume']
                price = record['price']
                amount = volume * price
                if amount < 300000:
                    continue
                deal_time = record.pop('time')
                time_str = '{} {}'.format(today_str, deal_time)
                date_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                record['date'] = date_time
                self.db.deal_record.insert(record)
            self.logger.info('{} has been inserted successfully at {}'.format(code, today_str))
        except Exception, e:
            self.logger.error('{} has failed to insert beacuse of {} at {}'.format(code, e, today_str))

    def analyse_all_stock(self, vol=300):
        records = self.db.trading_data.find()
        for record in records:
            code = record['code']
            try:
                self.big_deal_loader(code, vol=vol)
            except Exception, e:
                self.logger.error('{} has failed to insert beacuse of {} at {}'.format(code, e, date.today()))


if __name__ == '__main__':
    big_deal = BigDeal()
    scheduler = BlockingScheduler()
    scheduler.add_job(big_deal.analyse_all_stock, 'cron', day_of_week='mon-fri', hour='21', minute='30', timezone=pytz.timezone('Asia/Shanghai'))
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

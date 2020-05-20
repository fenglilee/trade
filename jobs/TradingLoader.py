# -*- coding: utf-8 -*-

"""
@author: fengli
@file: TradingLoader.py
@time: 2017/6/25 下午1:45
"""

import os
import sys
import pytz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from db.mongodb import Mongodb
import tushare as ts
import json
from datetime import datetime
from utils.log import log_setting
from apscheduler.schedulers.blocking import BlockingScheduler


class TradingLoader(object):
    def __init__(self):
        self.client = Mongodb()
        self.db = self.client.conn()
        self.logger = log_setting('trading_loader')

    def load_trading_data(self):
        collection = self.db.trading_data
        data = ts.get_today_all()
        result = data.to_json(orient='records')
        result = json.loads(result)
        real_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        try:
            for row in result:
                row['date'] = real_time
                old_record = collection.find_one({'code': row['code']})
                if old_record:
                    collection.update_one({'code': row['code']}, {'$set': row})
                else:
                    row_id = collection.insert_one(row).inserted_id
            self.logger.info('trading data at {} has been successfully updated'.format(real_time))
        except Exception, e:
            self.logger.error(e)


if __name__ == '__main__':
    loader = TradingLoader()
    scheduler = BlockingScheduler()
    scheduler.add_job(loader.load_trading_data, 'cron', day_of_week='mon-fri', hour='9', minute='30,40,50', timezone=pytz.timezone('Asia/Shanghai'))
    scheduler.add_job(loader.load_trading_data, 'cron', day_of_week='mon-fri', hour='11', minute='00,10,20,30', timezone=pytz.timezone('Asia/Shanghai'))
    scheduler.add_job(loader.load_trading_data, 'cron', day_of_week='mon-fri', hour='15', timezone=pytz.timezone('Asia/Shanghai'))
    scheduler.add_job(loader.load_trading_data, 'cron', day_of_week='mon-fri', hour='10,13,14', minute='00,10,20,30,40,50', timezone=pytz.timezone('Asia/Shanghai'))
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


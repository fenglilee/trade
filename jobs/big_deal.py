# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: big_deal.py
@time: 2019/11/10 5:04 下午
"""

import time
import random
from jobs import scheduler
from jobs import ts
from datetime import datetime
from config import DATE_FORMAT
from database.stock_basic import StockBasic
from database.big_deal import BigDeal
from database import db
from logger import info_log
from logger import error_log


@scheduler.task('cron', id='jobs.big_deal.get_big_deal', day_of_week='mon-fri', hour=16, minute=50)
def get_big_deal():
    try:
        with scheduler.app.app_context():
            stock_set = StockBasic.find_all()
            now = datetime.now()
            for stock in stock_set:
                ts_code = stock.ts_code
                code, _ = ts_code.split('.')
                try:
                    data = ts.get_sina_dd(code, date=datetime.strftime(now, DATE_FORMAT))
                except Exception as e:
                    data = None

                if data is None:
                    continue

                try:
                    data = data.dropna(axis=0, how='any')
                    data = data.loc[:, ['price', 'volume', 'type']]
                    records = data.to_dict(orient='records')
                    for record in records:
                        BigDeal.create(
                            commit=False,
                            ts_code=ts_code,
                            date=now.date(),
                            price=record['price'],
                            volume=record['volume'],
                            trade_type=record['type']
                        )
                    else:
                        db.session.commit()
                        info_log('get %s trade data succeed' % (ts_code,))
                except Exception as e:
                    error_log('get %s trade data failed: %s' % (ts_code, repr(e)), exc_info=True)

                random_int = random.randint(1, 10)
                time.sleep(random_int)

    except Exception as e:
        error_log(repr(e), exc_info=True)


if __name__ == '__main__':
    pass

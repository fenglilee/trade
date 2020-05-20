# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: week_data.py
@time: 2019/11/11 8:18 下午
"""


from jobs import ts
from datetime import datetime
from datetime import timedelta
from database import db
from database.stock_basic import StockBasic
from database.week_data import WeekModel
from logger import error_log
from jobs import scheduler

_DateFormat = '%Y%m%d'


@scheduler.task('cron', id='jobs.week_data.load_week_data', day_of_week='sun', hour=16)
def load_week_data(frq='w', adj='qfq'):
    try:
        with scheduler.app.app_context():
            stock_set = StockBasic.find_all()
            for stock in stock_set:
                end = datetime.now()
                start = end - timedelta(days=7)
                try:
                    data = ts.pro_bar(
                        ts_code=stock.ts_code,
                        freq=frq,
                        adj=adj,
                        start_date=datetime.strftime(start, _DateFormat),
                        end_date=datetime.strftime(end, _DateFormat)
                    )
                except Exception as e:
                    data = None

                if data is None:
                    continue

                try:
                    data = data.dropna(axis=0, how='any')
                    data = data.loc[:, ['ts_code', 'trade_date', 'pre_close']]
                    records = data.to_dict(orient='records')
                    for record in records:
                        record['trade_date'] = datetime.strptime(record['trade_date'], _DateFormat).date()
                        ins = WeekModel.find_one(ts_code=record['ts_code'], date=record['trade_date'])
                        if ins is None:
                            WeekModel.create(
                                commit=False,
                                date=record['trade_date'],
                                ts_code=record['ts_code'],
                                close=record['pre_close']
                            )
                        else:
                            ins.update(
                                commit=False,
                                date=record['trade_date'],
                                ts_code=record['ts_code'],
                                close=record['pre_close']
                            )
                    else:
                        db.session.commit()

                except Exception as e:
                    error_log(repr(e), exc_info=True)

    except Exception as e:
        error_log(repr(e), exc_info=True)


if __name__ == '__main__':
    pass

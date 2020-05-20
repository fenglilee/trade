# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: stock_basic.py
@time: 2019/11/10 2:44 下午
"""

from jobs import scheduler
from jobs import ts
from database import db
from database.stock_basic import StockBasic
from logger import info_log
from logger import error_log


@scheduler.task('cron', id='jobs.stock_basic.get_stock_basic', day_of_week='fri', hour=18)
def get_stock_basic(list_status='L', fields='ts_code,name,area,industry'):
    try:
        with scheduler.app.app_context():
            pro = ts.pro_api()
            try:
                data = pro.stock_basic(list_status=list_status, fields=fields)
            except Exception as e:
                data = None

            if data is None:
                return

            data = data.dropna(axis=0, how='any')
            records = data.to_dict(orient='records')
            for record in records:
                ins = StockBasic.find_one(ts_code=record['ts_code'])
                if ins is None:
                    StockBasic.create(commit=False, **record)
                else:
                    ins.update(commit=False, **record)
            else:
                db.session.commit()
                info_log('update stock basic succeed')
    except Exception as e:
        error_log('update stock basic failed: %s' % (repr(e),), exc_info=True)


if __name__ == '__main__':
    pass


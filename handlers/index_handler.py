# -*- coding: utf-8 -*-

"""
@author: fengli
@file: IndexHandler.py
@time: 2017/6/14 下午2:43
"""

import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from handlers.base_handler import BaseHandler
from models.models import TradingData
from global_config import DATE_FORMAT
from datetime import datetime
from handlers.base_handler import auth_check


class IndexHandler(BaseHandler):

    @auth_check
    async def get(self, *args, **kwargs):
        self.render("index.html", title=u'Today\'s Quotes', user=u'fengli')

    @auth_check
    async def post(self, *args, **kwargs):
        result = {'success': False, 'data': None, 'reason': ''}
        try:
            daily_set = TradingData.objects.all()
            data_set = list(map(
                lambda item: {
                    'name': item.name,
                    'code': item.code,
                    'date': datetime.strftime(item.date, DATE_FORMAT),
                    'trade': item.trade,
                    'changepercent': '{}%'.format('%.2f' % item.changepercent),
                    'volume': item.volume
                }, daily_set))
            result['success'] = True
            result['data'] = data_set

        except Exception as e:
            result['reason'] = e

        self.write(json.dumps(result))


if __name__ == '__main__':
    pass
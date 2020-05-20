# -*- coding: utf-8 -*-

"""
@author: fengli
@file: IndexHandler.py
@time: 2017/6/14 下午2:43
"""

import json
from datetime import datetime
from models.models import TradingData
from models.models import DailyData
from global_config import DATE_FORMAT
from handlers.base_handler import BaseHandler
from handlers.base_handler import auth_check


class DetailHandler(BaseHandler):

    @auth_check
    async def get(self):
        code = self.get_argument("code", None)
        daily_set = TradingData.objects(code=code).order_by('-date')
        daily_data = daily_set.first()
        if daily_data is None:
            self.render("500.html")
            return
        daily_data.changepercent = '{}%'.format('%.2f' % daily_data.changepercent)
        daily_data.turnoverratio = '{}%'.format('%.2f' % daily_data.turnoverratio)
        self.render("detail.html", title=u"Detail", user=u'fengli', data=daily_data)

    @auth_check
    async def post(self):
        result = {'success': False, 'data': None, 'reason': ''}
        try:
            req_txt = self.request.body
            req_json = json.loads(req_txt)
        except Exception as e:
            result["reason"] = "Invalidate request body {}".format(e)
            self.write(json.dumps(result))
            return
        try:
            date_str = req_json['date']
            date_query = datetime.strptime(date_str, DATE_FORMAT)
            daily_set = DailyData.objects(date=date_query)
            data_set = list(map(
                lambda item: {
                    'name': item.name,
                    'code': item.code,
                    'date': datetime.strftime(item.date, '%Y-%m-%d %H:%M:%S')[:11],
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
# -*- coding: utf-8 -*-

"""
@author: fengli
@file: LoginHandler.py
@time: 2017/6/14 下午5:39
"""

import ujson as json
from models.models import User
from handlers.base_handler import BaseHandler


class LogoutHandler(BaseHandler):

    async def post(self, *args, **kwargs):
        result = {'success': False, 'reason': None, 'data': None}

        self.clear_cookie("session_id")
        self.clear_cookie("hmac_key")

        result['success'] = True
        self.write(json.dumps(result))
        self.finish()


class LoginHandler(BaseHandler):

    async def get(self, *args, **kwargs):
        next_url = self.get_argument('next', None)
        if next_url is None:
            next_url = "/index"

        self.render('login.html',
                    title="登录",
                    user=None,
                    next_url=next_url
                    )
        self.finish()

    async def post(self, *args, **kwargs):
        result = {'success': False, 'reason': None, 'data': None}
        req_data = json.loads(self.request.body)
        user_name = req_data['user_name']
        password = req_data['password']
        next_url = req_data['next_url']

        user = User.objects(username=user_name).first()
        if not user:
            result['reason'] = 'username %s is not existed' % (user_name,)
            self.write(json.dumps(result))
            self.finish()

        password = self._md5(password)
        if password != user.password:
            result['reason'] = 'password is not correct'
            self.write(json.dumps(result))
            self.finish()

        self._session['user_name'] = user_name
        self._session.save()
        result['success'] = True
        result['data'] = {'next': next_url}
        self.write(json.dumps(result))
        self.finish()


if __name__ == '__main__':
    pass


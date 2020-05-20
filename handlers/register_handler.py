# -*- coding: utf-8 -*-

"""
@author: fengli
@file: RegisterHandler.py
@time: 2017/6/14 下午6:17
"""

import json
from models.models import User
from handlers.base_handler import BaseHandler


class RegisterHandler(BaseHandler):

    async def get(self):
        self.render('register.html', title='用户注册', user=None)

    async def post(self):
        result = {'success': False, 'reason': None, 'data': None}
        req_json = json.loads(self.request.body)
        username = req_json['user_name']
        email = req_json['email']
        password = req_json['password']
        phone = req_json['phone']
        occupation = req_json['occupation']
        address = req_json['address']

        same_name_user = User.objects(username=username).first()
        if same_name_user is not None:
            result['reason'] = 'Username %s has already been existed' % (username,)
            self.write(json.dumps(result))
            self.finish()

        same_email_user = User.objects(email=email).first()
        if same_email_user is not None:
            result['reason'] = 'Email addr %s has already been registered' % (email,)
            self.write(json.dumps(result))
            self.finish()

        password = self._md5(password)
        _ = await User.create(
            username=username,
            email=email,
            password=password,
            phone=phone,
            occupation=occupation,
            address=address
        )
        result['success'] = True
        self.write(json.dumps(result))
        self.finish()


if __name__ == '__main__':
    pass


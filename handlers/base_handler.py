# -*- coding: utf-8 -*-

"""
@author: fengli
@file: BaseHandler.py
@time: 2017/6/14 下午2:45
"""

import hashlib
import logging
from tornado.web import RequestHandler
from session.session import Session
from functools import wraps
from urllib.parse import urlencode
from urllib.parse import urlsplit
from tornado.web import HTTPError


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session = Session(self.application.session_manager, self)
        self._logger = logging.getLogger('developer.logger')

    def get_current_user(self):
        return self._session.get("user_name")

    @staticmethod
    def _md5(string=None):
        md5_string = hashlib.md5(string.encode('utf-8'))
        return md5_string.hexdigest()


def auth_check(method):
    @wraps(method)
    def wrapper(handler, *args, **kwargs):
        if not handler.current_user:
            if handler.request.method in ("HEAD", "GET"):
                url = handler.get_login_url()
                if "?" not in url:
                    if urlsplit(url).scheme:
                        next_url = handler.request.full_url()
                    else:
                        next_url = handler.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                handler.redirect(url)
                return
            raise HTTPError(403)
        return method(handler, *args, **kwargs)
    return wrapper


if __name__ == '__main__':
    pass
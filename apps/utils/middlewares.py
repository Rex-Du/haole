"""
middlewares: 
"""

# Author     : rexdu
# FileName   : middlewares.py
# CreateDate : 2019-09-22 22:40
import logging
import time

from django.shortcuts import redirect, reverse
from django.utils.deprecation import MiddlewareMixin

from haole import settings

logger = logging.getLogger('default')


class UserLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if not user.is_authenticated and request.path != reverse('admin:login'):
            return redirect(to=reverse('admin:login') + "?next=/")


class ResponseTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.ctime = time.time()

    def process_response(self, request, response):
        if request.path != '/favicon.ico':
            logger.info(f'reponse time of {request.path}: {time.time() - request.ctime}')
        return response

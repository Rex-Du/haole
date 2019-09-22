"""
middlewares: 
"""


# Author     : rexdu
# FileName   : middlewares.py
# CreateDate : 2019-09-22 22:40
from django.shortcuts import redirect, reverse
from django.utils.deprecation import MiddlewareMixin

from haole import settings


class UserLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if not user.is_authenticated and request.path != reverse('admin:login'):

            return redirect(to='admin:login')

"""
authentication: 
"""
# Author     : rexdu
# FileName   : authentication.py
# CreateDate : 2019-09-22 22:18
from django.shortcuts import redirect
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from haole import settings


class UserLoginAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = request._request.user
        if user.is_authenticated:
            return user, None
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))




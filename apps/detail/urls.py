"""
urls: 
"""
# Author     : rexdu
# FileName   : urls.py
# CreateDate : 2019-09-21 23:06
from django.conf.urls import url

from .views import DetailView

urlpatterns = [
    url(r'detail/(?P<id>\d+)/$', DetailView.as_view(), name='detail'),
]

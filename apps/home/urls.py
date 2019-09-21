"""
urls: 
"""
# Author     : rexdu
# FileName   : urls.py
# CreateDate : 2019-09-21 22:00
from django.conf.urls import url
from django.urls import path, include

from .views import HomeView, CategoryView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    url(r'category/(?P<category>\w+)', CategoryView.as_view(), name='category'),
]


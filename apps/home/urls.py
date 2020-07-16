"""
urls: 
"""
# Author     : rexdu
# FileName   : urls.py
# CreateDate : 2019-09-21 22:00
from django.conf.urls import url
from django.urls import path

from .views import HomeView, DeleteView, FavView, CancelFavView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    url('delete', DeleteView.as_view(), name='delete'),
    url('fav', FavView.as_view(), name='fav'),
    url('cancel', CancelFavView.as_view(), name='cancel'),
]


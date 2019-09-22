"""
urls: 
"""
# Author     : rexdu
# FileName   : urls.py
# CreateDate : 2019-09-21 22:00
from django.urls import path

from .views import HomeView

urlpatterns = [
    path('index/', HomeView.as_view(), name='home'),
]


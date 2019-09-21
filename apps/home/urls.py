"""
urls: 
"""
# Author     : rexdu
# FileName   : urls.py
# CreateDate : 2019-09-21 22:00


from django.urls import path, include

from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]


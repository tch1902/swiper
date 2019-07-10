from django.urls import path

from vip import api

urlpatterns = [
    path('info', api.vip_info),
]
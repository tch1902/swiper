from django.urls import path

from user import api

urlpatterns = [
    path('verify-phone',api.verify_phone),
    path('login',api.login),
    path('get_profile',api.get_profile),
    path('set_profile',api.set_profile),
    path('upload_profile',api.upload_profile),
]
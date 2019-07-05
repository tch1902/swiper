from django.urls import path

from user import api

urlpatterns = [
    path('verify-phone',api.verify_phone),
    path('login',api.login),
    path('get_profile',api.get_profile),
    path('set_profile',api.set_profile),
    path('upload_profile1',api.upload_profile1),
    path('upload_avatar',api.upload_avatar),

]
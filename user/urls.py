from django.urls import re_path
from .views import UserLoginapi,UserLogoutAPI

urlpatterns = [
    re_path(r'^api_login/$', UserLoginapi.as_view(), name='loginapi'),
    re_path(r'^api_logout/$', UserLogoutAPI.as_view(), name='logout'),
]

from django.urls import re_path
from .views import *

urlpatterns = [
    # re_path(r'^admin/$', AdminView.as_view(), name='admin_api_view'),
    re_path(r'^projects/$', ProjectListCreateView.as_view(), name='project-list-create'),
    re_path(r'^projects/(?P<pk>\d+)/$', ProjectDetailView.as_view(), name='project-detail'),
    re_path(r'^tasks/$', TaskListCreateView.as_view(), name='task-list-create'),
    re_path(r'^tasks/(?P<pk>\d+)/$', TaskDetailView.as_view(), name='task-detail'),
    re_path(r'^users/$', UserListCreateView.as_view(), name='user-list-create'),
    re_path(r'^users/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user-detail'),
]





import django_filters
from .models import Project,Task,Userprofile


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = ['name', 'description'] 


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['title', 'description']  

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = Userprofile
        fields = ['first_name', 'email'] 

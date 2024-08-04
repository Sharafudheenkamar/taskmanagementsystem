from django.db import models
from user.models import Userprofile

class Project(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    description = models.CharField(max_length=255,blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(Userprofile, related_name='projects_created', on_delete=models.CASCADE,blank=True, null=True)
    assigned_to = models.ManyToManyField(Userprofile, related_name='projects_assigned', blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255,blank=True, null=True)
    description = models.CharField(max_length=255,blank=True, null=True)
    status_choices = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    due_date = models.DateField(blank=True, null=True)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE,blank=True, null=True)
    assigned_to = models.ForeignKey(Userprofile, related_name='tasks_assigned', on_delete=models.CASCADE,blank=True, null=True)
    created_by = models.ForeignKey(Userprofile, related_name='tasks_created', on_delete=models.CASCADE,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
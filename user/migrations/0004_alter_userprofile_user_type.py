# Generated by Django 5.0.7 on 2024-08-03 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_userprofile_status_alter_userprofile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('MANAGER', 'Manager'), ('ADMIN', 'Admin'), ('USER', 'User')], max_length=20),
        ),
    ]

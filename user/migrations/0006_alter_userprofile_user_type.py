# Generated by Django 5.0.7 on 2024-08-03 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_userprofile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('USER', 'User'), ('MANAGER', 'Manager'), ('ADMIN', 'Admin')], max_length=20),
        ),
    ]

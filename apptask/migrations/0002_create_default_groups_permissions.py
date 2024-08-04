from django.db import migrations

def create_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Project = apps.get_model('apptask', 'Project')
    Task = apps.get_model('apptask', 'Task')

    admin_group, created = Group.objects.get_or_create(name='Admin')
    manager_group, created = Group.objects.get_or_create(name='Manager')
    user_group, created = Group.objects.get_or_create(name='User')

    # Assign permissions
    ct_project = ContentType.objects.get_for_model(Project)
    ct_task = ContentType.objects.get_for_model(Task)

    # Admin permissions
    admin_permissions = Permission.objects.filter(content_type__in=[ct_project, ct_task])
    admin_group.permissions.set(admin_permissions)

    # Manager permissions
    manager_permissions = Permission.objects.filter(content_type=ct_task)
    manager_group.permissions.set(manager_permissions)

    # User permissions (example)
    user_permissions = Permission.objects.filter(codename__in=['view_task', 'change_task'])
    user_group.permissions.set(user_permissions)

class Migration(migrations.Migration):

    dependencies = [
        ('apptask', '0001_initial'),  # This should be the initial migration file for task_management
        ('auth', '0012_alter_user_first_name_max_length'),  # Adjust based on your Django version
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions),
    ]

# Generated by Django 3.2.6 on 2021-08-25 10:29
from django.core.management.sql import emit_post_migrate_signal
from django.db import migrations


def assing_permissions(apps, schema_editor):
    # force post signal as permissions are created in post migrate signals
    # related Django issue https://code.djangoproject.com/ticket/23422
    emit_post_migrate_signal(2, False, "default")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    impersonate_user = Permission.objects.filter(
        codename="impersonate_user", content_type__app_label="account"
    ).first()
    manage_users = Permission.objects.filter(
        codename="manage_users", content_type__app_label="account"
    )

    for group in Group.objects.filter(permissions__in=manage_users).iterator():
        group.permissions.add(impersonate_user)


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0054_alter_user_language_code"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ("email",),
                "permissions": (
                    ("manage_users", "Manage customers."),
                    ("manage_staff", "Manage staff."),
                    ("impersonate_user", "Impersonate user."),
                ),
            },
        ),
        migrations.RunPython(assing_permissions, migrations.RunPython.noop),
    ]

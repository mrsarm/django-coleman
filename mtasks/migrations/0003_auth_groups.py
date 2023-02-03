from django.contrib.auth.models import Group, Permission
from django.core.management.sql import emit_post_migrate_signal
from django.db import models, migrations
import logging

logger = logging.getLogger(__name__)

public_group_permissions = {
  "Task Admin": [
      "add_task",
      "change_task",
      "delete_task",
      "view_task",
      "add_item",
      "change_item",
      "delete_item",
      "view_item",
      "add_partner",
      "change_partner",
      "delete_partner",
      "view_partner",
      "view_user",
  ],
  "Task Editor": [
      "add_task",
      "change_task",
      # "delete_task",
      "view_task",
      "add_item",
      "change_item",
      "delete_item",
      "view_item",
      "add_partner",
      "change_partner",
      # "delete_partner",
      "view_partner",
      "view_user",
  ],
}


def _add_group_permissions(apps, schema_editor):
    emit_post_migrate_signal(2, False, 'default')
    for group in public_group_permissions:
        group_rec, created = Group.objects.get_or_create(name=group)
        logger.info(f'Group "{group}" created')
        for perm in public_group_permissions[group]:
            group_rec.permissions.add(Permission.objects.get(codename=perm))
        logger.info(f'Permitting "{group}" to {", ".join(public_group_permissions[group])}')
        group_rec.save()


def _remove_group_permissions(apps, schema_editor):
    emit_post_migrate_signal(2, False, 'default')
    for group in public_group_permissions:
        group_rec = Group.objects.get(name=group)
        group_rec.delete()
        logger.info(f'Group "{group}" deleted')


class Migration(migrations.Migration):
    """
    Add basic groups "Task Admin" and "Task Editor" for users.
    """

    dependencies = [
        ('mtasks', '0002_alter_task_options'),
    ]

    operations = [
        migrations.RunPython(_add_group_permissions, _remove_group_permissions),
    ]

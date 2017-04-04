# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 03:25
from __future__ import unicode_literals

from django.db import migrations, models, connection


def remove_duplicate_allocation_sources(apps, schema_editor):
    AllocationSource = apps.get_model('core', 'AllocationSource')
    dupes = AllocationSource.objects.values('name').annotate(models.Count('id')).order_by().filter(id__count__gt=1)
    duplicate_sources = AllocationSource.objects.filter(name__in=[item['name'] for item in dupes]).order_by('name',
                                                                                                            '-id')
    allocation_source_ids_to_delete = []
    last_seen_source_name = None
    for allocation_source in duplicate_sources:
        if last_seen_source_name != allocation_source.name:
            # First time we've seen this allocation source - don't delete it.
            last_seen_source_name = allocation_source.name
            continue
        allocation_source_ids_to_delete.append(allocation_source.id)
    print('allocation_source_ids_to_delete: {}'.format(allocation_source_ids_to_delete))
    with connection.cursor() as cursor:
        for allocation_source_id in allocation_source_ids_to_delete:
            cursor.execute('DELETE FROM allocation_source_snapshot WHERE allocation_source_id = %s',
                           [allocation_source_id])
            cursor.execute('DELETE FROM instance_allocation_source_snapshot WHERE allocation_source_id = %s',
                           [allocation_source_id])
            cursor.execute('DELETE FROM user_allocation_snapshot WHERE allocation_source_id = %s',
                           [allocation_source_id])
            cursor.execute('DELETE FROM user_allocation_source WHERE allocation_source_id = %s',
                           [allocation_source_id])
            cursor.execute('DELETE FROM allocation_source WHERE id = %s', [allocation_source_id])


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0075_remove_allocationsource_source_id'),
    ]

    operations = [
        migrations.RunPython(
            remove_duplicate_allocation_sources,
            reverse_code=migrations.RunPython.noop)
    ]

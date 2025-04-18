# Generated by Django 5.2 on 2025-04-09 01:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0002_caixa'),
    ]

    operations = [
        migrations.AddField(
            model_name='caixa',
            name='origin_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype', verbose_name='Tipo de Origem'),
        ),
        migrations.AddField(
            model_name='caixa',
            name='origin_object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-16 01:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0005_preferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='userid',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]

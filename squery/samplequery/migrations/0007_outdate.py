# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-10 03:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samplequery', '0006_auto_20180104_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutDate',
            fields=[
                ('record', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='samplequery.Record')),
                ('isOutDated', models.BooleanField(default=False)),
            ],
        ),
    ]
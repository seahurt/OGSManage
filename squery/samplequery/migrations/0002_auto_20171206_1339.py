# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-06 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samplequery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='panel',
            name='panel_subtype',
            field=models.CharField(default='unknown', max_length=20, verbose_name='Panel subtype'),
        ),
        migrations.AlterField(
            model_name='tissues',
            name='tissue_full_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Tissue full name'),
        ),
    ]

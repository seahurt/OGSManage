# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-05 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('panel_name', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Panel name')),
                ('panel_path', models.CharField(max_length=500, verbose_name='Panel full path')),
                ('panel_type', models.CharField(max_length=20, verbose_name='Panel type')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_id', models.CharField(max_length=100, verbose_name='Full ID')),
                ('og_id', models.CharField(max_length=100, verbose_name='OG ID')),
                ('capm', models.CharField(max_length=100, verbose_name='CA-PM')),
                ('r1', models.CharField(max_length=500, verbose_name='R1')),
                ('r2', models.CharField(max_length=500, verbose_name='R2')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('panel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samplequery.Panel')),
            ],
        ),
        migrations.CreateModel(
            name='Tissues',
            fields=[
                ('tissue_short_name', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Tissue name')),
                ('tissue_full_name', models.CharField(max_length=100, verbose_name='Tissue full name')),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='tissue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samplequery.Tissues'),
        ),
    ]

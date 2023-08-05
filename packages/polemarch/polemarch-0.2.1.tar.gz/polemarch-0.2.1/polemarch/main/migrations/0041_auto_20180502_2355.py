# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-02 23:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_history_json_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='notes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='host',
            name='notes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='inventory',
            name='notes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='periodictask',
            name='notes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='notes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='template',
            name='notes',
            field=models.TextField(default=''),
        ),
    ]

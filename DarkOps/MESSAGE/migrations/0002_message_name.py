# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MESSAGE', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='name',
            field=models.CharField(default='', max_length=20, verbose_name='名字'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 17:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MESSAGE', '0003_auto_20171101_1722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='name',
            new_name='author',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-05 16:49
from __future__ import unicode_literals

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='启用时间')),
                ('status', models.BooleanField(default=True, verbose_name='使用状态')),
                ('username', models.CharField(blank=True, max_length=20, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=50, verbose_name='密码')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '主机',
                'verbose_name_plural': '主机列表',
            },
        ),
        migrations.CreateModel(
            name='HostDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='IP')),
                ('tgt_id', models.CharField(blank=True, max_length=50, verbose_name='目标ID')),
                ('fqdn', models.CharField(blank=True, max_length=50, verbose_name='计算机全称')),
                ('domain', models.CharField(blank=True, max_length=50, verbose_name='域名')),
                ('hwaddr_interfaces', models.CharField(blank=True, max_length=150, verbose_name='MAC地址')),
                ('cpu_model', models.CharField(blank=True, max_length=50, verbose_name='CPU型号')),
                ('kernel', models.CharField(blank=True, max_length=50, verbose_name='内核')),
                ('os', models.CharField(blank=True, max_length=50, verbose_name='操作系统')),
                ('osarch', models.CharField(blank=True, max_length=50, verbose_name='系统架构')),
                ('osrelease', models.CharField(blank=True, max_length=50, verbose_name='系统版本')),
                ('productname', models.CharField(blank=True, max_length=50, verbose_name='产品型号')),
                ('serialnumber', models.CharField(blank=True, max_length=50, verbose_name='序列号')),
                ('server_id', models.CharField(blank=True, max_length=50, verbose_name='服务ID')),
                ('virtual', models.CharField(blank=True, max_length=50, verbose_name='虚拟环境')),
                ('salt_status', models.BooleanField(default=False, verbose_name='Salt状态')),
                ('zbx_status', models.BooleanField(default=False, verbose_name='Zabbix状态')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '主机详细信息',
                'verbose_name_plural': '主机详细信息列表',
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '主机组',
                'verbose_name_plural': '主机组列表',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique='True', verbose_name='机房名称')),
                ('type', models.CharField(choices=[('DX', '电信'), ('LT', '联通'), ('YD', '移动'), ('ZJ', '自建')], default='DX', max_length=20, verbose_name='机房类型')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='机房地址')),
                ('contact', models.CharField(blank=True, max_length=100, verbose_name='联系方式')),
                ('start_Date', models.DateField(blank=True, null=True, verbose_name='租赁日期')),
                ('end_Date', models.DateField(blank=True, null=True, verbose_name='到期日期')),
                ('cost', models.CharField(blank=True, max_length=20, verbose_name='租赁费用')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '机房',
                'verbose_name_plural': '机房列表',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='名称')),
                ('brand', models.CharField(blank=True, max_length=30, verbose_name='品牌')),
                ('model', models.CharField(blank=True, max_length=30, verbose_name='型号')),
                ('ip_out', models.GenericIPAddressField(blank=True, null=True, unique=True, verbose_name='外网IP')),
                ('ip_in', models.GenericIPAddressField(blank=True, null=True, unique=True, verbose_name='内网IP')),
                ('info', models.CharField(blank=True, max_length=100, verbose_name='说明')),
                ('url', models.URLField(blank=True, max_length=100, verbose_name='访问地址')),
                ('username', models.CharField(blank=True, max_length=20, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=50, verbose_name='密码')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('idc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMDB.IDC', verbose_name='所属机房')),
            ],
            options={
                'verbose_name': '网络设备',
                'verbose_name_plural': '网络设备列表',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='服务器名称')),
                ('location', models.CharField(blank=True, max_length=30, verbose_name='机架位置')),
                ('start_date', models.DateField(verbose_name='启用日期')),
                ('status', models.BooleanField(default=True, verbose_name='使用状态')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('idc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMDB.IDC', verbose_name='所属机房')),
                ('ip', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='CMDB.HostDetail', verbose_name='IP地址')),
            ],
            options={
                'verbose_name': '服务器',
                'verbose_name_plural': '服务器列表',
            },
        ),
        migrations.CreateModel(
            name='SystemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='系统类型')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '系统类型',
                'verbose_name_plural': '系统类型列表',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='host',
            name='group',
            field=models.ManyToManyField(to='CMDB.HostGroup', verbose_name='所属主机组'),
        ),
        migrations.AddField(
            model_name='host',
            name='ip',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='CMDB.HostDetail', verbose_name='IP地址'),
        ),
        migrations.AddField(
            model_name='host',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMDB.Server', verbose_name='所属服务器'),
        ),
        migrations.AddField(
            model_name='host',
            name='system_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMDB.SystemType', verbose_name='操作系统类型'),
        ),
    ]

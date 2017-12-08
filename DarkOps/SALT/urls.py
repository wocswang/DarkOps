#encoding:utf-8
from django.conf.urls import url
from .views import *
from .file_local import *
from .file_remote import *
from django.conf import settings



urlpatterns =[
    #基本配置
    url(r'^command/$', command, name='command'),
    url(r'^server/$', server, name='server'),
    url(r'^config/(?P<server_id>[0-9]+)/$', config, name='config'),
    url(r'^config_fun/(?P<server_id>[0-9]+)/$', config_fun, name='config_fun'),
    #客户端配置
    url(r'^minions/(?P<server_id>[0-9]+)/$', minions,name='minions'),
    url(r'^minion_funs/$',minions_fun,name='minions_fun'),
    #命令操作
    url(r'^execute/(?P<server_id>[0-9]+)/$',execute,name='execute'),
    url(r'^execute_fun/(?P<server_id>[0-9]+)/$',execute_fun,name='execute_fun'),
    url(r'^result/$',result,name='result'),
    url(r'^jid_info/$',jid_info,name='jid_info'),

]
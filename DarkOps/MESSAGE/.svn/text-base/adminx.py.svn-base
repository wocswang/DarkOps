# _*_ encoding:utf-8 _*_

from xadmin import views
from .models import *
import xadmin


class MessageAdmin(object):
    list_display = ['message_name','author','detail','add_time']
    search_fields=['message_name','author','detail']
    list_filter = ['message_name','author','detail','add_time']

    model_icon = 'fa fa-commenting-o'
    style_fields = {"detail":"ueditor"}


xadmin.site.register(Message,MessageAdmin)
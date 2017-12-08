#coding: utf-8
from DjangoUeditor.models import UEditorField
from django.db import models
from datetime import datetime


class Message(models.Model):
    message_name = models.CharField(max_length=100,verbose_name=u"通知名称")
    author = models.CharField(max_length=20,verbose_name=u"名字")
    detail = UEditorField(verbose_name=u"通知详情",width=600,height=300,imagePath="MESSAGE/ueditor",filePath="MESSAGE/ueditor",default="")
    add_time = models.DateField(default=datetime.now,verbose_name=u"添加时间")

    def __str__(self):
        return self.message_name

    class Meta:
        verbose_name="通知"
        verbose_name_plural="通知列表"
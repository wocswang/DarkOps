#coding: utf-8
from django.db import models
from CMDB.models import IDC,Host
# Create your models here.
class SaltServer(models.Model):
    Role = (
    ('Master', 'Master'),
    ('Backend', 'Backend'),
    )
    idc = models.ForeignKey(IDC,verbose_name='所属机房')
    url = models.URLField(max_length=100,verbose_name='URL地址')
    username = models.CharField(max_length=50, verbose_name='用户名')
    password = models.CharField(max_length=50,verbose_name='密码')
    role = models.CharField(choices=Role,max_length=20,default='Master',verbose_name='角色')
    def __str__(self):
        return "%s - %s - %s" %(self.idc,self.url,self.role)
    class Meta:
        verbose_name = 'Salt服务器'
        verbose_name_plural = 'Salt服务器列表'

#https://docs.saltstack.com/en/latest/ref/modules/all/index.html
class Module(models.Model):
    client = models.CharField(max_length=20,default='execution',verbose_name='Salt模块类型')
    name = models.CharField(max_length=20,verbose_name='Salt模块名称')
    def __str__(self):
        return "%s - %s "% (self.client,self.name)
    class Meta:
        verbose_name = 'Salt模块'
        verbose_name_plural = 'Salt模块列表'
        unique_together = ("client", "name")

class Command(models.Model):
    cmd = models.CharField(max_length=100,verbose_name='Salt命令')
    doc = models.TextField(max_length=1000,blank=True,verbose_name='帮助文档')
    module = models.ForeignKey(Module,verbose_name='所属模块')
    def __str__(self):
        return  "%s - %s"%(self.module,self.cmd)
    class Meta:
        verbose_name = 'Salt命令'
        verbose_name_plural = 'Salt命令列表'
        unique_together = ("module", "cmd")

class Result(models.Model):
    #命令
    client = models.CharField(max_length=20,blank=True,verbose_name='执行方式')
    fun = models.CharField(max_length=50,verbose_name='命令')
    arg = models.CharField(max_length=255,blank=True,verbose_name='参数')
    tgt_type =  models.CharField(max_length=20,verbose_name='目标类型')
    #返回
    jid = models.CharField(blank=True,max_length=50,verbose_name='任务号')
    minions = models.CharField(max_length=500,blank=True,verbose_name='目标主机')
    result = models.TextField(blank=True,verbose_name='返回结果')
    #其他信息
    server = models.ForeignKey(SaltServer,verbose_name='所属Salt服务器')
    user = models.CharField(max_length=50,verbose_name='操作用户')
    datetime =models.DateTimeField(auto_now_add=True,verbose_name='执行时间')
    def __str__(self):
        return self.jid
    class Meta:
        verbose_name = '命令返回结果'
        verbose_name_plural = '命令返回结果'

class SvnProject(models.Model):
    name = models.CharField(max_length=50,blank=True,verbose_name='项目名称')
    salt_server = models.ForeignKey(SaltServer,verbose_name='所属Salt服务器')
    host = models.CharField(max_length=50,verbose_name='项目主机')
    path = models.CharField(max_length=200,verbose_name='项目根路径')
    target = models.CharField(max_length=50,verbose_name='项目目录')
    url = models.CharField(max_length=200,verbose_name='SVN地址')
    username = models.CharField(max_length=40,verbose_name='SVN账号')
    password = models.CharField(max_length=40,blank=True,verbose_name='SVN密码')
    status = models.CharField(max_length=40,default='新建',verbose_name='状态')
    create_date=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    info = models.TextField(max_length=500,blank=True,verbose_name='信息')
    def __str__(self):
        return "%s: %s - %s/%s"%(self.name,self.host,self.path,self.target)
    class Meta:
        verbose_name = 'SVN项目'
        verbose_name_plural = 'SVN项目列表'
        unique_together = ("host", "path", "target")


class Minions(models.Model):
    Status = (
    ('Unknown', 'Unknown'),
    ('Accepted', 'Accepted'),
    ('Denied', 'Denied'),
    ('Unaccepted', 'Unaccepted'),
    ('Rejected', 'Rejected'),
    )
    minion = models.CharField(max_length=50,verbose_name='客户端')
    salt_server = models.ForeignKey(SaltServer,verbose_name='所属Salt服务器')
    grains = models.TextField(max_length=500,blank=True,verbose_name='Grains信息')
    pillar = models.TextField(max_length=500,blank=True,verbose_name='Pillar信息')
    status = models.CharField(choices=Status,max_length=20,default='Unknown',verbose_name='在线状态')
    # create_date=models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    def __str__(self):
        return self.minion
    class Meta:
        verbose_name = 'Salt客户端'
        verbose_name_plural = 'Salt客户端列表'
        unique_together = ("minion", "salt_server")


class State(models.Model):
    #命令
    client = models.CharField(max_length=20,blank=True,verbose_name='执行方式')
    fun = models.CharField(max_length=50,verbose_name='命令')
    arg = models.CharField(max_length=255,blank=True,verbose_name='参数')
    tgt_type =  models.CharField(max_length=20,verbose_name='目标类型')
    #返回
    jid = models.CharField(blank=True,max_length=50,verbose_name='任务号')
    minions = models.CharField(max_length=500,blank=True,verbose_name='目标主机')
    result = models.TextField(blank=True,verbose_name='返回结果')
    #其他信息
    server = models.ForeignKey(SaltServer,verbose_name='所属Salt服务器')
    user = models.CharField(max_length=50,verbose_name='操作用户')
    datetime =models.DateTimeField(auto_now_add=True,verbose_name='执行时间')
    def __str__(self):
        return self.datetime
    class Meta:
        verbose_name = '部署结果'
        verbose_name_plural = '部署结果'

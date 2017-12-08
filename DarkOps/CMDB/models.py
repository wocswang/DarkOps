#coding: utf-8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.



class IDC(models.Model):
    name = models.CharField(unique='True',max_length=50,verbose_name=u"机房名称")
    type = models.CharField(choices=(("DX",u"电信"),("LT",u"联通"),("YD",u"移动"),("ZJ",u"自建")),max_length=20,verbose_name=u"机房类型",default='DX')
    address=models.CharField(blank=True,max_length=100,verbose_name=u"机房地址")
    contact=models.CharField(blank=True,max_length=100,verbose_name=u"联系方式")
    start_Date=models.DateField(null=True,blank=True,verbose_name=u"租赁日期")
    end_Date=models.DateField(null=True,blank=True,verbose_name=u"到期日期")
    cost=models.CharField(blank=True,max_length=20,verbose_name=u"租赁费用")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    def __str__(self):
        return self.name
    class Meta():
        verbose_name=u"机房"
        verbose_name_plural=u"机房列表"


class HostGroup(models.Model):
    name=models.CharField(max_length=30,unique=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    def __str__(self):
        return self.name

    class Meta():
        verbose_name=u"主机组"
        verbose_name_plural=u"主机组列表"



class SystemType(models.Model):
    name = models.CharField(max_length=30,unique=True,verbose_name=u"系统类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    def __str__(self):
        return self.name

    class Meta():
        verbose_name=u"系统类型"
        verbose_name_plural=u"系统类型列表"

class HostDetail(models.Model):
    ip = models.GenericIPAddressField(unique=True,verbose_name=u"IP")
    tgt_id=models.CharField(blank=True,max_length=50,verbose_name=u"目标ID")
    fqdn = models.CharField(blank=True,max_length=50,verbose_name=u"计算机全称")
    domain=models.CharField(blank=True,max_length=50,verbose_name=u"域名")
    hwaddr_interfaces=models.CharField(blank=True,max_length=150,verbose_name=u"MAC地址")
    cpu_model=models.CharField(blank=True,max_length=50,verbose_name=u"CPU型号")
    kernel=models.CharField(blank=True,max_length=50,verbose_name=u"内核")
    os =models.CharField(blank=True,max_length=50,verbose_name=u"操作系统")
    osarch=models.CharField(blank=True,max_length=50,verbose_name=u"系统架构")
    osrelease=models.CharField(blank=True,max_length=50,verbose_name=u"系统版本")
    productname=models.CharField(blank=True,max_length=50,verbose_name=u"产品型号")
    serialnumber=models.CharField(blank=True,max_length=50,verbose_name=u"序列号")
    server_id=models.CharField(blank=True,max_length=50,verbose_name=u"服务ID")
    virtual=models.CharField(blank=True,max_length=50,verbose_name=u"虚拟环境")
    salt_status=models.BooleanField(default=False,verbose_name=u"Salt状态")
    zbx_status=models.BooleanField(default=False,verbose_name=u"Zabbix状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    def __str__(self):
        return self.ip

    class Meta():
        verbose_name=u"主机详细信息"
        verbose_name_plural=u"主机详细信息列表"


class Server(models.Model):
    ip = models.OneToOneField('HostDetail',verbose_name=u"IP地址")
    name=models.CharField(blank=True,max_length=50,verbose_name=u"服务器名称")
    idc = models.ForeignKey(IDC,verbose_name=u"所属机房")
    location=models.CharField(blank=True,max_length=30,verbose_name=u'机架位置')
    start_date=models.DateField(verbose_name=u'启用日期')
    status=models.BooleanField(default=True,verbose_name=u"使用状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    def __str__(self):
        return self.name

    class Meta():
        verbose_name=u'服务器'
        verbose_name_plural=u'服务器列表'


class Host(models.Model):
    ip=models.OneToOneField(HostDetail,verbose_name=u"IP地址")
    server=models.ForeignKey(Server,verbose_name=u"所属服务器")
    system_type=models.ForeignKey(SystemType,verbose_name=u"操作系统类型")
    group=models.ManyToManyField('HostGroup',verbose_name=u"所属主机组")
    start_date=models.DateField(verbose_name=u"启用时间")
    status=models.BooleanField(default=True,verbose_name=u"使用状态")
    username=models.CharField(blank=True,max_length=20,verbose_name=u"用户名")
    password=models.CharField(blank=True,max_length=50,verbose_name=u"密码")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    def __str__(self):
        return self.ip.ip

    class Meta():
        verbose_name=u'主机'
        verbose_name_plural=u'主机列表'


class Network(models.Model):
    name=models.CharField(max_length=30,verbose_name=u"名称")
    brand=models.CharField(max_length=30,blank=True,verbose_name=u"品牌")
    model=models.CharField(max_length=30,blank=True,verbose_name=u"型号")
    ip_out=models.GenericIPAddressField(blank=True,unique=True,null=True,verbose_name=u"外网IP")
    ip_in=models.GenericIPAddressField(blank=True,unique=True,null=True,verbose_name=u"内网IP")
    info=models.CharField(blank=True,max_length=100,verbose_name=u"说明")
    url=models.URLField(max_length=100,blank=True,verbose_name=u"访问地址")
    username=models.CharField(max_length=20,blank=True,verbose_name=u"用户名")
    password=models.CharField(max_length=50,blank=True,verbose_name=u"密码")
    idc=models.ForeignKey('IDC',verbose_name=u"所属机房")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


    def __str__(self):
        return self.name


    class Meta():
        verbose_name=u"网络设备"
        verbose_name_plural=u"网络设备列表"






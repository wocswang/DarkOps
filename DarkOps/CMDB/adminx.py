# _*_ encoding:utf-8 _*_


from xadmin import views
from .models import *
import xadmin

class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True

class GlobalSettings(object):
    site_title="DarkOps后台管理平台"
    site_footer="*****有限公司"
    menu_style = "accordion"

class IDCAdmin(object):
    list_display=['name','type','address','contact','start_Date','end_Date','cost','add_time']
    search_fields=['name','type','address','contact','start_Date','end_Date','cost']
    list_filter=['name','type','address','contact','start_Date','end_Date','cost','add_time']
    model_icon='fa fa-building'

class HostGroupAdmin(object):
    list_display=['name','add_time']
    search_fields=['name']
    list_filter=['name','add_time']
    model_icon='fa fa-sitemap'

class SystemTypeAdmin(object):
    list_display=['name','add_time']
    search_fields=['name']
    list_filter=['name','add_time']
    model_icon='fa fa-cogs'

class HostDetailAdmin(object):
    list_display=['ip','tgt_id','fqdn','domain','hwaddr_interfaces','cpu_model','kernel','os','osarch','osrelease','productname','serialnumber','server_id','virtual','salt_status','zbx_status','add_time']
    search_fields=['ip','tgt_id','fqdn','domain','hwaddr_interfaces','cpu_model','kernel','os','osarch','osrelease','productname','serialnumber','server_id','virtual','salt_status','zbx_status']
    list_filter=['ip','tgt_id','fqdn','domain','hwaddr_interfaces','cpu_model','kernel','os','osarch','osrelease','productname','serialnumber','server_id','virtual','salt_status','zbx_status','add_time']
    model_icon='fa fa-television'

class ServerAdmin(object):
    list_display=['ip','name','idc','location','start_date','status','add_time']
    search_fields=['ip','name','idc','location','start_date','status']
    list_filter=['ip','name','idc','location','start_date','status','add_time']
    model_icon='fa fa-server'

class HostAdmin(object):
    list_display=['ip','server','system_type','group','start_date','status','username','password','add_time']
    search_fields=['ip','server','system_type','group','start_date','status','username','password']
    list_filter=['ip','server','system_type','group','start_date','status','username','password','add_time']
    model_icon='fa fa-bars'

class NetworkAdmin(object):
    list_display=['name','brand','model','ip_out','ip_in','info','url','username','password','idc','add_time']
    search_fields=['name','brand','model','ip_out','ip_in','info','url','username','password','idc']
    list_filter=['name','brand','model','ip_out','ip_in','info','url','username','password','idc','add_time']
    model_icon='fa fa-share-alt'



xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(IDC,IDCAdmin)
xadmin.site.register(HostGroup,HostGroupAdmin)
xadmin.site.register(SystemType,SystemTypeAdmin)
xadmin.site.register(HostDetail,HostDetailAdmin)
xadmin.site.register(Server,ServerAdmin)
xadmin.site.register(Host,HostAdmin)
xadmin.site.register(Network,NetworkAdmin)

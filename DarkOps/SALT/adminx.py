# _*_ encoding:utf-8 _*_


from .models import *
import xadmin


class SaltServerAdmin(object):
    list_display = ['idc','url','username','password','role']
    search_fields = ['idc','url','username','password','role']
    list_filter = ['idc','url','username','password','role']
    model_icon = 'fa fa-cubes'


class ModuleAdmin(object):
    list_display = ['client','name']
    search_fields = ['client','name']
    list_filter = ['client','name']
    model_icon = 'glyphicon glyphicon-cog'


class CommandAdmin(object):
    list_display = ['cmd','doc','module']
    search_fields = ['cmd','doc','module']
    list_filter = ['cmd','doc','module']
    model_icon = 'fa fa-pencil'


class ResultAdmin(object):
    list_display = ['client','fun','arg','tgt_type','jid','minions','result','server','user','datetime']
    search_fields = ['client','fun','arg','tgt_type','jid','minions','result','server','user']
    list_filter = ['client','fun','arg','tgt_type','jid','minions','result','server','user','datetime']
    model_icon = 'fa fa-pencil-square-o'



class SvnProjectAdmin(object):
    list_display = ['name','salt_server','host','path','target','url','username','password','status','create_date','info']
    search_fields = ['name','salt_server','host','path','target','url','username','password','status','info']
    list_filter = ['name','salt_server','host','path','target','url','username','password','status','create_date','info']
    model_icon = 'fa fa-code-fork'


''' 
class MinionsAdmin(object):
    list_display = ['minion','salt_server','grains','pillar','status']
    search_fields = ['minion','salt_server','grains','pillar','status']
    list_filter = ['minion','salt_server','grains','pillar','status']
    model_icon = 'fa fa-address-card'



class StateAdmin(object):
    list_display = ['client','fun','arg','tgt_type','jid','minions','result','server','user','datetime']
    search_fields = ['client','fun','arg','tgt_type','jid','minions','result','server','user']
    list_filter = ['client','fun','arg','tgt_type','jid','minions','result','server','user','datetime']
    model_icon = 'fa fa-hourglass-end'

'''

xadmin.site.register(SaltServer,SaltServerAdmin)
xadmin.site.register(Module,ModuleAdmin)
xadmin.site.register(Command,CommandAdmin)
xadmin.site.register(Result,ResultAdmin)
xadmin.site.register(SvnProject,SaltServerAdmin)

#xadmin.site.register(Minions,ModuleAdmin)
#xadmin.site.register(State,StateAdmin)
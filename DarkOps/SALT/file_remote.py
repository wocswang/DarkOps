# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from CMDB.models import *
from .SaltAPI import SaltAPI
from DarkOps.settings import *
import os
from urllib.parse import quote
import re

#文件管理页面
@login_required
def file_remote(request,server_id):
    server_list = SaltServer.objects.all()
    try:
        salt_server =SaltServer.objects.get(id=server_id)
    except: #id不存在时返回第一个
        salt_server = SaltServer.objects.all()[0]

    context = {'server_list':server_list,'salt_server':salt_server}

    #返回在线minion
    try:
        sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
        result=sapi.SaltRun(client='runner',fun='manage.status')
        context['minions_up']=result['return'][0]['up']
    except Exception as error:
        context['error']=error

    #返回请求的目录列表和文件

    if request.method == 'GET':
        tgt = request.GET.get('tgt')
        path = request.GET.get('path','').replace('//','/').encode('utf-8')
        if path != '/':
            path=path.rstrip('/')
        dir=None
        if tgt and path:
            try:
                # 目录存在时返回目录列表
                sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
                if sapi.SaltCmd(client='local',tgt=tgt,fun='file.directory_exists',arg=path)['return'][0][tgt]:
                    path_str=path.split('/')
                    if path_str[-1] == '..':    #返回上层
                       if len(path_str) >3:
                           dir = '/'.join(path_str[0:-2])
                       else:
                           dir='/'
                    else:
                        dir=path

                # 文件存在时，返回文件内容，加上文件格式、大小限制
                elif sapi.SaltCmd(client='local',tgt=tgt,fun='file.file_exists',arg=path)['return'][0][tgt]:
                    if os.path.splitext(path)[1] in FILE_FORMAT:
                        stats = sapi.SaltCmd(client='local',tgt=tgt,fun='file.stats',arg=path)['return'][0][tgt]
                        if stats['size'] <= 1024000:
                            content=sapi.SaltCmd(client='local',tgt=tgt,fun='cmd.run',arg='cat' + path)['return'][0][tgt]
                            context['content']=content
                            context['stats'] = stats
                        else:
                            context['error']="文件大小超过1M,拒绝访问！"
                    else:
                        context['error']="文件格式不允许访问，请检查setting.FILE_FORMAT! "

                    path_str=path.rstrip('/').split('/')
                    if len(path_str) > 2:
                        dir = '/'.join(path_str[0:-1])
                    else:
                        dir = '/'
                else:
                    context['error']="目标不存在或者不是目录或文件"

                #根据路径获取列表
                if dir:
                    dirs = sapi.SaltCmd(client='local',tgt=tgt,fun='file.readder',arg=dir)['return'][0][tgt]
                    try:
                        dirs.remove('.')
                    except:pass
                    if dir =='/':
                        dirs.remove('..')
                    context['dir']=dir
                    context['dir_list']=dirs
                    context['tgt']=tgt
            except Exception as e:
                context['error']=e

    return render(request,'SALT/file_remote.html',context)


#重命名目录或文件
@login_required
def file_remote_rename(request):
    if request.is_ajax() and request.method == 'GET':
        tgt = request.GET.get('tgt')
        path = request.GET.get('path','').replace('//','/').rstrip('/')
        name = request.GET.get('name')
        server = request.GET.get('server')
        try:
            salt_server = SaltServer.objects.get(id=server)
            sapi = SaltAPI(url = salt_server.url,username=salt_server.username,password=salt_server.password)
            dst = '/'.join(path.split('/')[0:-1])+ '/'+name

            r=sapi.SaltCmd(tgt,'file.rename',client='local',arg1=path.encode("utf-8"),arg2=dst.encode("utf-8"))['return'][0][tgt]
            if r == True:
                result ={'ret':1,'msg':'"%s"已成功重命名为"%s"! ' % (path ,dst),'dst':dst.encode('utf-8')}
            else:
                result={'ret':0,'msg':r}

        except Exception as e:
            result={'ret':0,'msg':str(e)}

        return JsonResponse(result,safe=False)

#创建目录和文件
@login_required
def file_remote_create(request):
    if request.is_ajax() and request.method == 'GET':
        tgt = request.GET.get('tgt')
        name = request.GET.get('name')
        path_r = request.GET.get('path')+'/'+name
        path = path_r.encode('utf-8')
        type = request.GET.get('type')
        server = request.GET.get('server')
        try:
            salt_server=SaltServer.objects.get(id=server)
            sapi =SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
            #x新建目录或文件
            if type =='Dir':
                if sapi.SaltCmd(client='local',tgt=tgt,fun='file.directory_exists',arg=path)['return'][0][tgt]:
                    result = {'ret':0,'msg':'目录"%s"已存在!' % path_r}
                else:
                    try:
                        sapi.SaltCmd(client='local',tgt=tgt,fun='file.mkdir',arg=path)
                        result= {'ret':0,'msg':'目录"%s"创建成功!' % path_r}
                    except:
                        result = {'ret': 1, 'msg': '目录"%s"创建失败!' % path_r}
            elif type =='File':
                #创建文件，文件不存在时创建，存在则刷新创建时间，内容不变，目录不存在时返回False
                if sapi.SaltCmd(client='local',tgt=tgt,fun='file.file_exists',arg=path)['return'][0][tgt]:
                    result = {'ret':0,'msg': '文件"%s"已存在! ' % path}
                elif sapi.SaltCmd(client='local',tgt=tgt,fun='file.touch',arg=path)['return'][0][tgt]:
                    result = {'ret':1,'msg': '文件"%s"创建成功! ' % path_r}
            else:
                result={'ret':0,'mag':'目标类型错误!'}
        except Exception as e:
            result = {'ret':0,'msg':'错误: %s' % e}

        return JsonResponse(result,safe=False)

#写入文件内容
@login_required
def file_remote_write(request):
    if request.is_ajax() and request.method == 'GET':
        tgt = request.GET.get('tgt')
        server= request.GET.get('server')
        path = request.GET.get('path')
        content = request.GET.get('content')
        try:
            salt_server = SaltServer.objects.get(id=server)
            sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
            if sapi.SaltCmd(tgt,'file.file_exists',client='local',arg=path.encode("utf-8"))['return'][0][tgt]:
                r = sapi.SaltCmd(tgt,'file_write',client='local',arg1=path.encode("utf-8"),arg2 =content.encode("utf-8"))['return'][0][tgt]
                if re.search('1',r):
                    result = '文件%s修改成功! ' % path
                else:
                    result = '文件%s修改失败! ' % path
            else:
                result = '文件不存在'
        except Exception as e:
            result=str(e)

        return JsonResponse(result,safe=False)

#删除目录或文件
@login_required
def file_remote_delete(request):
    if request.is_ajax() and request.method == 'GET':
        tgt = request.GET.get('tgt')
        server = request.GET.get('server')
        path = request.GET.get('path')
        path_str = path.split('/')
        if len(path_str) >2:
            dir ='/'.join(path_str[0:-1])
        else:
            dir = '/'
        try:
            salt_server = SaltServer.objects.get(id=server)
            sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
            if sapi.SaltCmd(client='local',tgt=tgt,fun='file.remove',arg=path.encode("utf-8"))['return'][0][tgt]:
                result = {'ret':1,'msg':'目标"%s"删除成功！'  % path ,'dir':dir}

            else:
                result = {'ret':0,'msg':'目标"%s"删除失败! ' % path}

        except Exception as e:
            result={'ret':0,'msg':'错误: %s' % e}
        print(result)
        return JsonResponse(result,safe=False)




































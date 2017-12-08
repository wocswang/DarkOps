# -*- coding: utf-8 -*-

import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error, json
import ssl
import json
import re
ssl._create_default_https_context = ssl._create_unverified_context
#Python 2.7.9 之后版本引入了一个新特性
#当你urllib.urlopen一个 https 的时候会验证一次 SSL 证书
#当目标使用的是自签名的证书时就会爆出一个
#urllib.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:581)> 的错误消息，



class SaltAPI:
    def __init__(self,url,username,password):
        self.__url = url.rstrip('/') #移除URL末尾的/
        self.__username = username
        self.__password = password
        self.__token_id = self.SaltLogin()
    #登陆获取token
    def SaltLogin(self):
        param = {'eauth': 'pam', 'username': self.__username, 'password': self.__password}
        params = urllib.parse.urlencode(param).encode('utf-8')

        #obj = urllib.parse.unquote(params)
        #headers = {'Accept':'application/x-yaml'}
        headers = {'X-Auth-Token': ''}
        url = self.__url+ '/login'
              #+ '/login'
        req = urllib.request.Request(url,params, headers)
        #print(url, '\n', params, '\n', headers)
        opener = urllib.request.urlopen(req)
        #print (opener.read(),'\n',opener.read().decode('utf-8'))
        content = json.loads(opener.read().decode('utf-8'))
        #content = opener.json()
        try:
            token = content['return'][0]['token']
            return str(token)
        except KeyError:
            return None

    #推送请求
    def PostRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id,'Accept':'application/json'}
        if obj:
            data, number = re.subn("arg\d*", 'arg', obj) #将arg1 arg2这些关键字都替换成arg，number为替换次数
            req = urllib.request.Request(url, data.encode('utf-8'),headers)  # obj为传入data参数字典，data为None 则方法为get，有date为post方法
        else:
            data=None#不需要data时一样需要送data,此处设置为none
            req = urllib.request.Request(url,data,headers)  # obj为传入data参数字典，data为None 则方法为get，有date为post方法

        opener = urllib.request.urlopen(req)

        post_res_formula=opener.read()
        #print(post_res_formula)
        #content = post_res_formula.json()
        content = json.loads(post_res_formula.decode('utf-8'))

        return content

    #执行命令
    def SaltCmd(self,tgt,fun,client='local_async',expr_form='glob',arg=None,**kwargs):
        params = {'client':client, 'fun':fun, 'tgt':tgt, 'expr_form':expr_form}
        if arg:
            a=arg.split(',') #参数按逗号分隔
            for i in a:
                b=i.split('=') #每个参数再按=号分隔
                if len(b)>1:
                    params[b[0]]='='.join(b[1:]) #带=号的参数作为字典传入
                else:
                    params['arg%s'%(a.index(i)+100)]=i
        if kwargs:
            params=dict(list(params.items())+list(kwargs.items()))
        # print params
        obj = urllib.parse.urlencode(params)
        #print (obj)
        res = self.PostRequest(obj)
        # print res
        return res
        #{u'return': [{u'jid': u'20160331104340284003', u'minions': [u'saltminion01-41.ewp.com']}]}
    #runner=salt-run=master本地执行
    def SaltRun(self,fun,client='runner_async',arg=None,**kwargs):
        params = {'client':client, 'fun':fun}
        if arg:
            a=arg.split(',') #参数按逗号分隔
            for i in a:
                b=i.split('=') #每个参数再按=号分隔
                if len(b)>1:
                    params[b[0]]='='.join(b[1:]) #带=号的参数作为字典传入
                else:
                    params['arg%s'%a.index(i)]=i
        if kwargs:
            params=dict(list(params.items())+list(kwargs.items()))
        # print params
        obj = urllib.parse.urlencode(params)
        res = self.PostRequest(obj)
        return res
    #获取JOB ID的详细执行结果
    def SaltJob(self,jid=''):
        if jid:
            prefix = '/jobs/'+jid
        else:
            prefix = '/jobs'
        res = self.PostRequest(None,prefix)
        # print res
        return res
    #获取grains
    def SaltMinions(self,minion=''):

        if minion and minion!='*':
            prefix = '/minions/'+minion
        else:
            prefix = '/minions'
        res = self.PostRequest(None,prefix)
        #print (res)
        return res
    #获取events
    def SaltEvents(self):
        prefix = '/events'
        res = self.PostRequest(None,prefix)
        return res

    #列出KEY
    def ListKey(self):
        prefix = '/keys'
        #print ('1')
        content = self.PostRequest(None,prefix)
        #print (content)
        accepted = content['return']['minions']
        denied = content['return']['minions_denied']
        unaccept = content['return']['minions_pre']
        rejected = content['return']['minions_rejected']
        return accepted,denied,unaccept,rejected
    #接受KEY
    def AcceptKey(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': key_id}
        obj = urllib.parse.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
    #删除KEY
    def DeleteKey(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': key_id}
        obj = urllib.parse.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

#测试：python manager.py shell ; from SALT.SaltAPI import * ; main()，代码修改了要ctrl+Z退出重进
def main():
    idc = '1'
    tgt = '*'   #  '*'不能使用list类型
    fun ='test.ping'
    client = 'local'
    arg = ['/srv/salt/test.txt','fadfwef2f']
    from .models import SaltServer
    salt_server = SaltServer.objects.get(idc=idc)
    sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
    result = sapi.SaltCmd(tgt=tgt,fun=fun,arg=arg)
    jid = result['return'][0]['jid']
    print(jid)
    jidinfo=sapi.SaltJob(jid)
    print(jidinfo)

if __name__ == '__main__':
    main()
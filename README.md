DarkOps运维管理平台

[toc]

DarkOps运维管理平台

DarkOps运维管理平台是基于Bootstrap前端技术+Django后台技术+Python语言开发的；结构上以Nginx+Wsgi+Django为展示层，以rpyc为传输层，以saltstack为控制层，以linux系统为虚拟机为被控应用层；实现系统状态监控、文件操作、代码发布、数据收集、分析统计等运维管理自动化功能。
从运维工具的角度考虑，决定选择以python语言为主，因为saltstack、ansible等都是python些的，这些工具都可以用在运维上，saltstack还有docker模块，Docker容器以后肯定也会上的，也方便管理，所以本平台选用saltstack自动化工具来操作。

后端

python语言的web框架有好多种，这里选择使用Django框架，因为它是全能型的；也和其他的框架做了对比，感觉这个比较好。
Django是Python编程语言驱动的一个开源模型-视图-控制器(MVC）风格的web应用程序框架。
本平台选用Django最新框架django==1.11.6

前端

主要以html+css+js为基础来显示前端页面，采用bootstrap,jquery,ajax等作为页面的高级使用效果更好。

数据库

Django支持多种数据库，默认使用sqlite3，仅仅一个文件，用来开发最方便，我还是比较习惯使用mysql，通过model可以直接生成对应数据库的表，更换无压力。

开发环境

这个开发环境最重要，因为它将伴随你所有的开发时间和体验，DJANGO开发工具IDE可以选择的有很多，有轻的有重的，例如sublime、Emacs、eclipse+pydev、pycharm 等等， 参考网上重多建议，选择了功能全面的Pycharm，支持git、svn、mysql管理、WIN CMD、代码补全高亮、智能提示等，还支持创建bootstrap项目。

配置管理工具

Func、Ansible、SaltStack、Puppet都属于配置管理工具，DarkOps平台决定用基于python语言的SaltStack作为控制台。

主要功能图

image

主要功能介绍

CMDB资产管理

机房

1.机房：设备统计
image

硬件服务器

2.硬件服务器：详细信息，主机统计，过滤，数据采集（grains）
image

操作主机

3.操作主机：详细信息，过滤，搜索，初始化安装（salt-ssh minion模块)，数据采集（grains)
image

网络设备

4.网络设备：web链接、过滤 image

操作系统

5.操作系统：主机统计 image

SALT配置管理

命令管理

1.命令管理：管理salt module和命令，通过'doc.runner','doc.wheel','doc.execution' 命令自动采集模块、命令、及帮助信息；非内置模块需要手动添加，比如svn. image

Minion管理

2.Minion管理：管理key的接受和删除，minions表，用于存储minion(key),状态 image grains,pillar等信息，CMDB中的数据可以根据IP来调取minion对象；还可以操作 自定义grain、pillar等数据。

接口配置

3.接口配置：SALT MASTER端REST API接口信息，关联机房；配置管理，实时获取 环境、配置等信息。 image

执行命令

image

本地文件

远程文件

代码发布

应用部署

监控平台

Host列表

image

Item列表

Graph列表

image

Template列表

Group列表

系统性能

应用状态

SQL性能

WEB性能

操作记录

登录日志

操作日志

执行记录

发布记录

部署记录

登录/首页

账户登录

image

个人信息

image

修改密码

image

后台管理

image

退出

资产管理配置

资产管理模块其中有机房列表，主机组列表,系统类型列表,主机详细信息列表，服务器列表，主机组列表，网络设备列表。本模块主要对资产做一个管理用于方便管理所拥有的资产。

资产管理 1.机房列表
image 2.主机组列表
image 3.系统类型列表
image 4.主机详细信息列表
image 5.服务器列表
image 6.主机列表
image 7.网路设备列表
image 后台管理的结构框架基本完成。主要是方便管理平台。主要完成的有资产管理模块，认证和授权模块，管理模块，资产管理的部分模块。

其中认证授权模块主要有，用户，用户组，权限的管理，管理中主要包含平台操作日志管理。

运维管理配置

运维管理模块目前已经完成salt服务器列表模块，salt模块列表，salt命令列表，接口管理模块。minion客户端模块正在编写调整。
运维管理
1.Salt服务器列表 image 2.Salt模块列表 image 3.Salt命令列表
image 4.命令返回结果 image

操作记录配置

1.日志记录 image

用户/用户组/权限管理配置

1.用户组 image 2.用户 image 3.权限 image

公告管理

通知列表

1.通知列表 image

后续

完善监控平台模块部分

使用xterm.js制作web形式console方面应用操作

主机分配及权限管理

...

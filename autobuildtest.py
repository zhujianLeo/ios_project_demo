
#! -*- coding: utf8 -*-

import os
import subprocess
import sys
import argparse
import ConfigParser
import glob
import time
from biplist import *

# pro_dir is ios xxx.xcodeproj 目录 这是我当前的python文件目录算出来的项目目录 需要手动修改为你的项目的目录 可以写成绝对路径
#pro_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'I4'))

config = ConfigParser.ConfigParser()
config.read("Untitled.conf")

def clean(dir,pro_name):
    print "开始清理!"
    print dir
    print   pro_name
    command = "cd %s; xcodebuild -target %s clean "% (dir,pro_name)
    os.system(command)

def build(dir,pro_name):
    print "编译!"
    print dir
    print   pro_name
    command = "cd %s;xcodebuild -target %s  -sdk iphoneos -configuration release" % (dir,pro_name)
    os.system(command)

def export(dir,build_config,pro_name,version,code_sign,code_profile):
    print "打包"
    print dir
    print build_config;
    print pro_name
    print version
    print code_sign
    print code_profile
    #设置ipa包的包名和存储位置
    current_time=time.strftime("%Y%m%d%H%M",time.localtime(time.time()))
    ipa_out_put = os.path.join(pro_dir,"build/%s-%s-%s-%s.ipa"%(current_time,version,pro_name,build_config))
    print "打包ipa!输出到 %s" % ipa_out_put
    command = "cd %s;xcrun -sdk iphoneos PackageApplication -v %s/build/release/%s.app -o '%s' —sign '%s'  —embed %s" % (dir,dir,pro_name,ipa_out_put,code_sign,code_profile)
    print command
    os.system(command)


#获取配置文件中的所有section并且循环遍历section，每一个section 中存储了一个渠道的所有配置
for section in config.sections():
    print config.options(section)
    
    #获取section 中各个option的值
    need_export         = config.get(section, 'need_export')
    pro_dir             = config.get(section, 'pro_dir')
    game_version        = config.get(section, 'game_version')
    build_version       = config.get(section, 'build_version')
    configuration       = config.get(section, 'configuration')
    sign_dev            = config.get(section, 'sign_dev')
    profile_dev         = config.get(section, 'profile_dev')
    sign_dis            = config.get(section, 'sign_dis')
    profile_dis         = config.get(section, 'profile_dis')
    print need_export
    print pro_dir
    print game_version
    print build_version
    print configuration
    print sign_dev
    print profile_dev
    print sign_dis
    print profile_dis
    
    if need_export == "false":
        print "section="+section+" 因为need_export = false,所以跳出了本次循环！"
        continue
    
    #获取目录下以xcodeproj后缀的所有文件名（包含xcodeproj后缀）
    f = glob.glob(pro_dir+'/*.xcodeproj')
    print pro_dir+'/*.xcodeproj'
    
    #获取目录下以xcodeproj后缀的所有文件名（不包含xcodeproj后缀）即获取需要编译项目的target
    for file in f:
        fileName = os.path.basename(file)
        (target,extension) = os.path.splitext(fileName)
        print fileName
        print target
        print extension
    
    #获取项目的info配置文件
    try:
        plist=readPlist(pro_dir+"/"+target+"/Info.plist");
        print plist
    
        print plist['CFBundleVersion']
    except InvalidPlistException,e:
        print "not a plist or plist invalid:",e

    #修改项目的info配置文件（修改了项目的游戏版本和编译版本号）
    try:
        plist['CFBundleVersion']=game_version
        plist['CFBundleShortVersionString']=build_version
        print pro_dir+"/"+target+"/Info.plist"
        writePlist(plist,pro_dir+"/"+target+"/Info.plist")
    except (InvalidPlistException, NotBinaryPlistException), e:
        print "Something bad happened:", e


    clean(pro_dir,target)

    build(pro_dir,target)

    if configuration == "both":
        print "configuration = "+configuration
        export(pro_dir,"debug",target,game_version,sign_dev,profile_dev)
        export(pro_dir,"release",target,game_version,sign_dis,profile_dis)
    elif configuration == "debug":
        print "configuration = "+configuration
        export(pro_dir,"debug",target,game_version,sign_dev,profile_dev)
    elif configuration == "release":
        print "configuration = "+configuration
        export(pro_dir,"release",target,game_version,sign_dis,profile_dis)
    else:
        print "configuration set error!"









# -*- coding: utf-8 -*
from __future__ import unicode_literals
from threading import Timer
import re
import requests
import random
import schedule
import time
import datetime
import itchat
from itchat.content import TEXT
from itchat.content import *
import pymysql
import json
import threading
#linux未更新
import cv2
import os
from pyzbar.pyzbar import decode

#网站正则
url_compile = re.compile(r"(.*?http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+.*)", re.S)

# 定向向标签为公众号的人发送信息


def thread_1():
    itchat.run()
def thread_2():
    while True:
        schedule.run_pending()  # 确保schedule一直运行
        time.sleep(1)

#获取公众号好友列表
def get_gzhFrieds(friendList):
    gzhFriend=[]
    errorList=[]
    for g in range(0,len(friendList)):
        try:
            remarkname=friendList[g]['RemarkName']
            if(remarkname[-3:]==user_tab):  #yjr  gzh
                data = {"name": friendList[g]['NickName'], "RemarkName": remarkname,'Sex': friendList[g]['Sex'],'UserName':friendList[g]['UserName']}
                gzhFriend.append(data)
        except:
            errorList.append(friendList[g]['NickName'])
    return gzhFriend

#遍历发送微信信息
def sendurl(gzhFriend):
    for item in gzhFriend:
        try:
            name=item['name']
            sex=int(item['Sex'])
            content='叮咚～\n送您一份温暖的早餐搭配，每天比别人知晓多一点，世界更精彩一点！~\(≧▽≦)/~\n\n'+url+'\n\n'
            itchat.send(content,item['UserName'])
            time.sleep(0.5)
        except:
            print(item['name']+'：有报错')



threads = []
t1 = threading.Thread(target=thread_1)  #执行自动回复
threads.append(t1)
t2 = threading.Thread(target=thread_2)  #执行定时任务
threads.append(t2)

if __name__ == "__main__":
    user_tab='gzh'  #yjr gzh
    url='https://mp.weixin.qq.com/s/9SWfCGlcuA8xYIM0c6FSag'
    itchat.auto_login(hotReload=True)
    friendList = itchat.get_friends(update=True)[1:]
    gzhFriend = get_gzhFrieds(friendList)
    print(str(len(gzhFriend)))

    #sendurl(gzhFriend)

    schedule.every().day.at("08:23").do(sendurl, gzhFriend)  # 每天定时发广告
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("退出线程")
# for g in range(0,len(friendList)):
#     itchat.send(SINCERE_WISH,friendList[g]['UserName'])
#     print((friendList[g]['RemarkName'] or friendList[g]['NickName']),'已发送')
#     sys.stdout.write(str(g+1)+"/"+str(len(friendList))+"\r")
#     sys.stdout.flush()
#     time.sleep(2)
# print('done')

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


def group(groupList):
    group = itchat.get_chatrooms(update=True)
    #print(group)
    from_group = ''
    groupUserName=[]
    for hufenGroup in groupList:
        for g in group:
            if g['NickName'] == hufenGroup:  # 从群中找到指定的群聊
                from_group = g['UserName']
                data = {"name": hufenGroup, "UserName": from_group}
                groupUserName.append(data)
    return groupUserName

def getValues(groupUserName):
    # 打开数据库连接
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='admin', db='private', charset='utf8',  #45.32.147.147  localhost
                           cursorclass=pymysql.cursors.DictCursor)      #cursorclass=pymysql.cursors.DictCursor代表返回json数据
    cursor = db.cursor()
    date = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    for item in groupUserName:
        groupSql='%'+item['name' ]
        valueList=[]
        try:
            #sql = 'select  @rowno:=@rowno+1 AS nm_order,f.* from( SELECT c.* FROM(SELECT d.*, DATE_FORMAT(d.DT_ENDDATE, "%Y-%m-%d") time FROM t_wechat_pinkread d WHERE nm_sid IN(SELECT t.id FROM(SELECT max(nm_sid) AS id, ST_WECHATID FROM t_wechat_pinkread GROUP BY ST_WECHATID ) t ) ) c WHERE c.time = "'+date+'" AND c.st_groupname LIKE "'+groupSql+'" ORDER BY c.ST_GZHNAME="求真帝" desc,c.st_gzhtype ASC, c.nm_sid  ASC)f,(select @rowno:=0) t '
            sql = 'select  @rowno:=@rowno+1 AS nm_order,f.* from( SELECT c.* FROM(SELECT d.*, DATE_FORMAT(d.DT_ENDDATE, "%Y-%m-%d") time FROM t_wechat_pinkread d WHERE nm_sid IN(SELECT t.id FROM(SELECT max(nm_sid) AS id, ST_WECHATID FROM t_wechat_pinkread GROUP BY ST_WECHATID ) t ) ) c WHERE c.time = "' + date + '" AND c.st_groupname LIKE "' + groupSql + '" ORDER BY c.ST_GZHNAME="求真帝" desc,c.nm_sid  ASC)f,(select @rowno:=0) t '
            print(sql)
            cursor.execute(sql)
            valueList = cursor.fetchall()
            item['value']=valueList
        except:
            my_friend = itchat.search_friends(name='牧蓝天')[0]['UserName']
            itchat.send(item['name']+':数据库查询数据有误', my_friend)
    cursor.close()
    db.close()
    return groupUserName

#每日规则和上报定时提醒
def job_tixing(groupUserName):
    date = str(time.strftime('%H:%M', time.localtime(time.time())))
    for item in groupUserName:
        try:
            itchat.send('定时提醒：'+date+'\n\n欢迎加入【壹周】，这是壹周的日常操作手册：\nhttps://dwz.cn/xMRuLYcd\n\n常用链接:\n1.文章上报▼\nhttps://dwz.cn/Gp4tpKBP\n2.加入打卡圈▼\nhttp://t.cn/EVtfnnf', item['UserName'])  #1.上周上报打卡统计结果▼\nhttps://shimo.im/docs/2sBmrsZ73p4By3sx/
            time.sleep(1)
            itchat.send('~上周打卡统计已出炉，请红色标记人员尽快核实\n\n统计结果▼\nhttps://shimo.im/docs/TqxeqFwrghkCfTMj/ ', item['UserName'])
            time.sleep(1)
            itchat.send('~欢迎大家拉人进群', item['UserName'])
            #picNamm = 'pic_qiandao' + item['name'][7:9] + '.jpg'
            #itchat.send_image(u'images/' + picNamm, item['UserName'])  签到小程序
            now_time = datetime.datetime.now()
            print('%s，已成功在%s发送提示消息' % (now_time,item['name']))
        except:
            my_friend= itchat.search_friends(name='牧蓝天')[0]['UserName']
            itchat.send('今天消息发送失败了',my_friend)

# 趣信圈推广
def job_tixing2(groupUserName):
    date = str(time.strftime('%H:%M', time.localtime(time.time())))
    for item in groupUserName:
        try:
            itchat.send(
                '重要通知：\n\n现推出互阅方式升级版V2.0\n\n极速互阅，十篇换一篇\n',  #操作流程▼\n1.扫码入圈、点击【公众号互粉互阅链接】、开始互阅\n\n额外提醒▼\n1.目前测试阶段，有问题群内@丁丁猫儿\n2.消息每半小时推送一次，若有打扰，还请见谅\n3.大家周末愉快~~\n
                item['UserName'])  # 1.上周上报打卡统计结果▼\nhttps://shimo.im/docs/2sBmrsZ73p4By3sx/
            time.sleep(2)
            itchat.send('1.点我开启极速互阅▼\nhttps://cdn.xinmob.cn/flow/share/showSub?subId=5c766d5a76bd182bc45d358a&shareId=showSrc&from=groupmessage&isappinstalled=0', item['UserName'])
            time.sleep(2)
            itchat.send(
                '目前测试阶段，若有问题请@丁丁猫儿，欢迎大家参加~~\n\n每30分钟推送一次，若有打扰，请见谅~',item['UserName'])

            now_time = datetime.datetime.now()
            print('%s，已成功在%s发送提示消息' % (now_time, item['name']))
        except:
            my_friend = itchat.search_friends(name='牧蓝天')[0]['UserName']
            itchat.send('今天消息发送失败了', my_friend)

#定时广告
def job_ad(groupUserName):
    for item in groupUserName:
        try:
            #itchat.send('~集中互阅、上报打卡、活跃互粉群~\n\n群详细介绍▼\nhttps://dwz.cn/ukpsdtiL\n\n要加群的看我▼\n人多了必需加微信拉：xigesi\n\n提示：加微信请备注一下：【互粉】两个字〜不然加微信的太多，很可能被忽略。', item['UserName'])
            itchat.send('~全网最高效的互粉群，限时加入！大家抓紧！', item['UserName'])
            time.sleep(1)
            itchat.send_image(u'images/ad1.png', item['UserName'])
        except:
            my_friend= itchat.search_friends(name='牧蓝天')[0]['UserName']
            itchat.send('今天在'+item['name']+'广告发送失败了',my_friend)

# 定时广告
def job_ad2(groupUserName):
    for item in groupUserName:
        try:
            itchat.send(
                '重要通知：\n\n互阅方式大升级版\n\n极速互阅，攒卡发帖\n',
                item['UserName'])  # 1.上周上报打卡统计结果▼\nhttps://shimo.im/docs/2sBmrsZ73p4By3sx/
            time.sleep(2)
            itchat.send(
                '1.点我开启极速互阅▼\nhttps://cdn.xinmob.cn/flow/share/showSub?subId=5c766d5a76bd182bc45d358a&shareId=showSrc&from=groupmessage&isappinstalled=0',
                item['UserName'])
            time.sleep(2)
            itchat.send(
                '发布文章▼\n点开上方链接后，打开第一篇文章查阅~~', item['UserName'])

        except:
            my_friend = itchat.search_friends(name='牧蓝天')[0]['UserName']
            itchat.send('今天在' + item['name'] + '广告发送失败了', my_friend)


# 22：15填报提醒
def job_jihe(groupUserName):
    for item in groupUserName:
        try:
            #itchat.send('每日互阅内容传送词：爬楼梯（方便大家从聊天记录定位每日互阅链接）', item['UserName'])
            #time.sleep(3)
            itchat.send('21:00互阅即将开始，请大家做好准备\n\n注意事项：\n\n 1、白天有填报表单的朋友请准时参加，未填报表单的朋友不要求。\n\n 2、21:00会公布今日互阅内容，只互阅，互阅完后开始签到。\n\n3、签到结束后，自由发挥，该互粉的互粉。', item['UserName'])
            time.sleep(5)
            itchat.send('互阅签到规则-找寻宝藏：\n\n请在阅读文章过程中找到“宝藏图片A、B”，并截图。\n\nP.S：签到时候需要大家上传截图佐证，并在文本框输入截图对应阅读数。\n\n更多详情▼\nhttps://dwz.cn/mHjLqbtB', item['UserName'])
            time.sleep(5)
            itchat.send('今日宝藏图片A▼', item['UserName'])
            time.sleep(5)
            itchat.send_image(u'images/baozangA.jpg', item['UserName'])
            time.sleep(5)
            itchat.send('今日宝藏图片B▼', item['UserName'])
            time.sleep(5)
            itchat.send_image(u'images/baozangB.jpg', item['UserName'])
            # itchat.send('请大家遵守规则，保持诚信！对于违规群员参考【壹周|规则说明】处理', item['UserName'])
            # itchat.send('【壹周|规则说明】:\n https://dwz.cn/ukpsdtiL', item['UserName'])
        except:
            my_friend= itchat.search_friends(name='牧蓝天')[0]['UserName']
            itchat.send('20:55集合消息发送失败了',my_friend)

#短网址生成
def get_short_url(longurl):
    querystring = {"url": longurl}
    url = "http://suo.im/api.php"

    response = requests.request("GET", url, params=querystring)

    if response.status_code != 200:
        return longurl
    else:
        return response.text

#推送今日互阅内容
def job_url(groupUserName):
    groupUserName = getValues(groupUserName)
    date = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    #print(groupUserName)
    for item in groupUserName:
        #itchat.send('各位小伙伴们久等了，今晚的互粉互阅现在开始。\n\n截止到今晚10点，共收到互粉申请' + str(len(item['value']))+ '条，请依次打开链接阅读和关注。\n\n格式说明▼\n编号-类型-群昵称-公众号名称：链接地址', item['UserName'])
        itchat.send('截止到 '+date+' 晚上8点，共收到互阅申请' + str(len(item['value'])) + '条，请依次打开链接阅读。\n\n今日宝藏图片▼\n请往上翻阅聊天记录。\n\n快速定位关键词▼\n「爬楼梯」', item['UserName'])
        time.sleep(1)
        content=''
        for val in item['value']:
            try:
                # val1=str(int(val['nm_order']))
                # val2=val['ST_GZHTYPE']
                # val3=val['ST_GROUPUSERNAME']
                # val4=val['ST_GZHNAME']
                # val5=val['ST_GZHURL']
                shortUrl=get_short_url(val['ST_GZHURL'])
                #content = '【' + str(int(val['nm_order'])) + '-' + val['ST_GZHTYPE'] + '-' + val['ST_GROUPUSERNAME'] + '-'+val['ST_GZHNAME'] + '】\n' + val['ST_GZHURL']
                #content = '【' + str(int(val['nm_order'])) + '-' + val['ST_GZHTYPE'] + '-' + val[ 'ST_GROUPUSERNAME']  + '】\n' + str(val['ST_GZHURL'])
                content += '【' + str(int(val['nm_order'])) + '-' + val['ST_GZHTYPE'] +'】\n' + str(shortUrl)+'\n\n'
                if int(val['nm_order']) == 35:
                    content += '\n\n(╯﹏╰)微信阅读冷却期1h，请后续内容间隔1小时后再进行阅读。为你带来的不便请见谅(╯﹏╰)\n\n快速定位关键词▼\n「冷却期1」\n\n\n\n'
                elif int(val['nm_order'])== 70:
                    content += '\n\n(╯﹏╰)微信阅读冷却期1h，请后续内容间隔1小时后再进行阅读。为你带来的不便请见谅(╯﹏╰)\n\n快速定位关键词▼\n「冷却期2」\n\n\n\n'
            except:
                # my_friend= itchat.search_friends(name='牧蓝天')[0]['UserName']
                # itchat.send('推送互阅内容失败',my_friend)
                print('推送互阅内容失败')
        itchat.send(content, item['UserName'])
        #print(content)
        time.sleep(5)
        itchat.send('今日互阅内容到此结束，请浏览完所有链接的朋友进行签到（不用着急，当日24:00前签到即可）。感谢你的合作！\n\n签到说明：\n①扫描二维码，点击打卡；\n②文本框输入“A:XX B.XX”(XX代表A、B文章阅读量)，如果你有什么问题或意见也可以写出来\n③上传A、B宝藏截图（完全COPY别人的图，发现一次就T）', item['UserName'])
        time.sleep(2)
        itchat.send('特别说明▼\n非常重要！请保证【群昵称-上报填写的群昵称-小程序打卡昵称】三个一致！且不要包含特殊表情！', item['UserName'])
        time.sleep(2)
        itchat.send('打卡签到二维码▼', item['UserName'])
        picNamm = 'pic_qiandao'+item['name'][7:9]+'.jpg'
        itchat.send_image(u'images/'+picNamm,item['UserName'])
        time.sleep(2)
        itchat.send('打卡签到结果示例▼', item['UserName'])
        itchat.send_image(u'images/qiandao.png', item['UserName'])
        time.sleep(2)
        itchat.send('请群员们签到完成后自由发挥', item['UserName'])

#自动回复
@itchat.msg_register([TEXT, CARD,SHARING,PICTURE], isGroupChat=True)
def group_reply_media(msg):
    # 时间段
    d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '08:00', '%Y-%m-%d%H:%M')
    d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '21:00', '%Y-%m-%d%H:%M')
    # 当前时间
    n_time = datetime.datetime.now()
    # 消息来自于哪个群聊
    chatroom_id = msg['FromUserName']
    # 发送者的昵称
    # username = msg['ActualNickName']  #群聊昵称
    usernameList=[]
    for item in groupUserName:
        value=item['UserName']
        usernameList.append(value)
    # ①群判断：消息并不是来自于需要回复的群
    if not chatroom_id in usernameList:
        return
    # ②时间判断:判断当前时间是否在范围时间内
    if not(n_time > d_time and n_time < d_time1):
        return
    #③根据文本内容再判断
    replyText = '嘿，并不反对你互粉互阅，但只是希望能集中时间，晚上（20:55集合，21:00行动）大家集体行动，提高效率！\n\n对了，你可以将你需要互阅的内容上报一下，点这里▼\nhttps://dwz.cn/Gp4tpKBP\n\n友情提示：还不听话会送飞机票哦~有什么问题可以看看群公告。'
    if msg['Type'] == TEXT:
        result = url_compile.search(msg['Content'])  #判断文本内容是否有链接
        if result is not None:
            itchat.send(replyText, chatroom_id)
    else:
        itchat.send(replyText, chatroom_id)



threads = []
t1 = threading.Thread(target=thread_1)  #执行自动回复
threads.append(t1)
t2 = threading.Thread(target=thread_2)  #执行定时任务
threads.append(t2)

if __name__ == "__main__":
    itchat.auto_login(hotReload=True)
    #itchat.auto_login(enableCmdQR=2, hotReload=True)  #linux服务器
    print('已开启程序' )
    groupList=['【壹周|粉阅群02 20:55到场】','【壹周|粉阅群03 20:55到场】']
    #groupList = [ '【壹周|粉阅群03 20:55到场】']
    groupAd = ["诚信者，行天下。互阅3群","👏拒广告高效纯互阅群👏","1🎉民众-【公众号】互粉群","互阅互粉（禁砍价）","😊互粉-需要开流量主私聊群主哦","互粉互阅500群（关注阅读到几？）","💪真诚互阅，回数字","🚺🚹互粉1群（禁互阅、禁链接）","精选高质量互粉","互赞群 不要乱改群名",'互粉互阅群不取关高质量1群','🐷 佛系互阅互粉互广②群','高质量公众号互粉群1',"互关、互阅、广告！😊","梦马●互粉","最后的互阅群。"]
    groupUserName=group(groupList)   #获取需要管理的群UserName
    groupAdName=group(groupAd)   #获取需要发送广告的的群UserName
    #job_ad(groupAdName)
    #job_tixing(groupUserName)             #发送定时提醒和规则  #获取数据库里的数据】
    #job_tixing2(groupUserName)  # 发送定时趣兴广告
    #job_jihe(groupUserName)               #22:15集合提醒
    #job_url(groupUserName)                #22:30发送互阅内容和签到图片

    schedule.every().day.at("08:00").do(job_tixing,groupUserName)
    schedule.every().day.at("09:00").do(job_tixing, groupUserName)
    schedule.every().day.at("10:00").do(job_tixing,groupUserName)
    schedule.every().day.at("11:00").do(job_tixing, groupUserName)
    schedule.every().day.at("12:00").do(job_tixing,groupUserName)
    schedule.every().day.at("13:00").do(job_tixing, groupUserName)
    schedule.every().day.at("14:00").do(job_tixing,groupUserName)
    schedule.every().day.at("15:00").do(job_tixing, groupUserName)
    schedule.every().day.at("16:00").do(job_tixing,groupUserName)
    schedule.every().day.at("17:00").do(job_tixing, groupUserName)
    schedule.every().day.at("18:00").do(job_tixing,groupUserName)
    schedule.every().day.at("19:00").do(job_tixing, groupUserName)
    schedule.every().day.at("20:00").do(job_tixing, groupUserName)#规则和提醒每隔2H发送一次
    schedule.every().day.at("20:55").do(job_jihe,groupUserName)   # 规定每天提醒大家集合
    schedule .every().day.at("21:00").do(job_url,groupUserName)   # 规定每天执行公布内容
    schedule.every().day.at("23:59").do(job_ad, groupAdName)      # 每天定时发广告
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print ("退出线程")


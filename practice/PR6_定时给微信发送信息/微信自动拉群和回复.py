# -*- coding: utf-8 -*
import datetime
import re
from threading import Timer

import itchat
from itchat.content import *

# 小宇宙今天新闻匹配正则
xyz_compile = re.compile(r'.*?小宇宙整理.*?%d月%d日.*'
                         % (datetime.datetime.now().month, datetime.datetime.now().day), re.S)

# 验证好友信息正则，关键词中有Python，Py和加群的关键字就可以了
add_friend_compile = re.compile(r'宠物|交流|加群')

# 获取用户昵称的正则的
nickname_compile = re.compile(r'NickName\':\'(.*)\'', re.S)


# # 小宇宙日报抓取
# @itchat.msg_register([TEXT], isGroupChat=True)
# def xyz_reply(msg):
#     group_list = [u'我是渣渣辉', u'我是轱天乐', u'探挽懒月']
#     group_name = []
#     for group in group_list:
#         chat = itchat.search_chatrooms(name=group)
#         if len(chat) > 0:
#             group_name.append(chat[0]['UserName'])
#     # 过滤小宇宙新闻
#     result = xyz_compile.search(msg['Content'])
#
#     print(msg['ActualNickName'] + " : " + msg['Content'])
#
#     if result is not None:
#         if result.group() is not None and msg['ActualNickName'] == u'小宇宙':
#             for group in group_name:
#                 itchat.send('%s' % (msg['Content']), toUserName=group)


# 每个半个小时发依次信息貌似能防止掉线
def loop_send():
    global count
    itchat.send('主人，我还在正常工作，请放心！'
                , toUserName=itchat.search_friends(name=u'老婆')[0]['UserName'])
    count += 1
    if count < 10000:
        Timer(1800, loop_send).start()


# 自动通过加好友
@itchat.msg_register(itchat.content.FRIENDS)
def deal_with_friend(msg):
    if add_friend_compile.search(msg['Content']) is not None:
        itchat.add_friend(**msg['Text'])  # 自动将新好友的消息录入，不需要重载通讯录
        itchat.send_msg('嘤嘤嘤，我是智障机器人小Pig，\n很高兴认识你，回复关键字:\n\n 加群，公众号 \n 来继续我们的故事！',
                        msg['RecommendInfo']['UserName'])
        #itchat.send_image('welcome.png', msg['RecommendInfo']['UserName'])





# 自动处理信息
# 1.加好友后发送加群信息
# 2.过滤加群信息
# 3.公众号推荐
# 4.打赏
@itchat.msg_register([TEXT])
def deal_with_msg(msg):
    text = msg['Content']
    if text == u'加群':
        # itchat.add_member_into_chatroom('@@a451d37e79fe3e68e26dbfc71cae299fe51d568d201881691c62394f31f8547c',
        #                                 [{'UserName': msg['FromUserName']}], useInvitation=False)
        itchat.send_image('images/q1.jpg', msg['FromUserName'])
    elif text == u'公众号':
        itchat.send_image('images/gongzhong.jpg', msg['FromUserName'])
    else:
        itchat.send_msg('不好意思，你说的我好像不太明白，请回复关键字:\n\n 加群，公众号 \n 来继续我们的故事！', msg['FromUserName'])


# 获得群聊id
def get_group_id(group_name):
    group_list = itchat.search_chatrooms(name=group_name)
    return group_list[0]['UserName']


if __name__ == '__main__':
    count = 0
    Timer(1800, loop_send).start()
    #itchat.auto_login(enableCmdQR=2, hotReload=True)  #这是在linux服务器上
    itchat.auto_login(hotReload=True)
    # result=itchat.get_chatrooms()
    # cc=itchat.search_chatrooms(userName=u'@@88b584890fe623132a09d9c4786d51f9857f77f5092dd4aa322cf9997fd78928')
    # DD=itchat.search_chatrooms(name='@@88b584890fe623132a09d9c4786d51f9857f77f5092dd4aa322cf9997fd78928')
    # print(result)
    # print(cc)
    # print(DD)
    itchat.run()


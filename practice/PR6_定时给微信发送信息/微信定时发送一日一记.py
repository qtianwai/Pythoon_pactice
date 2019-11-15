# -*- coding: utf-8 -*
from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests
import random
import schedule
import time
import datetime

bot = Bot(cache_path=False) #登陆网页微信，并保存登陆状态


# linux执行登陆请调用下面的这句
#bot = Bot(console_qr=2,cache_path="botoo.pkl")
def send_news(contents):
    try:
        my_girlfriend = bot.friends().search(u'X_sky')[0] #我女朋友
        my_girlfriend.send(contents)
        my_girlfriend.send(u'请务必在23:50前填写完毕，24:00会同步今日数据')
        now_time = datetime.datetime.now()
        print('%s，已成功发送提示消息' % (now_time))

    except:
        my_friend = bot.friends().search(u'X_sky')[0]
        my_friend.send(u"今天消息发送失败了")

def job():
    contents = '一日一记：' + '\n' + 'https://wj.qq.com/s2/3067586/d212/'
    send_news(contents)


if __name__ == "__main__":
    # 定时
    print('已开启程序' )
    schedule.every().day.at("21:40").do(job)  # 规定每天23:11执行job()函数
    while True:
        schedule.run_pending()  # 确保schedule一直运行
        time.sleep(1)
    bot.join()  # 保证上述代码持续运行



#自动回复
# @bot.register(my_friend)
# def forward_boss_message(msg):
#     msg.forward(bot.file_helper, prefix='施冰艳发言')
#
# # 堵塞线程，并进入 Python 命令行
# embed()
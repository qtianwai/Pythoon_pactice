# -*- coding: utf-8 -*
import qqbot
import requests
import bs4
import time
import pyautogui
import pyperclip
import schedule
from threading import Timer
import threading

def thread_2():
    while True:
        schedule.run_pending()  # 确保schedule一直运行
        time.sleep(1)
def douban(url,topicUrl):
    print('程序开始了，你有3S的准备时间，按 ctrl+c 退出')
    time.sleep(3)
    pyautogui.click(221, 1060, button='left')  # 221,1060是目前chorme浏览器在我电脑的位置
    time.sleep(3)
    pyautogui.click(1898, 16, button='left')  # 关闭浏览器
    time.sleep(5)
    pyautogui.click(221, 1060, button='left')  # 221,1060是目前chorme浏览器在我电脑的位置
    time.sleep(3)
    pyautogui.click(298, 57, button='left')  # 298,57是输入框位置
    pyperclip.copy(url + '/' + topicUrl+ '/')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    time.sleep(5)  # 怕网页没加载完
    pyautogui.moveTo(1915, 130, duration=1)  # 1915, 130是滚动栏位置
    pyautogui.dragTo(1915, 1058, duration=1)  # 1915, 1007是滚动栏底部位置
    # result = pyautogui.locateCenterOnScreen('聊天框.png')
    # pyautogui.click(result[0], result[1], button='left')
    pyautogui.click(800, 830, button='left')  # 移动到输入框位置
    pyperclip.copy('欢迎大家继续加入')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(3)
    # result = pyautogui.locateCenterOnScreen('send.png')
    # if result != None:
    #     pyautogui.click(result[0], result[1], button='left')
    pyautogui.click(1070, 915, button='left')  # 移动到发送位置
    time.sleep(3)
    pyautogui.click(1898, 16, button='left')  # 关闭浏览器
    date = str(time.strftime('%H:%M', time.localtime(time.time())))
    print('定时提醒：'+date+'已结束')

threads = []
t2 = threading.Thread(target=thread_2)  #执行定时任务
threads.append(t2)

if __name__ == '__main__':
    pyautogui.PAUSE =1
    pyautogui.FAILSAFE = True
    topicGroup=['150938963','150938881','150938802','150938717','150938601','150938232'] #发言帖子
    baseUrl = 'https://www.douban.com/group/topic'
    print("自动留言程序已启动")
    schedule.every().day.at("07:12").do(douban, baseUrl,topicGroup[0])
    schedule.every().day.at("08:19").do(douban, baseUrl, topicGroup[1])
    schedule.every().day.at("15:05").do(douban, baseUrl, topicGroup[2])
    schedule.every().day.at("10:24").do(douban, baseUrl, topicGroup[3])
    schedule.every().day.at("12:46").do(douban, baseUrl, topicGroup[4])
    schedule.every().day.at("15:22").do(douban, baseUrl, topicGroup[5])
    schedule.every().day.at("11:31").do(douban, baseUrl, topicGroup[0])
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print ("退出线程")





# -*- coding: utf-8 -*
import qqbot
import requests
import bs4
import time
import pyautogui
import pyperclip


##SentQQ
# class QQ(object):
#     def __init__(self):
#         self.qqnumber = '345681007'
#         self.message = '信息自动推送功能test!!!'
#         self.groupname = ['坚果日报内部群']
#         self.bot = qqbot._bot
#
#     def sendMsgToGroup(self, msg, group, bot):
#         for group in group:
#             bg = bot.List('group', group)
#             if bg is not None:
#                 bot.SendTo(bg[0], msg)
#
#     def main(self):
#         self.bot.Login(['-q', self.qqnumber])
#         self.sendMsgToGroup(self.message, self.groupname, self.bot)


##爬取数据
# class GetData(object):
#     def __init__(self):
#         self.rooturl = 'https://www.xxxx.com'
#         self.url = self.rooturl + '/ah/20?lang=1'
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
#
#     def getdata(self):
#         response = requests.get(self.url, headers=self.headers)
#         if int(response.status_code) == 200:
#             htmldata = bs4.BeautifulSoup(response.text, 'html.parser')
#             blognumber = 0
#             result = "[%s] 技术文章推荐: \n \n" % (time.strftime('%Y-%m-%d', time.localtime(time.time())))
#             for k in htmldata.find_all('a'):
#                 if blognumber <= 10:
#                     try:
#                         if k['title'] != '':
#                             blogurl = self.rooturl + str(k['href'])
#                             blogtitle = str(k['title'])
#                             bloginfo = "%d.[%s] \n  %s \n" % (blognumber, blogtitle, blogurl)
#                             result = result + bloginfo
#                             blognumber += 1
#                     except:
#                         pass
#
#         return result

#流程：自动识别搜索位置，鼠标定位，从QQ群号遍历，输入第一个QQ群号513732983，鼠标下移固定尺寸，鼠标双击，粘贴文本，输入（ctrl+enter），选取关闭；回到搜索位置，继续后续操作，制止遍历完
# pyautogui.moveTo(600,600,duration=0.5)
if __name__ == '__main__':
    pyautogui.PAUSE =1
    pyautogui.FAILSAFE = True
    f = open('QQ.txt')
    content=f.read()
    QQGroup=['群聊1','群聊2','群聊3','群聊4','sadasdas哈哈'] #必须保证第一个群是能被查到的
    falseGroup=[]
    SuccessGroup=[]
    mouseX_guanbi=960 #给关闭按钮随便先给个数
    mouseY_guanbi =540 #给关闭按钮随便先给个数
    mouseY_chat=540 #给关闭按钮随便先给个数
    print('程序开始了，你有3S的时间将QQ显示在首页，按 ctrl+c 退出')
    time.sleep(3)
    print('3S准备时间已到，程序开始执行')
    index=0
    for item in QQGroup:
        result=pyautogui.locateCenterOnScreen('图像识别/不变定位.png') #编辑个性签名不会变，搜索框(y+43),第一个结果选项（y+119）
        mouseX=result[0]
        mouseY=result[1]
        mouseY1 = mouseY+43  #搜索框Y值
        mouseY2 = mouseY+110  # 查询结果Y值
        pyperclip.copy(item)
        pyautogui.doubleClick(mouseX,mouseY1,button='left')
        pyautogui.hotkey('delete')
        pyautogui.hotkey('ctrl', 'v')
        print('已点击搜索框，并输入第一个群号'+str(item))
        pyautogui.doubleClick(mouseX, mouseY2, button='left')  # 双击搜索结果
        if index==0:
            result = pyautogui.locateCenterOnScreen('图像识别/聊天框关闭按钮.png')#以第一个关闭为标准
            mouseX_guanbi = result[0]
            mouseY_guanbi = result[1]
            mouseY_chat = result[1] - 40
        pyperclip.copy(content)
        pyautogui.click(mouseX_guanbi, mouseY_chat, button='left')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('ctrl', 'enter')
        pyautogui.click(mouseX_guanbi, mouseY_guanbi, button='left')
        pyautogui.hotkey('enter')  # 防止有些群设置禁言
        print('已发送消息，群号为' + item)
        SuccessGroup.append(item)
        index=index+1
    print('一共发送'+str(len(SuccessGroup))+'个群');print(str(SuccessGroup))
    print('循环已结束')






import json
import re
import time

import pymysql
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

print('请输入用户')
id = '1462544284'
print('请输入密码')
password = 'HYsby12180219'
account = {"account": id, "password": password}
qq_url = 'https://qzone.qq.com/'


def  writeTxt(html,type):
    haveFunFile=open('留言板内容.txt',type,encoding="utf-8")
    haveFunFile.write(html)

def login():
    driver = webdriver.Chrome(executable_path='D:\爬虫相关\chromedriver_win32/chromedriver.exe')
    driver.get(qq_url)
    driver.switch_to.frame('login_frame')
    driver.find_element_by_id('switcher_plogin').click()
    driver.find_element_by_id('u').clear()
    driver.find_element_by_id('u').send_keys(account['account'])
    driver.find_element_by_id('p').clear()
    driver.find_element_by_id('p').send_keys(account['password'])
    driver.find_element_by_id('login_button').click()
    time.sleep(10)  #QQ有个SB弹框消息，刚好挡住后面的点击内容，这里设置时间久一点，让他加载出来了我们后面点掉他
    driver.switch_to.default_content()
    try:
        driver.find_element_by_xpath("//div[@id='qz_notification']/a[@class='op-icon icon-close']").click() #点掉弹出框
        print("去掉弹出框")
    except Exception as e:
        print("Exception found", format(e))

    driver.find_element_by_xpath("//ul[@class='head-nav-menu']/li[@class='menu_item_334']/a").click()
    time.sleep(3)
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[1]"))
    html = driver.page_source
    page = 1
    writeTxt(html,'w')  #已经获取到第一业的html文件，继续获取剩下的页码
    print('已录入第1页内容')
    while page<11:   #最多获取前10页留言
        elem= driver.find_element_by_xpath("//div[@id='pager_bottom']/div/p/a[last()]")
        elem_class=elem.get_attribute("class")
        if elem_class!='c_tx none':
            driver.execute_script("arguments[0].scrollIntoView(false);",elem)
            elem.click()
            page += 1   #跳转到下一页页码
            time.sleep(3)
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element_by_xpath("//iframe[1]"))
            appendHtml = driver.page_source
            writeTxt(appendHtml,'a')
            print('已录入第%s页内容' % (page))
        else:
            print('已录入完毕')
            break  #已经到最后一页，跳出循环
    driver.quit()

#程序主入口
login()   #自动登录，获取留言板内容，并将内容保存至txt文件中
print('aaa')



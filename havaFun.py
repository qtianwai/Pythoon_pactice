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
headers = {
    'authority': 'user.qzone.qq.com',
    'method': 'GET',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}
def gethtml(url_singer):
    driver = webdriver.Chrome(executable_path='D:\爬虫相关\chromedriver_win32/chromedriver.exe')
    driver.get(url_singer)
    time.sleep(1)
    driver.switch_to.frame('g_iframe')
    time.sleep(2)
    html=driver.page_source
    driver.quit()
    return html

def getHtmlByRequets(url):  #url+?直接访问网页
    try:
        kv={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        re=requests.request('get',url,timeout=30,headers=kv)
        re.raise_for_status()
        re.encoding=re.apparent_encoding
        return re.text
    except:
        print('访问页面有误')
        return


def parse_listSong(html):
    soup=BeautifulSoup(html,'html.parser')
    html=soup.prettify()
    songs=soup.findAll('tbody')[0].findAll('a',attrs={"href":re.compile(r'song.*=\d+')})
    songs_title = soup.findAll('tbody')[0].findAll('b')
    song_listurl=[]
    for i in range(len(songs)):
        try:
            song=songs[i]
            songUrl='http://music.163.com/api/song/lyric?id='+re.search(r'=(\d+)',song.attrs["href"]).group(1)+'&lv=1&kv=1&tv=-1'
            songInfo={'url':songUrl}
            songInfo['title']=songs_title[i].attrs['title']
            song_listurl.append(songInfo)
        except:
            print(str(Exception))
            continue
    return song_listurl



def parse_dirSong(html_txt,song):
    json_song=json.loads(html_txt)
    songWords=json_song['lrc']['lyric']
    words=re.sub(r'\[.*\]','',songWords).strip()
    song['lyric']=words
    return song


def saveInMysql(song):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "admin", "pythontest", charset='utf8')
    cursor = db.cursor()
    try:
        sql="select * from t_hy_song_i where st_title='%s'" %song['title']
        cursor.execute(sql)
        rs = cursor.fetchall()
        if len(rs) == 0:
            effect_row = cursor.executemany("insert into t_hy_song_i(st_title,st_lyric,st_url)values(%s,%s,%s)",
                                            [(song['title'], song['lyric'], song['url'])])
            db.commit()
    finally:
        cursor.close()
        db.close()

def  writeTxt(html):
    haveFunFile=open('havefun2.txt','w',encoding="utf-8")
    haveFunFile.write(html)

#不太明白
def get_g_tk(cookie):
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)  # ord()是用来返回字符的ascii码
    return hashes & 0x7fffffff

#不明白
def back_session(realCookie):
    session = requests.session()
    c = requests.utils.cookiejar_from_dict(realCookie, cookiejar=None, overwrite=True)
    session.headers = headers
    session.cookies.update(c)   #设置session对应的cookie？这部分不应该服务器已经配置好了吗？
    return session

def get_allQQ(mysession, g_tk, qzonetoken):
    # 获取好友QQ的网址
    url_friend = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?' \
                 'uin=' + account['id'] + '&do=1&fupdate=1&clean=1&g_tk=' + str(g_tk) + '&qzonetoken=' + qzonetoken

    friendIdpat = '"uin":(.*?),'
    friendNamepat = '"name":(.*?),'
    resp = mysession.get(url_friend)
    friendIdlist = re.compile(friendIdpat).findall(resp.text)
    friendNameList = re.compile(friendNamepat).findall(resp.text)
    nvs = zip(friendNameList, friendIdlist)
    nvDict = dict((name, value) for name, value in nvs)
    time.sleep(3)
    return nvDict


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
    time.sleep(3)
    driver.switch_to.default_content()
    driver.find_element_by_class_name('menu_item_334').click()
    html = driver.page_source
    xpat = r'window\.g_qzonetoken = \(function\(\)\{ try{return \"(.*)";'
    #cookie处理
    qzonetoken = re.compile(xpat).findall(html)[0]  #获取token
    cookies = driver.get_cookies()
    realCookie = {}
    for elem in cookies:
        realCookie[elem['name']] = elem['value']
    g_tk = get_g_tk(realCookie)  #没搞懂
    session = back_session(realCookie) #没搞懂
    print(g_tk, realCookie, session.cookies)
    friend_list = get_allQQ(session, g_tk, qzonetoken)
    print(friend_list)

    return driver

#程序主入口
login()



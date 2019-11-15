import json
import re
import time

import pymysql
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

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



#程序主入口
url_singer="https://music.163.com/#/artist?id=13193"
html_song=gethtml(url_singer)#获取歌手歌曲列表页面
song_list=parse_listSong(html_song)#对列表进行解析，获取每一首歌的url地址
count=0
errot_count=0
for song in song_list:
    try:
        url=song['url']
        html_txt=getHtmlByRequets(url)#获取每一首歌子页面内容
        song=parse_dirSong(html_txt,song)#解析html，获取title和歌词
        saveInMysql(song)#将歌曲名，歌词内存存入数据库
        count=count+1
        left=len(song_list)-count-errot_count
        print('存入歌曲',song['title'],'成功,已存入',count,'首歌曲，存入失败',errot_count, '首歌曲,还剩余', left, '首歌曲待解析')
    except:
        print(str(Exception))
        errot_count = errot_count + 1
        left = len(song_list) - count-errot_count
        print('存入歌曲',song['title'],'失败,已存入', count, '首歌曲，存入失败',errot_count, '首歌曲,还剩余', left, '首歌曲待解析')
        continue

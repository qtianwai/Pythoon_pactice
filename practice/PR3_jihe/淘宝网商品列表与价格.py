import re

from bs4 import BeautifulSoup
import requests
__author__ = 'xzy'

def getHtml(url):  #url+?直接访问网页
    try:
        kv={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        re=requests.request('get',url,timeout=30,headers=kv)
        re.raise_for_status()
        re.encoding=re.apparent_encoding
        return re.text
    except:
        print('访问页面有误')
        return

def parseHtml_byBeautiful(html):
    soup=BeautifulSoup(html,'html.parser')
    txt=soup.prettify()
    print(txt)

def parsreHtml_byRe(html,list):
    try:
        titles=re.findall(r'\"raw_title\"\:\".*?\"',html)  #"raw_title":"新飞小型冰箱三门家用冷藏冷冻小冰箱三开门式电冰箱双门宿舍节能"
        prices = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)  # "view_price":"698.00"
        for i in range(len(titles)):
            title=eval(titles[i].split(':')[1])
            price=eval(prices[i].split(':')[1])
            list.append([title,price])
        return list
    except:
        print('解析出错')
        return ''


def printScreen(result):
    tplt = "{:4}\t{:20}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in result:
        count = count + 1
        print(tplt.format(count, g[1], g[0]))


#程序执行
def main():
    keyword='冰箱'
    depth=2
    start_url='https://s.taobao.com/search?q='+keyword
    infolist=[]
    for i in range(depth):
        try:
            start_url+='&s='+str(i*44)
            html=getHtml(start_url)
            parsreHtml_byRe(html,infolist)
        except:
            continue
    printScreen(infolist)

main()









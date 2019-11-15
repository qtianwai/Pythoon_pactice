# -*- coding: utf-8 -*-
import re

import scrapy
from selenium import webdriver


class Mayday(scrapy.Spider):
    name = 'mayday'

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='D:\爬虫相关\chromedriver_win32/chromedriver.exe')
        self.browser.set_page_load_timeout(4)

    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def start_requests(self):
        start_urls = ['https://music.163.com/#/artist?id=13193']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        print(selector)
        print('---------------------------------------------------')
    # def parse(self, response):
    #     for i in range(5):
    #         #link = sel.xpath('@href').extract()
    #         try:
    #             item=response.xpath('//div[@class="node_list"]/div')[i]
    #             text= item.xpath('text()').extract()
    #             id=re.findall(r'\d{6}',text[0])[0]
    #             print(id)
    #             url_stcoks = 'https://gupiao.baidu.com/stock/'
    #             url=url_stcoks+'sh'+id+'.html'
    #             yield scrapy.Request(url,callback=self.parse_stock)
    #         except:
    #             continue
    #
    # def parse_stock(self,response):
    #     infodick={}
    #     name=response.xpath('//a[@class="bets-name"]/text()')[0].extract().strip()
    #     name=re.findall(r'[\u4e00-\u9fa5]+',name,re.S)[0]
    #     #print(name)
    #     infodick['标题']=name
    #     titles=response.xpath('//dt')
    #     values=response.xpath('//dd')
    #     for i in range(len(titles)):
    #         title=titles[i].xpath('text()').extract()[0]
    #         value=values[i].xpath('text()').extract()[0]
    #         infodick[title]=value
    #     print(infodick)
    #     yield infodick






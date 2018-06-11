# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import re

from PR1_douban_zufang import html_downloader


def blogParser(index):

  cnblogs = html_downloader.requestCnblogs(index)
  soup = BeautifulSoup(cnblogs, 'html.parser')
  all_div = soup.find_all('a',href=re.compile(r"https://www.douban.com/group/topic"))

  blogs = []
  #循环div获取详细信息
  for item in all_div:
  #     < a
  #
  #     class ="" href="https://www.douban.com/group/topic/110386760/" title="无中介（合租）八号线曲阳地铁豪华装修，只限爱干净女生，付三押一月租费1780。" >
  #
  #     无中介（合租）八号线曲阳地铁豪华装修，只限爱干...
  # < / a >
      blog = analyzeBlog(item)
      blogs.append(blog)

  return blogs

#解析每一条数据
def analyzeBlog(item):
    result = {}
    a_title = item['title']
    a_href=item['href']
    a_text=item.get_text()
    if a_title is not None:
        # 博客标题
        result["title"] = a_title
        result["href"] = a_href
        result["text"] = a_text
    return result



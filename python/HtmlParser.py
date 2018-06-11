# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import re

from python import url_spider


def blogParser(index):

  cnblogs = url_spider.requestCnblogs(index)
  soup = BeautifulSoup(cnblogs, 'html.parser')
  # <tr class="">
  #               <td class="title">
  #
  #                   <a href="https://www.douban.com/group/topic/118082407/" title="五角场附近 绿色米兰奥特莱斯对面  南北通透精装修一室户 直租  无中介费 服务费 性价比高" class="">
  #                      五角场附近 绿色米兰奥特莱斯对面  南北通透精装修...
  #                   </a>
  #               </td>
  #               <td nowrap="nowrap"><a href="https://www.douban.com/people/175318099/" class="">懵懂懵圈</a></td>
  #               <td nowrap="nowrap" class="">24</td>
  #               <td nowrap="nowrap" class="time">06-10 21:55</td>
  #           </tr>
  all_div = soup.find('div',attrs={'class': 'olt'}).find_all('a',href=re.compile(r"https://www.douban.com/group/topic"))

  blogs = []
  #循环div获取详细信息
  for item in all_div:
      blog = analyzeBlog(item)
      blogs.append(blog)

  return blogs

#解析每一条数据
def analyzeBlog(item):
    result = {}
    a_title = find_all(item,'a','titlelnk')
    if a_title is not None:
        # 博客标题
        result["title"] = a_title[0].string
        # 博客链接
        result["href"] = a_title[0]['href']
    p_summary = find_all(item,'p','post_item_summary')
    if p_summary is not None:
        # 简介
        result["summary"] = p_summary[0].text
    footers = find_all(item,'div','post_item_foot')
    footer = footers[0]
    # 作者
    result["author"] = footer.a.string
    # 作者url
    result["author_url"] = footer.a['href']
    str = footer.text
    time = re.findall(r"发布于 .+? .+? ", str)
    result["create_time"] = time[0].replace('发布于 ','')

    comment_str = find_all(footer,'span','article_comment')[0].a.string
    result["comment_num"] = re.search(r'\d+', comment_str).group()

    view_str = find_all(footer,'span','article_view')[0].a.string
    result["view_num"] = re.search(r'\d+', view_str).group()

    return result

def find_all(item,attr,c):
    return item.find_all(attr,attrs={'class':c},limit=1)

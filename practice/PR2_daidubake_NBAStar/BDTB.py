# -*- coding:utf-8 -*-
#主要研究根据正则表达式筛选字符串
import re
import urllib.request
import urllib.parse

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()
# 百度贴吧爬虫类
class BDTB:

    # 初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool=Tool()
        self.file = None
        self.floorTag='1'
        self.floor=1

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
          #  request = urllib.Request(url)
            response = urllib.request.urlopen(url)
            response_result=response.read()
            html=response_result.decode('utf-8')
           # print (html)
            return html
        except urllib.URLError as e:
            if hasattr(e, "reason"):
                print ("连接百度贴吧失败,错误原因", e.reason)
                return None

    # 获取帖子标题
    def getTitle(self):
        page = self.getPage(1)
        #class ="core_title_txt pull-left text-overflow  " title="纯原创我心中的NBA2014-2015赛季现役50大" style="width: 396px" > 纯原创我心中的NBA2014-2015赛季现役50大 < / h3 >
        pattern = re.compile('<h3 class="core_title_txt pull-left text-overflow  .*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            # print result.group(1)  #测试输出
            return result.group(1).strip()
        else:
            return None

    # 获取帖子一共有多少页
    # < liclass ="l_reply_num" style="margin-left:8px" > < span class ="red" style="margin-right:3px" > 141 < / span > 回复贴，共 < span class ="red" > 5 < / span > 页 < / li >
    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            # print result.group(1)  #测试输出
            return result.group(1).strip()
        else:
            return None

    # 获取每一层楼的内容,传入页面内容
    def getContent(self):
        page = self.getPage(1)
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content)
        return contents

    def writeData(self, contents):
        # 向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == '1':
                # 楼之间的分隔符
                floorLine = "\n" + str(
                    self.floor) + u"-----------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def setFileTitle(self, title):
        # 如果标题不是为None，即成功获取到标题
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")
baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL, 1)
#bdtb.getPage(1)
title=bdtb.getTitle()
bdtb.setFileTitle(title)
contents=bdtb.getContent()
content=contents[1]
print(content)
bdtb.writeData(contents)
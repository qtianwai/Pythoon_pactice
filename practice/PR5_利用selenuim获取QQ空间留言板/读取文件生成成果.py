import re

import pymysql

__author__ = 'xzy'

def saveInMysql(obj):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "admin", "pythontest", charset='utf8')
    cursor = db.cursor()
    try:
        sql="select * from t_hy_qq_liuyan where st_date='%s'" %obj['date']
        cursor.execute(sql)
        rs = cursor.fetchall()
        if len(rs) == 0:
            effect_row = cursor.executemany("insert into t_hy_qq_liuyan(nm_qqid,st_qqname,st_content,st_date)values(%s,%s,%s,%s)",
                                            [(obj['qqId'], obj['qqName'], str(obj['content']),obj['date'])])
            db.commit()
    finally:
        cursor.close()
        db.close()


def start():
    content=open('留言板内容.txt','r',encoding="utf-8").read()
    Regex1=re.compile(r'<li id="pLi_.*?" class="bor3">(.*?)</div></li>')  #截取每一个留言框,这里是贪心模式，所有都匹配到ul了，但也没太大关系
    qqId=Regex1.findall(content)
    commentList=[]
    for liuyan in qqId:
        #liuyan=text[0]
        Regex2=re.compile(r'user_name_info_(\d+)')   #获取留言QQ号
        Regex3 = re.compile(r'<a name="link_\d+" href="http://user.qzone.qq.com/\d+".*?class="c_tx q_namecard".*?>(.*?)</a>') #获取留言QQ名
        Regex4=re.compile(r'<div id="commentContentDiv_\d+".*?<td>(.*?)</td>')
        Regex5=re.compile((r'<p class="reply_wrap"><span class="c_tx3 mode_post">(.*?)</span>'))
        comment={}
        comment['qqId']=Regex2.search(liuyan).group(1)
        comment['qqName'] = Regex3.search(liuyan).group(1)
        comment['content'] = Regex4.search(liuyan).group(1)
        comment['date'] = Regex5.search(liuyan).group(1)
        commentList.append(comment)
    return commentList


commentList=start()
for obj in commentList:
    saveInMysql(obj)
print("程序结束")








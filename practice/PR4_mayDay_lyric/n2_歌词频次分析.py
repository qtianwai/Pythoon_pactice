import jieba
import pymysql
from xlwt import Workbook


def getSonges(songlist):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "admin", "pythontest", charset='utf8')
    cursor = db.cursor()
    try:
        sql = "select * from t_hy_song_i "
        cursor.execute(sql)
        rs = cursor.fetchall()
        for song in rs:
            lyric=song[1]+'\n'+song[2]
            songlist.append(lyric)
    finally:
        cursor.close()
        db.close()
        return songlist

def write(fpath,songlist):
    try:
        f=open(fpath, 'w', encoding='utf-8')
        for lyric in songlist:
            f.write(lyric+'\n\n')
    finally:
        f.close()


def analysy(fpath):
    file = open(fpath, 'r',encoding='utf-8')
    lyric_str = file.read()
    seg = jieba.cut(lyric_str)  # jieba分词
    word_list = []
    word_dict = {}
    for each in seg:
        # print(each+' ')
        if len(each) > 1:  # 过滤长度为1的词
            word_list.append(each)  # 加入到词语列表中

    for index in word_list:  # 遍历词语列表
        if index in word_dict:
            word_dict[index] += 1  # 根据字典键访问键值，如果该键在字典中，则其值+1
        else:
            word_dict[index] = 1  # 如果键不在字典中，则设置其键值为1

    sorted(word_dict.items(), key=lambda e: e[1], reverse=False)

    fc = open("fenci.txt", 'w')
    for item in word_dict.items():
        print(item)
        fc.write(item[0] + str(item[1]) + '\n')  # 将分词词频输出到txt文本中

    # 将分词和词频输出到excel中
    file = Workbook()
    table = file.add_sheet('data')

    ldata = []
    num = [a for a in word_dict]
    num.sort()

    for item in num:  # 频次
        ldata.append(str(word_dict[item]))  # 次数

    for i in range(1000):
        table.write(i, 0, num[i])
        table.write(i, 1, ldata[i])
    file.save("歌词频率统计.xls")
#main
songlist=[]
songlist=getSonges(songlist)#从数据库中获取所有歌曲名+歌词
fpath='五月天歌词.txt'
write(fpath,songlist)#将所有歌词写到同一个txt# 文件
analysy(fpath)#对歌词进行分析
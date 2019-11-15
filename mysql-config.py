#-*- encoding:utf-8 -*-
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "admin", "pythontest",charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
effect_row = cursor.executemany("insert into t_hy_song_i(st_title,st_lyric,st_url)values(%s,%s,%s)", [("222","飒飒大神","11sad113")])
db.commit()
cursor.close()


# 关闭数据库连接
db.close()
#!/usr/bin/env pytho
# -*- coding:utf-8 -*-
import pymysql

# 创建连接
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='admin', db='tmall', charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# 创建游标
cursor.execute("select * from t_HY_theme_I")

# 获取剩余结果的第一行数据
row_1 = cursor.fetchone()
print (row_1)
# 获取剩余结果前n行数据
# row_2 = cursor.fetchmany(3)

# 获取剩余结果所有数据
# row_3 = cursor.fetchall()

conn.commit()
cursor.close()
conn.close()
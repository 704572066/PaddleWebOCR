#!/usr/bin/python 
# -*- coding: UTF-8 -*-

import MySQLdb
import sys

def save2db(vin, img1, img2, text, language):
    try:
        # 读取图片文件
        # fp = open("./test.jpg")
        # img = fp.read()
        # mysql连接
        conn = MySQLdb.connect(host='192.168.11.102', port=20534, user='root', passwd='Zju2023@', db='test', charset="utf8")
        cursor = conn.cursor()
        # 注意使用Binary()函数来指定存储的是二进制
        # cursor.execute("INSERT INTO ford values(%s,%s,%s,%s)" % (vin,img1,img2,text))

        sql = "insert into ford(vin,img1,img2,text,lang) values(%s,%s,%s,%s,%s)"

        # cursor.execute(sql)

        cursor.execute(sql, (vin, img1, img2, text, language))
        # 如果数据库没有设置自动提交，这里要提交一下
        conn.commit()
        cursor.close()
        # 关闭数据库连接
        conn.close()
    except Exception as r:
        print('未知错误 %s' %r)


def get_imgs(vin):
    try:
        # 读取图片文件
        # fp = open("./test.jpg")
        # img = fp.read()
        # mysql连接
        conn = MySQLdb.connect(host='192.168.11.102', port=20534, user='root', passwd='Zju2023@', db='test', charset="utf8")
        cursor = conn.cursor()
        # 注意使用Binary()函数来指定存储的是二进制
        # cursor.execute("INSERT INTO ford values(%s,%s,%s,%s)" % (vin,img1,img2,text))

        sql = "select id,img1,img2,text,confidence,direction,lang,model,percentage from ford where vin = %s"

        # cursor.execute(sql)

        cursor.execute(sql, (vin,))
        # 如果数据库没有设置自动提交，这里要提交一下
        # 获取所有记录列表
        results = cursor.fetchall()
        # conn.commit()
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return results
    except Exception as r:
        print('未知错误 %s' %r)



def get_texts(id):
    try:
        # 读取图片文件
        # fp = open("./test.jpg")
        # img = fp.read()
        # mysql连接
        conn = MySQLdb.connect(host='192.168.11.102', port=20534, user='root', passwd='Zju2023@', db='test', charset="utf8")
        cursor = conn.cursor()
        # 注意使用Binary()函数来指定存储的是二进制
        # cursor.execute("INSERT INTO ford values(%s,%s,%s,%s)" % (vin,img1,img2,text))

        sql = "select text,confidence,direction,lang,model,percentage from ford where id = %s"

        # cursor.execute(sql)
        # value = (id,id)

        cursor.execute(sql, (id,))
        # 如果数据库没有设置自动提交，这里要提交一下
        # 获取所有记录列表
        result = cursor.fetchone()

        # conn.commit()
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return result
    except Exception as r:
        print('未知错误 %s' %r)

# get_texts(3)
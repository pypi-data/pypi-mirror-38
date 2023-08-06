#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/3 上午10:58
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : vendor
# @File    : app_music
# @Contact : guangze.yu@foxmail.com
"""

# aiting API config
import pymysql
conn = pymysql
db = pymysql.connect(host="rm-uf6lp85qe22m65cu6oo.mysql.rds.aliyuncs.com",
                     user="root",
                     password="Root1q2w",
                     db="db_voice",
                     port=3306)
cur = db.cursor()
query = "select * from serverhost;"
cur.execute(query)
results = cur.fetchall()[0]


# API token config
local_token_url = 'http://localhost:8000/gettoken'
remote_token_url = '%s/gettoken' % results[0]

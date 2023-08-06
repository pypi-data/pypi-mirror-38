#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-21 下午8:37
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : config
# @Contact : guangze.yu@foxmail.com
"""

########SQL DateBase config###############
sql = 'mysql'
tools = 'pymysql'
usr = 'root'
password = 'Root1q2w'
host = 'rm-uf6lp85qe22m65cu6oo.mysql.rds.aliyuncs.com:3306'
db_name = 'db_voice'
sqlconfig = '%s+%s://%s:%s@%s/%s?charset=utf8' %(sql,tools,usr,password,host,db_name)


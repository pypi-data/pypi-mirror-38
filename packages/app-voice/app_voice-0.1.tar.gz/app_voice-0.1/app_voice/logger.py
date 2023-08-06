#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-26 下午10:26
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : logger
# @Contact : guangze.yu@foxmail.com
"""
import logging
import sys

def get_logger(log_name):
    logger = logging.getLogger(log_name)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    file_handler = logging.FileHandler("./log/%s.log"%log_name)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger



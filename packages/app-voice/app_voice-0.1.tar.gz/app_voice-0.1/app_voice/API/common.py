#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-27 上午11:39
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : common
# @Contact : guangze.yu@foxmail.com
"""
import requests
import base64
import time
import random
import string
import hashlib
import json
import hmac
import redis

app_key = '7809fdad2a6c299d8d13b0a232e15350'
app_secret = 'a1bfc4d4a0e1bb5c51ca097f6bd28c51'
pack_id = 'com.ximalaya.ting.android.car.shangqichengyongche'
bundle_id = 'com.ximalaya.ting.android.car.shangqichengyongche'
device_id = 'E4B3185B0932'

pool = redis.ConnectionPool(host='127.0.0.1', password='Root1q2w', port=6379)
cache = redis.Redis(connection_pool=pool)
def signature(param):
    msg = ''
    param_sorted = {i: str(param[i]) for i in sorted(param.keys())}
    for i in param_sorted:
        msg += '&'+i+'='+param_sorted[i]
    msg_byte = bytes(msg[1:],'utf-8')
    msg_base64 = bytes(base64.encodebytes(msg_byte).decode('utf-8').replace('\n',''),'utf-8')
    key = bytes(app_secret, 'utf-8')
    msg_hmac_sha1 = hmac.new(key, msg_base64, hashlib.sha1).digest()
    sig = hashlib.md5(msg_hmac_sha1).hexdigest()
    return sig

class Oauth2(object):
    def __init__(self):
        self.app_key = app_key
        self.device_id = device_id
        self.grant_type = 'client_credentials'
        self.nonce = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.timestamp = str(int(time.time()*1000))
        self.url = 'http://api.ximalaya.com/oauth2/secure_access_token'
        self.access_token = self.login()

    def login(self):
        headers = {'ContentType':'application/x-www-form-urlencoded'}
        param = {'client_id':self.app_key, 'device_id':self.device_id,'grant_type': self.grant_type, 'nonce':self.nonce,
                 'timestamp':self.timestamp}
        sig = signature(param)
        param['sig'] = sig
        access = requests.post(self.url,headers=headers, data=param)
        text = json.loads(access.content.decode('utf-8'))
        access_token = text['access_token']
        expires_time = text['expires_in']
        cache.set('ximalaya_token',access_token,expires_time)
        return access_token

def get_token():
    token = cache.get('ximalaya_token')
    if token is None:
        token = Oauth2().login()
    else:
        token = token.decode('utf-8')
    return token

class Common(object):
    def __init__(self):
        self._access_token = get_token()
        self._client_os_type = '3'
        self._app_key = app_key
        self._device_id = device_id
        self._pack_id = pack_id
        self._param_public = {'access_token':self._access_token, 'app_key':self._app_key, 'client_os_type':
            self._client_os_type, 'device_id':self._device_id,'pack_id':self._pack_id}
        self._param_private = {}
        self._url = 'http://api.ximalaya.com'

    def get(self):
        param = self._param_public.copy()
        param.update(self._param_private)
        sig = signature(param)
        param['sig'] = sig
        res = requests.get(self._url, param)
        return json.loads(res.content.decode('utf-8'))

    def update(self, param_dict):
        self._param_private = param_dict
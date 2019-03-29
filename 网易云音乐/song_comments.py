# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 13:44:16 2019

@author: http://www.lizenghai.com
"""

from Crypto.Cipher import AES
import base64
import requests
import json


class SongComments:
    '''
        获取指定歌曲id下的总评论数和热门评论（包含评论人的用户信息）
        发布地址：http://www.lizenghai.com
    '''
    headers = {'Host': 'music.163.com',
 'Connection': 'keep-alive',
 'Content-Length': '474',
 'Origin': 'https://music.163.com',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
 'DNT': '1',
 'Content-Type': 'application/x-www-form-urlencoded',
 'Accept': '*/*',
 'Accept-Encoding': 'gzip, deflate, br',
 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    
    first_param = '{rid: "", offset: "20", total: "true", limit: "20", csrf_token: ""}'
    second_param = "010001"
    third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    forth_param = "0CoJUm6Qyw8W8jud"
    def __init__(self, song_id):
        self.song_id = song_id
        
        
    def AES_encrypt(self, text, key, iv):
        pad = 16 - len(text) % 16
        if isinstance(text, (str)):
            text = text.encode('utf-8')
        text = text + (pad * chr(pad)).encode('utf-8')
        iv = iv.encode('utf-8')
        if isinstance(key, (str)):
            key = key.encode('utf-8')
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    def build_params(self, first_param, forth_param):
        iv = "0102030405060708"
        first_key = forth_param
        second_key = 16 * 'F'
        h_encText = self.AES_encrypt(first_param, first_key, iv)
        h_encText = self.AES_encrypt(h_encText, second_key, iv)
        return h_encText

    def post_html(self, url, postdata):
        response = requests.post(url, headers=self.headers, data=postdata, timeout=5)
        return response.content.decode()
    
    def clear_json_data(self, json_dict):
        
        for i in range(len(json_dict['hotComments'])):
            for k in ['userId', 'nickname', 'userType', 'vipType', 'authStatus', 'avatarUrl']:
                json_dict['hotComments'][i][k] = json_dict['hotComments'][i]['user'][k]
            json_dict['hotComments'][i].pop('user')
            json_dict['hotComments'][i].pop('beReplied')
            json_dict['hotComments'][i].pop('decoration')
        return json_dict
    def run(self):

        url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(self.song_id)
        first_param = '{rid: "", offset: "", total: "true", limit: "20", csrf_token: ""}'
        params = self.build_params(first_param, self.forth_param)
        postdata = {'params':params,
                    'encSecKey':self.encSecKey}
        json_text = self.post_html(url, postdata)
        json_dict = json.loads(json_text)
        json_dict = self.clear_json_data(json_dict)
        hot_comments = json_dict['hotComments']
        total_comments_num = json_dict['total']
        return total_comments_num, hot_comments

if __name__ == '__main__':
    sc = SongComments(1293886117)
    total_comments_num, hot_comments = sc.run()
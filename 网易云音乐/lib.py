# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:24:57 2019

@author: http://www.lizenghai.com
"""


import requests, os, time
from pyquery import PyQuery as pq


def get_html(url):
    headers_play = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
     'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
     'Cache-Control': 'no-cache',
     'Connection': 'keep-alive',
     'DNT': '1',
     'Host': 'music.163.com',
     'Pragma': 'no-cache',
     'Upgrade-Insecure-Requests': '1',
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    response = requests.get(url, headers=headers_play)
    content = response.content.decode()
    return content

def get_total_page():
    #% 获取歌单总页数
    baseurl = 'http://music.163.com/discover/playlist/'
    content = get_html(baseurl)
    doc = pq(content)
    page_area = doc('a.zpgi')
    total_page_num = int(page_area.eq(-1).text())
    print('总页码：',total_page_num)
    return total_page_num

def get_page_playlist_id(webcontent):
    #% 获取歌单列表页歌单id
    doc = pq(webcontent)
    playlist_area = doc('a.tit.f-thide.s-fc0')
    #print(len(playlist_area))
    playlist_ids = [x.attr('href').split('?id=')[-1] for x in playlist_area.items()]
    #print(playlist_ids)
    return playlist_ids

def get_all_song_id(playlist_id):
    #% 获取歌单里的歌曲id
    one_playlist_url = 'https://music.163.com/playlist?id={}'.format(playlist_id)
    content = get_html(one_playlist_url)
    doc = pq(content)
    songid_area = doc('div#song-list-pre-cache ul.f-hide a')
    #print(len(songid_area))
    all_song_ids = [x.attr('href').split('?id=')[-1] for x in songid_area.items()]
    #print(all_song_ids)
    return all_song_ids

def get_song_info(song_id):
    #% 获取歌曲的信息
    song_url = 'https://music.163.com/song?id={}'.format(song_id)
    content = get_html(song_url)
    doc = pq(content)
    song_info = {}
    meta = doc('meta')
    for x in meta.items():
        if x.attr.name == 'description':
            description = x.attr.content
            #print(description)
            song_info['description'] = description.split('所属专辑：')[-1] if '所属专辑：' in description else ''
    #print(doc('title').text())
    x = doc('title').text().split(' - ')
    if len(x) >= 3:
        name, singer, *_ = x
    else:
        return None
    song_info['singer'] = singer
    song_info['song_name'] = name
    #print(song_info)    
    return song_info

def get_all_playlist_id():
    # 获得所有歌单id
    fpath = 'all_playlist_id'
    if os.path.exists(fpath):
        with open(fpath, 'r') as f:
            all_playlist_id = f.read()
            all_playlist_id = all_playlist_id.split('\n')
    else:
        all_playlist_id = []
    totalnum = get_total_page()
    for i in range(totalnum):
        url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}'.format(i*35)
        content = get_html(url)
        tmp = get_page_playlist_id(content)
        all_playlist_id.extend(tmp)
        time.sleep(1)
    all_playlist_id = list(set(all_playlist_id))  # 去重
    with open(fpath, 'w') as f:
        f.writelines('\n'.join(all_playlist_id))
    return all_playlist_id
        

if __name__ == '__main__':
    pass
        
    
    
    
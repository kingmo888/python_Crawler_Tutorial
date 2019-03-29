# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:24:41 2019

@author: http://www.lizenghai.com
"""

import time, os, json
from lib import *
from song_comments import SongComments

def down_all_song_id():
    totalnum = get_total_page()
    all_playlist_id = get_all_playlist_id()
    path_playlist_visited = 'playlist_visited'
    path_sond_id = 'all_sond_id'
    if os.path.exists(path_playlist_visited):
        with open(path_playlist_visited, 'r') as f:
            playlist_visited = f.read()
            playlist_visited =  playlist_visited.split('\n')
    else:
        playlist_visited = []
    
    all_playlist_id = [x for x in all_playlist_id if x not in playlist_visited]
    all_sond_id = []
    if os.path.exists('all_sond_id'):
        with open('all_sond_id', 'r') as f:
            all_song_id = f.read()
            all_song_id = all_song_id.split('\n')
    alen = len(all_playlist_id)
    for i, playlist_id in enumerate(all_playlist_id):
        print(i+1)
        time.sleep(0.5)
        tmp = get_all_song_id(playlist_id)
        
        all_sond_id.extend(tmp)
        playlist_visited.append(playlist_id)
        
        
        if (i !=0 and i % 50 == 0) or i == alen -1:
            with open(path_playlist_visited, 'w') as f:
                f.writelines('\n'.join(playlist_visited))
                
            all_sond_id = list(set(all_sond_id))
            with open(path_sond_id, 'w') as f:
                f.writelines('\n'.join(all_sond_id))


def down_song_allinfo(song_id):
    song_info = get_song_info(song_id)
    if song_info is None:
        return
    total, comments = SongComments(song_id).run()
    song_info['total'] = total
    song_info['comments'] = comments
    with open('tmp\{}.json'.format(song_id), 'w') as f:
        json.dump(song_info, f)

def test1():
    with open('all_sond_id', 'r') as f:
        all_song_id = f.read()
        all_song_id = all_song_id.split('\n')
    for song_id in all_song_id:
        if os.path.exists('tmp\{}.json'.format(song_id)):

            continue
        down_song_allinfo(song_id)
        time.sleep(0.01)
        
def test2():
    from multiprocessing.dummy import Pool as ThreadPool
    with open('all_sond_id', 'r') as f:
        all_song_id = f.read()
        all_song_id = all_song_id.split('\n')
    pool = ThreadPool(20)
    hasdown = []
    for song_id in all_song_id:
        if os.path.exists('tmp\{}.json'.format(song_id)):
            hasdown.append(song_id)
    all_song_id = [x for x in all_song_id if x not in hasdown]
    pool.map(down_song_allinfo, all_song_id)

if __name__ == '__main__':
    down_all_song_id()
    test2()
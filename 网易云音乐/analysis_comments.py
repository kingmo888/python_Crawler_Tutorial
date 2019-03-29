# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:24:41 2019

@author: http://www.lizenghai.com
"""


import os, json, copy
from lib import *
from song_comments import SongComments
import pandas as pd
import matplotlib.pyplot as plt
import wordcloud # 词云展示库
import collections
import numpy as np
from PIL import Image # 图像处理库
def set_ch():
    # 使python绘图支持中文
	from pylab import mpl
	mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
	mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
set_ch()
#%%
def deal_song_data(sdict):
    comm = pd.DataFrame(sdict['comments'])
    comm['description'] = sdict['description']
    comm['singer'] = sdict['singer']
    comm['song_name'] = sdict['song_name']
    comm['total'] = sdict['total']
    return comm

with open('all_sond_id', 'r') as f:
    all_song_id = f.read()
    all_song_id = all_song_id.split('\n')
    
all_json = []
song_infos = {}
for i,song_id in enumerate(all_song_id):
    if i % 100 == 0:
        print(i)
    jpath = 'tmp\{}.json'.format(song_id)
    if os.path.exists(jpath):
        with open(jpath, 'r') as f:
            tmp = json.load(f)
            all_json.append(tmp)
        
        tmp2 = copy.copy(tmp)
        tmp2.pop('comments')
        song_infos[song_id] = tmp2
            

all_data = list(map(deal_song_data, all_json))
all_data2 = pd.concat(all_data)

song_infos = pd.DataFrame(song_infos).T


#%% 对评论总数进行排序

song_infos = song_infos.sort_values('total', ascending=False)
# 统计评论过万的歌曲数量
sub_song_infos = song_infos[song_infos['total']>=10000]
print('歌曲评论过万数量有{}首'.format(len(sub_song_infos)))
# 把评论过万歌曲输出到txt文件中
with open('评论过万歌曲列表.txt', 'w', encoding='utf-8') as f:
    for i in range(len(sub_song_infos)):
        line = sub_song_infos.iloc[i]
        mystr = '{}-->      {} {}\n'.format(str(line['total']).ljust(10, ' '), line['song_name'],line['singer'])
        f.writelines(mystr)
    
#%% 绘图：评论数top20的歌曲
        
fig_data = song_infos.head(20)
fig_data = fig_data.set_index('song_name')
fig = plt.figure(figsize=(14,10))
fig.suptitle('评论数top20的歌曲')
new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf']
ax1 = fig.add_subplot(1,1,1)
ax1.bar(range(len(fig_data)),fig_data['total'].values, tick_label=fig_data.index, color=new_colors)
#xticks=list(range(0,len(line),int(len(line)/30)))  # 显示30个labels
#ax1.set_xticks(xticks.index.tolist())
for tick in ax1.get_xticklabels():
    tick.set_rotation(90)
ax1.set_xlabel('歌名')
ax1.set_ylabel('评论数量')
fig.show()
fig.savefig('output\\评论数top20的歌曲.jpg')

#%% 按照歌手统计每个歌手的所有歌曲评论总数
total_comm_by_singer = song_infos[['singer', 'total']].groupby('singer').sum()
total_comm_by_singer = total_comm_by_singer.sort_values('total', ascending=False)

#%%
fig_data = total_comm_by_singer.head(20)
fig = plt.figure(figsize=(14,10))
fig.suptitle('歌手所有歌曲总评论数top20')
new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf']
ax1 = fig.add_subplot(1,1,1)
ax1.bar(range(len(fig_data)),fig_data['total'].values, tick_label=fig_data.index, color=new_colors)
#xticks=list(range(0,len(line),int(len(line)/30)))  # 显示30个labels
#ax1.set_xticks(xticks.index.tolist())
for tick in ax1.get_xticklabels():
    tick.set_rotation(90)
ax1.set_xlabel('歌手')
ax1.set_ylabel('评论数量')
fig.show()
fig.savefig('output\\歌手所有歌曲总评论数top20.jpg')

#%% 对所有歌手按照评论数量为热度制作词云
word_counts = total_comm_by_singer['total'].to_dict()

mask = np.array(Image.open('timg.jpg')) # 定义词频背景
wc = wordcloud.WordCloud(
    font_path='C:/Windows/Fonts/simhei.ttf', # 设置字体格式
    mask=mask, # 设置背景图
    max_words=200, # 最多显示词数
    max_font_size=100 # 字体最大值
)
wc.generate_from_frequencies(word_counts) # 从字典生成词云
image_colors = wordcloud.ImageColorGenerator(mask) # 从背景图建立颜色方案
wc.recolor(color_func=image_colors) # 将词云颜色设置为背景图方案
#plt.imshow(wc) # 显示词云
##plt.axis('off') # 关闭坐标轴
#plt.show() # 显示图像
wc.to_file("output\\所有歌手按照评论数量为热度制作词云.png")
#%% 歌曲中，产量最大前20 是？
total_songnum_by_singer = song_infos.groupby('singer').count()
total_songnum_by_singer = total_songnum_by_singer.sort_values('total', ascending=False)

#%%
fig_data = total_songnum_by_singer.head(20)
fig_data = fig_data['total']
fig = plt.figure(figsize=(14,10))
fig.suptitle('歌手歌曲数量排行top20')
new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf']
ax1 = fig.add_subplot(1,1,1)
ax1.bar(range(len(fig_data)),fig_data.values, tick_label=fig_data.index, color=new_colors)
#xticks=list(range(0,len(line),int(len(line)/30)))  # 显示30个labels
#ax1.set_xticks(xticks.index.tolist())
for tick in ax1.get_xticklabels():
    tick.set_rotation(90)
ax1.set_xlabel('歌手')
ax1.set_ylabel('歌曲数量')
fig.show()
fig.savefig('output\\歌手歌曲数量排行top20.jpg')

#%% 对所有歌手按照歌曲数量为热度制作词云

word_counts =  total_songnum_by_singer['total'].to_dict()
wc = wordcloud.WordCloud(
    font_path='C:/Windows/Fonts/simhei.ttf', # 设置字体格式
    #mask=mask, # 设置背景图
    background_color="white", #背景颜色
    max_words=200, # 最多显示词数
    max_font_size=100, # 字体最大值
    width=400,  #图幅宽度
    height=400
)
wc.generate_from_frequencies(word_counts) # 从字典生成词云
#wc.generate(word_counts)
wc.to_file("output\\所有歌手按照歌曲数量为热度制作词云.png")


#%% 去掉宝宝巴士、英语
tmp = total_songnum_by_singer['total'].to_dict()
tmp.pop('宝宝巴士')
tmp.pop('英语听力')
tmp.pop('群星')
word_counts = tmp
wc = wordcloud.WordCloud(
    font_path='C:/Windows/Fonts/simhei.ttf', # 设置字体格式
    #mask=mask, # 设置背景图
    background_color="white", #背景颜色
    max_words=200, # 最多显示词数
    max_font_size=100, # 字体最大值
    width=400,  #图幅宽度
    height=400
)
wc.generate_from_frequencies(word_counts) # 从字典生成词云
#wc.generate(word_counts)
wc.to_file("output\\所有歌手按照歌曲数量为热度制作词云（去巴士、英语、群星）.png")
#%% 对所有评论分词后制作词云
# 分词步骤比较耗时
import jieba

# 把所有评论以段落形式拼接
alltext = '\n'.join(all_data2['content'].tolist())
#segs=jieba.cut(alltext)
# 文本分词
seg_list_exact = jieba.cut(alltext, cut_all = False) # 精确模式分词
seg_list_exact2 = list(seg_list_exact)
#%%
object_list = []
with open('myStopWords.txt', 'r') as f:
    stopwords = f.read()
stopwords = stopwords.split('\n')   
for word in seg_list_exact2: # 循环读出每个分词
    if word not in stopwords: # 如果不在去除词库中
        object_list.append(word) # 分词追加到列表
#%%
word_counts = collections.Counter(object_list) # 对分词做词频统计


wc = wordcloud.WordCloud(
    font_path='C:/Windows/Fonts/simhei.ttf', # 设置字体格式
    #mask=mask, # 设置背景图
    background_color="white", #背景颜色
    max_words=200, # 最多显示词数
    max_font_size=100, # 字体最大值
    width=400,  #图幅宽度
    height=400
)
wc.generate_from_frequencies(word_counts) # 从字典生成词云
#wc.generate(word_counts)
wc.to_file("output\\所有评论词云.png")
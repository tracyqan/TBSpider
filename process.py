#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: tracyqan time:2018/12/19

import pandas as pd
import pyecharts
from wordcloud import WordCloud
import jieba
import re
import matplotlib.pyplot as plt



def make_cloud(data):
    print('开始绘制商品信息词云')
    name = ''.join(list(data['name']))
    word = re.sub(r'&lt;spanclass=H&gt;|&lt;/span&gt;', '', name)
    words = ' '.join(jieba.cut(word))
    w = WordCloud(
        font_path= 'simhei.ttf',
        width=800,
        height=400,
        mask=plt.imread('mask.jpg')
    )
    w.generate(words)
    filename = 'wordcloud.png'
    w.to_file(filename)
    print('图表已保存至{}'.format(filename))

def create_bar(data):
    """
    绘制价格与出售数量的关系图
    """
    print('开始绘制价格与出售数量的关系图')
    # 1元以下的销售量
    count_1 = data[data['price']<=1]['saleCount'].sum()
    # 1元-3元的销售量
    count_2 = data[(data['price']>1) & (data['price']<=3)]['saleCount'].sum()
    # 3元-5元的销售量
    count_3 = data[(data['price'] > 3) & (data['price'] <= 5)]['saleCount'].sum()
    # 5元-7元的销售量
    count_4 = data[(data['price'] > 5) & (data['price'] <= 7)]['saleCount'].sum()
    # 7元-9元的销售量
    count_5 = data[(data['price'] > 7) & (data['price'] <= 9)]['saleCount'].sum()
    # 9元-12元的销售量
    count_6 = data[(data['price'] > 9) & (data['price'] <= 12)]['saleCount'].sum()
    # 12元-15元的销售量
    count_7 = data[(data['price'] > 12) & (data['price'] <= 15)]['saleCount'].sum()
    # 15元以上的销售量
    count_8 = data[data['price'] > 15]['saleCount'].sum()
    title = '圣诞商品价格与出售数量的关系图'
    x = ['1元以下', '1元-3元', '3元-5元', '5元-7元', '7元-9元', '9元-12元', '12元-15元', '15元以上']
    y = [count_1, count_2, count_3, count_4, count_5, count_6, count_7, count_8]
    bar = pyecharts.Bar()
    bar.add(title, x, y, mark_point=['max', 'min', 'average'])
    bar.render(title+'.html')
    print('图表已保存至{}.html'.format(title))

def make_bar(data):
    """
    绘制折扣与出售数量的关系图
    """
    print('开始绘制折扣与出售数量的关系图')
    discount = [x/y if y!=0 else 0 for x,y in zip(data['realPrice'], data['price'] )]
    data['discount'] = discount
    # 打不折销售量
    count_1 = data[data['discount'] == 0]['saleCount'].sum()
    # 0-2折销售量
    count_2 = data[(data['discount'] > 0) & (data['discount'] <= 0.2)]['saleCount'].sum()
    # 2-4折销售量
    count_3 = data[(data['discount'] > 0.2) & (data['discount'] <= 0.4)]['saleCount'].sum()
    # 4-6折销售量
    count_4 = data[(data['discount'] > 0.4) & (data['discount'] <= 0.6)]['saleCount'].sum()
    # 6-8折销售量
    count_5 = data[(data['discount'] > 0.6) & (data['discount'] <= 0.8)]['saleCount'].sum()
    # 8折以上销售量
    count_6 = data[data['discount'] > 0.8]['saleCount'].sum()
    title = '圣诞商品折扣与出售数量的关系图'
    x = ['打不折', '0-2折', '2-4折', '4-6折', '6-8折', '8折以']
    y = [count_1, count_2, count_3, count_4, count_5, count_6]
    bar = pyecharts.Bar()
    bar.add(title, x, y, mark_point=['max', 'min', 'average'])
    bar.render(title+'.html')
    print('图表已保存至{}.html'.format(title))

def create_map(data):
    print('开始绘制全国销售量示例图')
    countrys = [x.split(' ')[0] for x in data['place']]
    data['countrys'] = countrys
    countrys_set = list(set(countrys))
    values = []
    title = '全国销售量示例图'
    for i in countrys_set:
        values.append(data[data['countrys'] == i]['saleCount'].sum())
    map = pyecharts.Map(title, width=800, height=400)
    map.add('', countrys_set, values, maptype='china', is_visualmap=True, visual_text_color="#000")
    map.render(title+'.html')
    print('图表已保存至{}.html'.format(title))

def main():
    filename = 'goods.csv'
    data = pd.read_csv(filename)
    make_cloud(data)
    #create_bar(data)
    #make_bar(data)
    #create_map(data)

if __name__ == '__main__':
    main()
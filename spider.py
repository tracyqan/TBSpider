#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: tracyqan time:2018/12/19

import requests
import pandas as pd
import time


def get_info(pages, key):
    url = 'https://ai.taobao.com/search/getItem.htm?'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    datas = []
    for page in range(1, (2*pages)+1):
        # try:
        param = {
            'page': page,
            'key': key,
            'pageNav': 'true'
        }
        res = requests.get(url, params=param, headers=headers)
        res.raise_for_status()
        res.encoding = 'utf-8'
        print(res.url)
        res = res.json()
        # 淘宝奇数页偶数页的json格式不一样，奇数页商品信息在2个列表中储存
        for i in res['result']['auction']:
            data_1 = {}
            data_1['name'] = i.get('description', '').replace(' ', '')
            data_1['place'] = i.get('itemLocation', '')
            data_1['price'] = i.get('price', 0)
            data_1['realPrice'] = i.get('realPrice', 0)
            data_1['saleCount'] = i.get('saleCount', 0)
            datas.append(data_1)
        # if page % 2 == 1:
        #
        #     for k in res['result']['p4ptop']:
        #         data_2 = {}
        #         data_2['name'] = k.get('title', '').replace(' ', '')
        #         data_2['place'] = k.get('location', '')
        #         # json数据中该列表中价格是以分为单位的 乘0.01转为以元为单位
        #         data_2['price'] = k.get('goodsPrice', 0)
        #         data_2['realPrice'] = k.get('salePrice', 0)
        #         data_2['saleCount'] = k.get('sell', 0)
        #         datas.append(data_2)
        print('the goods of page<{}> had crawled'.format(page))
        time.sleep(2)
        # except Exception as e:
        #     print(e)
    return datas

def save_data(datas, filename):
    df = pd.DataFrame(datas)
    df.to_csv(filename, encoding='utf-8')
    print('已保存至文档')

def get_data():
    key = '圣诞帽'
    page = 20
    datas = get_info(page, key)
    filename = 'goods.csv'
    if datas:
        save_data(datas, filename)


if __name__ == '__main__':
    get_data()
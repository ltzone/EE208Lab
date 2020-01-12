# -*- coding: utf-8 -*-
import math
from threading import Thread
import queue
import json
import os , sys
#导入requests库(请求和页面抓取)
import requests
#导入time库(设置抓取Sleep时间)
import time
#导入random库(生成乱序随机数)
import random
#导入正则库(从页面代码中提取信息)
import re
#导入数值计算库(常规计算)
import numpy as np
from PIL import Image
from wordcloud import WordCloud
#导入科学计算库(拼表及各种分析汇总)
import pandas as pd
#导入绘制图表库(数据可视化)
import matplotlib.pyplot as plt
#导入结巴分词库(分词)
import jieba as jb
#导入结巴分词(关键词提取)
import jieba.analyse

f=open("index_sn_part4.txt", 'r')

#设置请求中头文件的信息
headers = {'User-Agent':'Mozilla/5.0 '
                        '(Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML,'
                        ' like Gecko) Chrome/76.0.3809.132 '
                        'Safari/537.36'}

q = queue.Queue()
NUM = 5
JOBS = 10
#cookies=***
def crawl_sn_cmt_tag(sku, shop):# change for url
#https://review.suning.com/ajax/review_count/cluster-32762695-
# 000000011373116603-0000000000-----satisfy.htm?callback=satisfy
    url=r"https://review.suning.com/ajax/" \
        r"review_count/cluster-32762695-0000000" \
        r"{}-{}" \
        r"-----satisfy.htm?".format(sku,shop)
    comment_tag_path = r'C:\TC-prog\JetBrain_pycharm_TC' \
                       r'\PycharmProjects\Crawler_EEFinal' \
                       r'\sn_cmt_SCORE\httpproduct.suning.com{}{}.html.txt'.format(sku,shop)

    try:
        r=requests.get(url,headers=headers,timeout=5)
        r.raise_for_status()
    except:
        print ('爬取失败')

    raw = r.text[:]
    pos = 0
    for i in range(len(raw)):
        if raw[i] == '(':
            pos = i


    try:
        # data0 = re.sub(u'^fetchJSON_comment98vv106813\(', '', html)
        r_json_str = r.text[pos + 1:-1]
        # print (r_json_str)
        r_json_obj = json.loads(r_json_str, strict=False)  # 转成python对象
        print(r_json_obj)
        r_json_dict = r_json_obj['reviewCounts'][0]  # 好评中评差评等的统计
        # print ('苏宁评论标签：')
        # 追加模式，逐行写入
        if not os.path.exists(comment_tag_path):
            with open(comment_tag_path, 'a+') as file:
                sumcnt = int(r_json_dict['totalCount'])
                good = int(r_json_dict['fiveStarCount'])  # 好评数
                # gen =r_json_dict['fourStarCount'] # 中评数
                # poor=r_json_dict['oneStarCount'] # 差评
                after = int(r_json_dict['againCount'])
                # print(good, sumcmt, after)
                # print(good/sumcmt)
                score = int((1.0 * good / sumcnt * 0.8)*100+math.log(sumcnt,10)* 7)

                file.write("httpproduct.suning.com" + shop + sku + ".html" + '\t' + str(score) + '\n')
                print(shop + sku + '\t' + str(score))
    except:
        print('large json')


def run():
    global f
    for line in f.readlines():
        try:
            pp = line.split('\t')
            webpage = pp[1].strip('\n')
            print(webpage)
            temp = webpage[16:-9]
            if (len(webpage) > 60):
                continue
            pos = 0
            for i in range(len(temp)):
                if temp[i] == 'm':
                    pos = i
            itemID = temp[pos + 1:]
            # print(itemID)
            # print(type(itemID))
            #if (len(itemID) != 21): continue
            shop = itemID[:-11]
            sku = itemID[10:]
            print(shop, sku)

            crawl_sn_cmt_tag(sku, shop)
            time.sleep(random.random() * 2)
        except:
            print("Invalid Input!")


def working():
    while True:
        #arguments = q.get()
        run()
        q.task_done()


#fork NUM个线程等待队列
for i in range(NUM):
    t = Thread(target=working)
    t.setDaemon(True)
    t.start()
#把JOBS排入队列
for i in range(JOBS):
    q.put(i)
#阻塞，等待所有JOBS完成
q.join()
f.close()
# -*- coding: utf-8 -*-

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


f=open("rest_idx.txt", 'r')

#设置请求中头文件的信息
headers = {'User-Agent':'Mozilla/5.0 '
                        '(Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML,'
                        ' like Gecko) Chrome/76.0.3809.132 '
                        'Safari/537.36',
#'Accept':'text/html;q=0.9,*/*;q=0.8',
#'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#"Accept-Language": "zh-CN,zh;q=0.9",
#'Connection':'close',
'Referer':'https://www.jd.com/'
}

q = queue.Queue()
NUM = 5
JOBS = 10
#cookies=***
def crawl_jd_cmt_tag(prdtId):# change for url

    url=r"https://sclub.jd.com/comment/" \
        r"productPageComments.action?callback=fetchJSON_comment98vv106813&" \
        r"productId={}&" \
        r"score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1".format(prdtId)
    comment_tag_path = r'C:\TC-prog\JetBrain_pycharm_TC' \
                       r'\PycharmProjects\Crawler_EEFinal' \
                       r'\jd_cmt_tags\httpsitem.jd.com{}.html.txt'.format(prdtId)

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
        r_json_str = r.text[pos + 1:-2]
        # print (r_json_str)
        r_json_obj=json.loads(r_json_str,strict=False)
        print (r_json_obj)
        r_json_tags=r_json_obj['hotCommentTagStatistics']
        print ('狗东评论标签：')
        # 追加模式，逐行写入

        for r_json_tag in r_json_tags:
            with open(comment_tag_path,'a+') as file:
                file.write(r_json_tag['name']+
                           '\t'+str(r_json_tag['count'])+'\n')
                print(r_json_tag['name']+
                      '\t'+str(r_json_tag['count']))
    except:
        print('failed')


def run():
    global f
    for line in f.readlines():
        try:
            pp = line.split('\t')
            webpage = pp[1].strip('\n')
            print(webpage)
            temp = webpage[14:-5]
            pos = 0
            for i in range(len(temp)):
                if temp[i] == 'm':
                    pos = i
            itemID = temp[pos + 1:]

            if (len(webpage) > 35):
                continue

            crawl_jd_cmt_tag(itemID)
            time.sleep(random.random() * 3)
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
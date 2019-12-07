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
import math



#设置请求中头文件的信息
headers = {'User-Agent':'Mozilla/5.0 '
                        '(Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML,'
                        ' like Gecko) Chrome/76.0.3809.132 '
                        'Safari/537.36',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#"Accept-Language": "zh-CN,zh;q=0.9",
'Connection':'close',
'Referer':'https://www.jd.com/'
}


#cookies=***
def crawl_jd_cmt_SCORE(prdtId=100009691096):# change for url

    url=r"https://sclub.jd.com/comment/" \
        r"productPageComments.action?callback=fetchJSON_comment98vv1279&" \
        r"productId=%s&" \
        r"score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1"%prdtId
    comment_tag_path = r'C:\TC-prog\JetBrain_pycharm_TC' \
                       r'\PycharmProjects\Crawler_EEFinal' \
                       r'\jd_cmt_SCORE\httpsitem.jd.com%s.html.txt'%prdtId

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
        #print (r_json_obj)
        r_json_Sum=r_json_obj['productCommentSummary']
        print ('狗东评论打分：')
        print(r_json_Sum)
        # 追加模式，逐行写入
        with open(comment_tag_path, 'w') as file:
            sumcmt=r_json_Sum['commentCount']
            rate=r_json_Sum['goodRateShow'] # 好评率*100
            #good=r_json_Sum['goodCount'] # 好评数
            #gen =r_json_Sum['generalCount'] # 中评数
            #poor=r_json_Sum['poorCount'] # 差评数
            video =r_json_Sum['videoCount']
            after =r_json_Sum['afterCount']

            score=int(rate*0.7+math.log10(sumcmt)*5+
                          ((after+video)*1.0)/sumcmt/0.05)


            file.write("httpitem.jd.com"+str(prdtId) +".html"
                       + '\t' + str(score) + '\n')
            print("httpsitem.jd.com"+str(prdtId) +".html"
                       + '\t' + str(score))


    except:
        print('large json')


if __name__ == '__main__':

    with open("Final_available_idx.txt",'r') as f:
        for line in f.readlines():
            pp = line.split('\t')
            webpage = pp[1].strip('\n')
            print (webpage)
            temp=webpage[14:-5]
            pos=0
            for i in range(len(temp)):
                if temp[i] == 'm':
                    pos = i
            itemID=temp[pos+1:]
            print(itemID)
            if(len(webpage)>35):
                continue
            print (itemID)
            try:
                itemID=int(itemID)
                crawl_jd_cmt_SCORE(itemID)
                time.sleep(random.random() * 3)
            except:
                print("Invalid Input!")

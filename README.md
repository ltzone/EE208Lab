# EE208Lab
2019 Fall Semester EE208 Final Project Working Space :D

# 目录说明
```
root
|	|--Crawler 京东爬虫脚本
|	|--jd_contents 京东商品信息提取到的信息,based on URL
|	|--logo_recognition SIFT识别logo所用图片，archived
|	|--static 前端用到的静态文件
|	|--templates 前端用到的网页模板
|
|--code.py web.py 前端脚本
|
|--getdetail.py 提取京东商品的属性脚本
|--jd_cmt_TAGS.py 提取京东商品features
|
|--logo_sift.py 图像识别脚本
|
|--search.py Lucene检索程序，支持相关度、价格排序、评论分排序
|--final.1.py Lucene建索引脚本，working

```

# URL组织形式
```
index/moreidx -> search -> filter -> result

pictidx -> match -> search -> filter -> result
result_group [(/result,result)]
helping_group [(/match,match)]
```

# Goal

定向采集 2-3 个电商网站的某一类商品（如图书、数码、美妆、个护等）的信息（含评论信息）, 对这些信息进行抽取、索引和检索，构建一个搜索引擎。要求：

1.网页数目不少于 1万条

2.能根据**商品名称、商品属性、关键词、** 
** 商品图片** 等进行检索

3.能按**相关度、价格等属性进行排序**

4.能按类别、品牌、特性等属性进行过滤

5.能基于商品评论内容估计商品质量，并实现基于商品评价的排序（ Optional ）

爬取评论关键词，进行评分

6.能实现基于logo图像的搜索（Optional）

对网页范围内的品牌建立category-logo关系，对传入图片做logo匹配。

7.\*pagerank

# 进度

## Week1 ~12.6 Crawler & Parser for multiple Websites

## Week2 ~12.13 Build Searcher

## Week3 ~12.20 Comments / Logo Name / Logo Pict Search / PageRank

## Week4 ~12.27 Clean-Up and Presentation

## Week5 ~1.10 Report
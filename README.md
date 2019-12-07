# EE208Lab
2019 Fall Semester EE208 Final Project Working Space :D

# Goal

定向采集 2-3 个电商网站的某一类商品（如图书、数码、美妆、个护等）的信息（含评论信息）, 对这些信息进行抽取、索引和检索，构建一个搜索引擎。要求：

1.网页数目不少于 1万条

2.能根据**商品名称、商品属性、关键词、** 
**- 商品图片** 等进行检索

3.能按**相关度、价格等属性进行排序**

4.能按类别、品牌、特性等属性进行过滤

5.能基于商品评论内容估计商品质量，并实现基于商品评价的排序（ Optional ）

爬取评论关键词，进行评分

6.能实现基于logo图像的搜索（Optional）

对网页范围内的品牌建立category-logo关系，对传入图片做logo匹配。

7.\*pagerank

# 进度

## Week1 ~12.6 Crawler & Parser for multiple Websites

准备工作：爬取网页，爬取内容包括此后实验需要用到的所有信息

Wednesday、Friday：

- 解析网页，提取URL、商品名称、价格、属性
- 根据评论内容打分
- 商品图片提取（可能包括上下文）

Friday：建立索引文档（支持相关度排序、过滤）、搭建检索器 （for website and for pict）

Saturday：Web前端

## Week2 ~12.13 Build Searcher

## Week3 ~12.20 Comments / Logo Name / Logo Pict Search / PageRank

## Week4 ~12.27 Clean-Up and Presentation

## Week5 ~1.10 Report
# EE208Lab
2019 Fall Semester EE208 Final Project
By Group 14

# 目录说明
```
root
|-- Crawler 京东爬虫脚本
|-- Web web前端及检索程序
|	|-- FINDEX lucene索引文件
|	|-- static 网页用到的静态文件
|	|-- templates web.py模板
|	|-- code.py web运行脚本
|		| # dependency
|		|-- logo_sift.py logo匹配脚本
|		|-- search.py lucene检索脚本
|		|-- hash_table.json 用于LSH匹配哈希表
|	|-- makehash.py 建立哈希表的py脚本
|		
|-- jd_cmt_score 根据评论为京东商品打分脚本与文件
|-- jd_cmt_tags 京东商品评论标签爬取脚本与文件
|-- jd_makeidx
|	|-- detail 爬取的京东商品信息
|	|-- index 建立的lucene索引
|	|-- getdetail.py 爬取京东商品信息脚本
|	|-- makeindex.py 建立lucene索引脚本
|	|-- cmtidx.txt 建立索引的URL和imgURL记录，用于LSH匹配
|
|-- logo_recognition logo识别所需文件
|
|-- sn_crawler 爬取苏宁商品URL、获取商品信息的脚本与文件
|-- sn_cmt 苏宁商品评论标签爬取脚本与文件
|-- sn_score 根据评论为苏宁商品打分脚本与文件
|
|-- report 实验报告及相关文档
```

# 运行方式
```
$ python Web/code.py
```

# 环境要求
- Python 2.7
- Lucene 4.9.0
- jieba中文分词器 https://github.com/fxsjy/jieba
- opencv2
- web.py
# EE208Lab
2019 Fall Semester EE208 Final Project Working Space :D

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
|		
|-- jd_cmt_score 根据评分为京东商品打分脚本与文件
|-- jd_cmt_tags 京东商品评论标签爬取脚本
|-- jd_makeidx
|	|-- detail 爬取的京东商品信息
|	|-- index 建立的lucene索引
|	|-- getdetail.py 爬取京东商品信息脚本
|	|-- makeidx.py 建立lucene索引脚本
|	|-- idx.txt 建立索引的URL和imgURL记录，用于LSH匹配
|
|-- logo_recognition logo识别所需文件
|-- sn ... working
|
|-- report 实验报告及相关文档

```

# URL组织形式
```
index/moreidx -> search -> filter -> result

pictidx -> match -> search -> filter -> result
result_group [(/result,result)]
helping_group [(/match,match)]
```

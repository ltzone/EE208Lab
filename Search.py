#!/usr/bin/env python

INDEX_DIR = "pictindex"

import sys, os, lucene
reload(sys)
sys.setdefaultencoding('utf-8')

import json

from java.io import File
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
import jieba

'''
field assumption:
field name   |  indexed  |  stored | tokenized | record freq&position
imgurl  N Y N N
path    N Y N N
title(=content) Y Y Y Y
name  N Y N N
brand N Y N N
price  use a built-in LONG field 以分为单位，存整数
rank   use a built-in LONG field 以小数点后几位为单位，存整数
attribute(一列商品属性，用空格和冒号区分)  N Y N N
feature（一列商品印象+数字，用空格和冒号区分） N Y N N
'''

def read_results(scoreDocs):
    # 读取lucene检索结果对象ScoreDocs
    # 输出一个结果res_lis，list的元素是一个包含了商品所有信息的json串，在网页中可以用json.loads()解码
    res_lis = []
    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        item = dict()
        item['imgurl'] = doc.get("imgurl").strip()
        item['url'] = doc.get("url").strip()
        item['title'] = doc.get("title")
        item['brand'] = doc.get("brand")
        item['price'] = doc.get("price")
        item['rank'] = doc.get("rank")
        itemattr = dict()
        attrseg = doc.get("attribute").split(' ')
        for attr in attrseg:
            attrseg = attr.split(':')
            itemattr[attrseg[0]]=attrseg[1]
        item['attribute'] = itemattr
        itemfeat = dict()
        featseg = doc.get("feature").split(' ')
        for feat in featseg:
            featseg = feat.split(':')
            featattr[featseg[0]]=featseg[1]
        item['feature'] = itemfeat
        res_lis.append(json.dumps(item))
    return res_lis

def highprice_search(searcher, analyzer, command):
    # 按价格降序排序
    highprice_sorter = Sort(SortField("price",SortField.LONG,true))
    seg_list = jieba.cut(command)
    command = (" ".join(seg_list))
    query = QueryParser(Version.LUCENE_CURRENT, "contents",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 50, highprice_sorter)
    return read_results(scoreDocs)

def lowprice_search(searcher, analyzer, command):
    # 按价格升序排序
    lowprice_sorter = Sort(SortField("price",SortField.LONG))
    seg_list = jieba.cut(command)
    command = (" ".join(seg_list))
    query = QueryParser(Version.LUCENE_CURRENT, "title",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 50, lowprice_sorter)
    return read_results(scoreDocs)

def rank_search(searcher, analyzer, command):
    rank_sorter = Sort(SortField("rank",SortField.LONG))
    seg_list = jieba.cut(command)
    command = (" ".join(seg_list))
    query = QueryParser(Version.LUCENE_CURRENT, "contents",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 50, rank_sorter)
    return read_results(scoreDocs)

def search(query,method):
    query = unicode(query)
    STORE_DIR = "pictindex"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = SimpleAnalyzer(Version.LUCENE_CURRENT)
    return globals()[method+'_search'](searcher,analyzer,query)


'''
if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    #directory = SimpleFSDirectory(File(STORE_DIR))
    #searcher = IndexSearcher(DirectoryReader.open(directory))
    #analyzer = SimpleAnalyzer(Version.LUCENE_CURRENT)
    #run(searcher, analyzer)
    del searcher
'''
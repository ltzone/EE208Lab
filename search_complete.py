#!/usr/bin/env python
# coding=UTF-8
INDEX_DIR = "FINDEX"

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
attribute N Y N N
attribute(一列商品属性，用空格和冒号区分)  N Y N N
feature（一列商品印象+数字，用空格和冒号区分） N Y N N
'''

def read_results(scoreDocs, searcher):
    # 读取lucene检索结果对象ScoreDocs
    # 输出一个结果res_lis，list的元素是一个包含了商品所有信息的json串，在网页中可以用json.loads()解码
    res_lis = []
    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        item = dict()
        item['imgurl'] = doc.get("imgurl").strip()
    #    item['url'] = doc.get("url").strip()
        item['title'] = doc.get("title")
        item['brand'] = doc.get("brand")
        item['price'] = doc.get("price")
        item['rank'] = doc.get("rank")
        item['category'] = doc.get("attribute")
        '''
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
        '''
        res_lis.append(json.dumps(item))
    return res_lis

def highprice_search(searcher, analyzer, command):
    # 按价格降序排序
    highprice_sorter = Sort(SortField("price",SortField.LONG,True))
    seg_list = jieba.cut(command)
    command = (" ".join(seg_list))
    query = QueryParser(Version.LUCENE_CURRENT, "title",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 50, highprice_sorter)
    return read_results(scoreDocs,searcher)

def lowprice_search(searcher, analyzer, command):
    # 按价格升序排序
    lowprice_sorter = Sort(SortField("price",SortField.LONG))
    seg_list = jieba.cut(command)
    command = (" ".join(seg_list))
    query = QueryParser(Version.LUCENE_CURRENT, "title",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 50, lowprice_sorter)
    return read_results(scoreDocs,searcher)

def rank_search(searcher, analyzer, command):
    rank_sorter = Sort(SortField("rank",SortField.LONG))
    seg_list = jieba.cut(command)
    command = (" ".join(seg_list))
    query = QueryParser(Version.LUCENE_CURRENT, "title",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 50, rank_sorter)
    return read_results(scoreDocs,searcher)

def relativity_search(searcher, analyzer, command):
    print "calling relativity_search"
    print command
    seg_list = jieba.cut(command)
    command = (" ".join(seg_list))
    query = QueryParser(Version.LUCENE_CURRENT, "title",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 50).scoreDocs
    return read_results(scoreDocs,searcher)


def search_command(query,method):
    query = unicode(query)
    STORE_DIR = "FINDEX"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = SimpleAnalyzer(Version.LUCENE_CURRENT)
    return globals()[method+'_search'](searcher,analyzer,query)

'''
中间格式contents = (json object):
dict {
    imgurl
    url
    title
    brand
    price
    rank
    attr {
        text: text
        ...
    }
    feature{
        text: num
        ...
    }
}
'''

def tag_filter(contents,categorys,features,brands):
    results = list()
    for item in contents:
        item = json.loads(item)
        if match_item(item,categorys,features,brands):
            results.append(item)
    return results

def match_item(item,categorys,features,brands):
    if not match_item_one(item,categorys,'category'):
        return False
    if not match_item_one(item,features,'feature'):
        return False
    if not match_item_one(item,brands,'brand'):
        return False
    return True

def match_item_one(item,properties,property_name):
    if (not properties):
        for proper in properties:
            if proper in item[property_name].keys():
                return True
    return False


def sort_and_filter(x_count,length):
    x_tuple = zip(x_count.keys(),x_count.values())
    x_sorted = sorted(x_tuple)
    filtered_x = x_sorted[:length]
    return filtered_x

def total(contents):
    # 返回三个参数的tuple，三个长度最长为n的[(key,num)]列表，分别是brand，category和feature的tag
    brand_count = dict()
    category_count = dict()
    feature_count = dict()
    for item in contents:
        item = json.loads(item)
        brand = item['brand']
        category = item['category']
    
    ###    features = item['feature']
     
        if not brand_count.has_key(brand):
            brand_count[brand] = 0
        brand_count[brand] += 1
        if not category_count.has_key(category):
            category_count[category] = 0
        category_count[category] += 1

        '''
        for feature in features.keys():
            if not feature_count.has_key(feature):
                feature_count[feature] = 0
            feature_count[features] += features[feature]
        '''
    brand_tags = sort_and_filter(brand_count,5)
    category_tags = sort_and_filter(category_count,5)
    '''
    feature_tags = sort_and_filter(feature_count,10)
    '''
    feature_tags = []
    return (brand_tags,category_tags,feature_tags)


def itemlis(contents):
    res_lis = []
    for item in contents:
        item = json.loads(item)
        res_lis.append((item["imgurl"],item["url"],item["title"]))
    return res_lis




if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=True'])
    print 'lucene', lucene.VERSION
    print search_command("索尼","relativity")
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    #directory = SimpleFSDirectory(File(STORE_DIR))
    #searcher = IndexSearcher(DirectoryReader.open(directory))
    #analyzer = SimpleAnalyzer(Version.LUCENE_CURRENT)
    #run(searcher, analyzer)

#!/usr/bin/env python
# coding=UTF-8
INDEX_DIR = "FINDEX"

import sys, os, lucene
reload(sys)
sys.setdefaultencoding('utf-8')

import json

from java.io import File
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search import Sort
from org.apache.lucene.search import SortField
from org.apache.lucene.search import TermQuery
import jieba
import re
from makehash import get_feature_Local, get_feature, LSHash


projs = [ 
    [7, 10, 16, 21, 23, 34, 45, 48, 61, 62, 69, 77], 
    [12, 20, 23, 30, 32, 40, 57, 61, 62, 70, 78, 94], 
    [10, 14, 18, 21, 25, 33, 39, 44, 50, 67, 91, 93], 
    [13, 18, 19, 42, 52, 65, 67, 68, 71, 88, 90, 92], 
    [4, 6, 15, 23, 28, 37, 45, 46, 62, 81, 83, 93]]

def parseCommand(command):
    '''
    input: C title:T author:A language:L
    output: {'contents':C, 'title':T, 'author':A, 'language':L}

    Sample:
    input:'contenance title:henri language:french author:william shakespeare'
    output:{'author': ' william shakespeare',
                   'language': ' french',
                   'contents': ' contenance',
                   'title': ' henri'}
    '''
    allowed_opt = ['website','brand']
    command_dict = {}
    opt = 'title'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict

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
        item['url'] = doc.get("url").strip()
        item['title'] = "".join(doc.get("title").split())
        item['brand'] = doc.get("brand")
        item['price'] = doc.get("price")
        item['rank'] = doc.get("score")
        item['category'] = doc.get("attribute")
        item['source'] = doc.get("website")

        # 商品具体属性
        itemdet = dict()
        detseg = doc.get("detail").split('\t')
        for detail in detseg:
            detailseg = detail.split(':')
            if len(detail)>1:
                itemdet[detailseg[0]]=detailseg[1]
        item['detail'] = itemdet

        # 商品评价tag
        itemfeat = dict()
        featseg = re.split(' ',doc.get("tag"))
        for feat in featseg:
            featureseg = feat.split('\t')
            if (len(featureseg)>1):
                itemfeat[featureseg[0].strip()]=featureseg[1]
        item['feature'] = itemfeat
        res_lis.append(json.dumps(item))
    return res_lis

def highprice_search(searcher, analyzer, command):
    # 按价格降序排序
    highprice_sorter = Sort(SortField("price",SortField.Type.LONG,True))
    query = command_to_query(command,analyzer)
    scoreDocs = searcher.search(query, 150, highprice_sorter).scoreDocs
    return read_results(scoreDocs,searcher)

def lowprice_search(searcher, analyzer, command):
    # 按价格升序排序
    lowprice_sorter = Sort(SortField("price",SortField.Type.LONG))
    query = command_to_query(command,analyzer)
    scoreDocs = searcher.search(query, 150, lowprice_sorter).scoreDocs
    return read_results(scoreDocs,searcher)

def rank_search(searcher, analyzer, command):
    rank_sorter = Sort(SortField("score",SortField.Type.LONG,True))
    query = command_to_query(command,analyzer)
    scoreDocs = searcher.search(query, 150, rank_sorter).scoreDocs
    return read_results(scoreDocs,searcher)

def relativity_search(searcher, analyzer, command):
    print "calling relativity_search"
    print command
    query = command_to_query(command,analyzer)
    scoreDocs = searcher.search(query,150).scoreDocs
    return read_results(scoreDocs,searcher)

def command_to_query(command,analyzer):
    command_dict = parseCommand(command)
    print command_dict
    seg_list = jieba.cut(command_dict['title'])
    command_dict['title'] = (" ".join(seg_list))
    querys = BooleanQuery()
    for k,v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    return querys


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
    category
    detail {
        text: text
        ...
    }
    feature{
        text: num
        ...
    }
}
'''

def tag_filter(contents,categorys,features,brand,source):
    results = list()
    for item in contents:
        item2 = json.loads(item)
        if match_item(item2,categorys,features,brand,source):
            results.append(item)
    return results

def match_item(item,categorys,features,brands,sources):
    if not match_item_one(item,categorys,'category'):
        return False
    if not match_item_feature(item,features,'feature'):
        return False
    if not match_item_one(item,brands,'brand'):
        return False
    if not match_item_one(item,sources,'source'):
        return False
    return True

def match_item_feature(item,properties,property_name):
    # 与其他属性不同，特色取交集
    if (not properties):
        return True
    for proper in properties:
        if proper not in item[property_name].keys():
            return False
    return True

def match_item_one(item,properties,property_name):
    if (not properties):
        return True
    for proper in properties:
        if proper == item[property_name]:
            return True
    return False

def sort_and_filter(x_count,length):
    x_tuple = zip(x_count.keys(),x_count.values())
    x_sorted = sorted(x_tuple,key = lambda kv:(-kv[1], kv[0]))
    filtered_x = x_sorted[:length]
    return filtered_x

def total(contents):
    # 返回三个参数的tuple，三个长度最长为n的[(key,num)]列表，分别是brand，category和feature的tag
    brand_count = dict()
    category_count = dict()
    feature_count = dict()
    source_count = dict()
    for item in contents:
        item = json.loads(item)
        brand = item['brand']
        category = item['category']
        feature = item['feature']
        source = item['source']
        if not brand_count.has_key(brand):
            brand_count[brand] = 0
        brand_count[brand] += 1
        if not category_count.has_key(category):
            category_count[category] = 0
        category_count[category] += 1
        if not source_count.has_key(source):
            source_count[source] = 0
        source_count[source] += 1
        for (felem,fnum) in feature.items():
            if not feature_count.has_key(felem):
                feature_count[felem] = 0
            feature_count[felem] += int(fnum)

    brand_tags = sort_and_filter(brand_count,5)
    category_tags = sort_and_filter(category_count,5)
    source_tags = sort_and_filter(source_count,2)
    feature_tags = sort_and_filter(feature_count,10)
    return [brand_tags,category_tags,feature_tags,source_tags]


def itemlis(contents):
    res_lis = []
    for item in contents:
        res_lis.append(json.loads(item))
    return res_lis
'''
item
0 - imgurl
1 - url
2 - title
3 - property

'''



def pict_search(img):
    urls = match_pict(img)
    print urls
    STORE_DIR = "FINDEX"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    res_lis = []
    for url in urls:
        query = TermQuery(Term("url",url))
        scoreDocs = searcher.search(query, 1).scoreDocs
        res_lis += read_results(scoreDocs,searcher)
    return res_lis
 

def similarity(det1,det2):
    sum = 0
    for i in range(len(det1)):
        sum += abs(det1[i]-det2[i])
    return sum


def match_pict(img):
    docs = []
    imgfeat = get_feature_Local(img)
    with open("hash_table.json",'r') as load_f:
        load_list = json.load(load_f)

        for j in range(5):
            hash_val = LSHash(imgfeat,projs[j])
            hits = load_list[j][int(hash_val)]
            print (len(hits))
            for hit in hits:
                elem = hit[0],similarity(imgfeat,hit[1])
                if elem not in docs:
                    docs.append(elem)
    docs_sorted = sorted(docs,key = lambda kv:(kv[1]))
    res_lis = [i for (i,j) in docs_sorted[:50]]
    return res_lis


if __name__ == '__main__':
    STORE_DIR = "index"
    # lucene.initVM(vmargs=['-Djava.awt.headless=True'])
    # print 'lucene', lucene.VERSION
    # print search_command("索尼","relativity")
    print match_pict("ttt.png")
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    #directory = SimpleFSDirectory(File(STORE_DIR))
    #searcher = IndexSearcher(DirectoryReader.open(directory))
    #analyzer = SimpleAnalyzer(Version.LUCENE_CURRENT)
    #run(searcher, analyzer)

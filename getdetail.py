#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')


def getTitle(url):
    try:
        url1= urllib2.urlopen(url).read()
        html = BeautifulSoup(url1,features="html.parser")
        title = html.title.string
        return title
    except :
        title=''
        print "false"
        return title

#dict1 = {}

def parse(url,content):

    # imgurl
    soup = BeautifulSoup(content,features='html.parser')
    for img in soup.find_all('img', id="spec-img"):
        src = img.get('data-origin', '')
        if (src == '' or not (src.endswith('jpg') or src.endswith('png'))):
            continue
        src = 'http:' + src
        with open(url + '.txt', 'a') as f3:
            f3.write(src)
            print src
            f3.write('\n')


    # other
    for k in soup.find_all('ul', {'class': 'parameter2 p-parameter-list'}):
        full = k.get_text()

        # name
        url2 = 'https://p.3.cn/prices/mgets?skuIds=J_' + str(k.contents[3].get('title'))
        c = str(str(full)[1:-1])
        c1=c.split('\n')
        c2=c1[0].split("：")
        with open(url + '.txt', 'a') as f:
            f.write(c2[1])
            print c2[1]
            f.write('\n')
        #dict1[c2[0]]=c2[1]

        # brand
        for k in soup.find_all('a', {'clstag': 'shangpin|keycount|product|pinpai_1'}):
            brand = k.get_text()
            #dict1['brand'] = brand
            with open(url + '.txt', 'a') as f:
                f.write(brand)
                print brand
                f.write('\n')

        # price
        request2 = urllib2.Request(url2)
        response2 = urllib2.urlopen(request2)
        content2 = response2.read()
        a = content2.find('\"p\":\"')
        b = content2.find('\"}]')
        #dict1['price'] = content2[a + 5:b]
        with open(url + '.txt', 'a') as f:
            f.write(content2[a + 5:b])
            print content2[a + 5:b]
            f.write('\n')

        # attribute
        for k in soup.find_all('a', {'clstag': 'shangpin|keycount|product|mbNav-3'}):
            item = k.get_text()
            #dict1['type'] = item
            with open(url + '.txt', 'a') as f:
                f.write(item)
                print item
                f.write('\n')

        # other information
        with open(url + '.txt', 'a') as f:
            for i in c1[1:-1]:

                c2=i.split("：")

                f.write(c2[0])
                f.write(':')
                f.write(c2[1])
                f.write('\t')
            print 'ok\n'
                #dict1[c2[0]]=c2[1]



def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    if len(s) > 255:
        s = s[:255]
    return s

def getdetail(url):
    filename = valid_filename(url)
    #dict1['title'] = getTitle(url)
    with open(filename + '.txt', 'w') as f:
        f.write(getTitle(url))
        f.write('\n')
        f.write(url)
        f.write('\n')
        f.close()
    content = urllib2.urlopen(url).read()
    parse(filename, content)


def main():
    #getdetail('https://item.jd.com/37313139007.html')
    f = open("Fi-index.txt")
    line = f.readline()
    while line:
        url=line.split('\t') [0]
        print url
        getdetail(url)
        line = f.readline()




if __name__ == '__main__':
    main()
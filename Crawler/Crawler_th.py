# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import os
import Queue
import threading
from threading import Thread
import time
import urllib
import urlparse
from BLF import *


def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    if len(s) > 255:
        s = s[:255]
    return s


def get_page(page):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0)\
            Gecko/20100101 Firefox/14.0.1'}
    try:
        req = urllib2.Request(url=page, headers=header)
        respones = urllib2.urlopen(req, timeout=10)
        content = respones.read()
    except:
        return ''.encode('utf8')
    return content


def complete_url(Link, url):
    if Link[0] == 'h':
        return Link
    if Link[0] == '/':
        if len(Link) == 1 or Link[1] != '/':
            return urlparse.urljoin(url, Link)
        else:
            return 'http:' + Link
    return Link


def check_ban(string):
    global banlist
    for i in banlist:
        if re.search(i + '$', string) != None:
            return True
    return False


def get_soup(content, sup):
    sup.append(BeautifulSoup(content, 'html.parser'))

def get_all_links(content):
    if content == None:
        return []
    import re
    urlset = set()
    urls = re.findall(r"item.jd.com/[^\s]*.html",content,re.I)
    for u in urls:
        urlset.add('http://'+u)
    links = list(urlset)
    return links



def set_in(string):
    for j in range(1, 10):
        has = globals()['hash_%s' % (str(j))](string) % 998244353
        crawled.set(has)


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'Fi-index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'Fi-html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)  # 将网页存入文件
    f.close()


def checkin(string):
    In = True
    for j in range(1, 10):
        has = globals()['hash_%s' % (str(j))](string) % 998244353
        In &= crawled.get(has)
    return In


def crawl():
    global count
    global seed
    global max_page

    Q.put(seed)
    while not Q.empty():
        if count >= max_page:
            while not Q.empty():
                Q.get()
                Q.task_done()
            break

        page = Q.get()
        if page == '':
            Q.task_done()
            continue
        #if not page[:20] == 'https://item.jd.com':
         #   continue
        if not checkin(page) and not checkin(page + '/'):
            print page
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content)
            time.sleep(1)
            if count < max_page:
                for link in outlinks:
                    Q.put(link)
            if varlock.acquire():
                count += 1
                set_in(page)
                graph[page] = outlinks
                varlock.release()
        Q.task_done()


if __name__ == '__main__':
    mod=998244353
    len_a = len(sys.argv)
    seed = sys.argv[1] if len_a > 1 else 'https://item.jd.com/100001484839.html'
    max_page = int(sys.argv[2]) if len_a > 2 else 15000
    parrel_num = int(sys.argv[3]) if len_a > 3 else 8

    banlist = []
    with open("banlist.txt", "r") as F:
        for lin in F:
            banlist.append(lin.strip())

    Q = Queue.Queue()
    count = 0
    graph = {}
    crawled = Bitarray(mod)
    varlock = threading.Lock()

    for i in range(parrel_num):
        tas = Thread(target=crawl)
        tas.setDaemon(True)
        tas.start()
    Q.join()
    
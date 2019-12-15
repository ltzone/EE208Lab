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
import urlparse
from BLF import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtCore import *

reload(sys)
sys.setdefaultencoding("utf-8")


class BrowserRender(QWebView):
    def __init__(self, show=True):
        try:
            self.app = QApplication(sys.argv)
        except:
            self.app = QCoreApplication.instance()
        QWebView.__init__(self)
        if show:
            self.show()
    def download(self, url, timeout=60):
        loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)
        self.loadFinished.connect(loop.quit)
        self.load(QUrl(url))
        timer.start(timeout * 1000)
        loop.exec_()
        if timer.isActive():
            timer.stop()
            return self.html()
        else:
            print "Request time out: " + url
    def html(self):
       return self.page().mainFrame().toHtml()

    def find(self, pattern):
       return self.page().mainFrame().findAllElements(pattern)

    def attr(self, pattern, name, value):
       for e in self.find(pattern):
           e.setAttribute(name, value)

    def text(self, pattern, value):
       for e in self.find(pattern):
           e.setPlainText(value)

    def click(self, pattern):
       for e in self.find(pattern):
           e.evaluateJavaScript("this.click()")


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


def complete_url(link, url=' '):
    # if link[0] == 'h':
    #     return Link
    if link[0] == '/':
        if len(link) == 1 or link[1] != '/':
            link = urlparse.urljoin(url, Link)
        else:
            link = 'http:' + link
    ret = urlparse.urlparse(link)
    link = urlparse.urljoin(ret.scheme + "://" + ret.netloc, ret.path)

    return link


def get_clean_url(url):
    ret = urlparse.urlparse(url)
    link = urlparse.urljoin(ret.scheme + "://" + ret.netloc, ret.path)
    return link


'''
def get_price(url):
    global flag
    if flag:
        br = BrowserRender(show=False)
        flag = False
    br.download(url)
    price = br.find("span.mainprice")
    print price[0].toPlainText().encode("utf-8").strip()
    return price[0].toPlainText().encode("utf-8").strip()
'''


def get_all_links(content):
    if content == None:
        return []
    links = set()
    url = 'http://product.suning.com'
    soup = BeautifulSoup(content,features='html.parser')
    p = re.compile(r".*product.suning.com.*")
    for i in soup.findAll('a'):
        linkPage = i.get('href')
        if p.match(str(linkPage)):
            links.add(complete_url(linkPage,url))
    links = list(links)
    return links


def set_in(string):
    for j in range(1, 10):
        has = globals()['hash_%s' % (str(j))](string) % 998244353
        crawled.set(has)


def get_data(content,url,price):
    soup = BeautifulSoup(content, features='html.parser')
    data = dict()
    data['title'] = soup.head.title.text
    data['url'] = url
    imgurl = soup.findAll('a',{'id':'bigImg'})[0]
    imgurl = complete_url(imgurl.findAll('img')[0].get('src'))
    data['imgurl'] = imgurl
    name_tag = soup.findAll('span', {'class':'breadcrumb-title'})[0]
    name = name_tag.get('title')
    dropdown = soup.findAll('div',{'class':'dropdown'})
    brand_tag = dropdown[-1].find('a')
    attribute_tag = dropdown[-2].find('a')
    data['brand'] = brand_tag.find_all(text=True)[0]
    data['name'] = name
    data['attribute'] = attribute_tag.text
    data['price'] = price
    return data


def add_page_to_folder(page,a):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index_sn.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html_sn'  # 存放网页的文件夹
    filename = valid_filename(page)+'.txt'  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(a['title'] + '\n')
    f.write(a['url'] + '\n')
    f.write(a['imgurl'] + '\n')
    f.write(a['name'] + '\n')
    f.write(a['brand'] + '\n')
    f.write(a['price'] + '\n')
    f.write(a['attribute'] + '\n')
    f.close()


def checkin(string):
    In = True
    for j in range(1, 10):
        has = globals()['hash_%s' % (str(j))](string) % 998244353
        In &= crawled.get(has)
    return In


'''
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
            time.sleep(3)
            if varlock.acquire():
                content = get_page(page)
                add_page_to_folder(page, content)
                outlinks = get_all_links(content)
                if count < max_page:
                    for link in outlinks:
                        Q.put(link)
                count += 1
                set_in(page)
                graph[page] = outlinks
                varlock.release()
        Q.task_done()
'''


'''

len_a = len(sys.argv)
seed = sys.argv[1] if len_a > 1 else 'https://product.suning.com/0000000000/11397426600.html?safp=d488778a.10004.0.10ef57f37a&safc=prd.0.0'
max_page = int(sys.argv[2]) if len_a > 2 else 5
parrel_num = int(sys.argv[3]) if len_a > 3 else 2

start_time = time.time()

Q = Queue.Queue()
count = 0
graph = {}
crawled = Bitarray(998244353)
varlock = threading.Lock()

for i in range(parrel_num):
    tas = Thread(target=crawl)
    tas.setDaemon(True)
    tas.start()
Q.join()
endtime = time.time()
print("finished in %lfs" % (endtime - start_time))

'''


pages = ['https://list.suning.com/0-20006-0.html','https://www.suning.com/pinpai/2450-258007-0.html']
max_page = 6

start_time = time.time()

crawled = Bitarray(998244353)
count = 0
p = re.compile(r".*product.suning.com.*")
br = BrowserRender(show=False)

while len(pages):
    if count >= max_page:
        break

    page = pages.pop(0)
    if page == '':
        continue

    if not checkin(page) and not checkin(page + '/'):
        content = get_page(page)
        outlinks = get_all_links(content)
        pages = pages + outlinks

        if not p.match(str(page)):
            continue

        count += 1
        print count
        print page
        set_in(page)

        time.sleep(5)

        # price
        try:
            br.download(page)
            price = br.find("span.mainprice")
            price = price[0].toPlainText().encode("utf-8").strip()
            price = price[2:]
            print price
        except:
            price = ' '
            print "price error"

        data = get_data(content,page,price)
        add_page_to_folder(page,data)




endtime = time.time()
print("finished in %lfs" % (endtime - start_time))







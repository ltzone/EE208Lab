#!/usr/bin/env python
# -*- coding: UTF-8 -*-
INDEX_DIR = "IndexFiles.index"
import jieba
import re
import urllib2
from bs4 import BeautifulSoup
import sys, os, lucene, threading, time
from datetime import datetime
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from socket import error as SocketError
import sys
import urllib2
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
import errno

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

def analysis(s):
    return ' '.join(jieba.cut(s))

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    if len(s) > 255:
        s = s[:255]
    return s

def getTitle(url):
    try:
        url1= urllib2.urlopen(url).read()
        html = BeautifulSoup(url1,features="html.parser")
        # title = html.find('title')
        title = html.title.string

        return title
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, dialog, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        #analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(dialog,root, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def getTxtAttribute(self, contents, attr):
        m = re.search(attr + ': (.*?)\n',contents)
        if m:
            return m.group(1)
        else:
            return

    def indexDocs(self, dialog,root, writer):

        t3 = FieldType()
        t3.setIndexed(False)
        t3.setStored(True)
        t3.setTokenized(False)
        t3.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)

        t1 = FieldType()
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(True)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        f = open(dialog)
        lines = f.readlines()
        for line in lines:
            info = line.split('\t')
            print info[0],'and    ',info[1]
            url = info[0]
            filename = valid_filename(url)
            #filename1 = filename.split('\n')
            #filename2 = filename1[0]

            try:



                print "adding", filename,'\n'
                if title != None:


                    path = os.path.join(root, filename)

                    #file = open(path)
                    #contents = unicode(file.read(), 'utf-8','ignore')
                    #file.close()
                    ll=[]

                    f = open(filename+".txt")
                    line = f.readline()
                    while line:
                        if (line[-1]=='\n'):
                            ll.append(line[:-1])
                        else:
                            ll.append(line)

                        line = f.readline()
                    doc = Document()
                    if len(contents) > 0:
                        doc.add(Field('price', int(100*float(ll[5])), t3))
                        print 'add price', int(100*float(ll[5])),'\n'
                        doc.add(Field('path', path, t3))
                        print 'add path', path, '\n'
                        doc.add(Field('imgurl', ll[2], t3))
                        print 'add imgurl', ll[2], '\n'
                        doc.add(Field('title', ll[0], t1))
                        doc.add(Field('name', ll[3], t3))
                        doc.add(Field("brand", ll[4], t3))
                        doc.add(Field("attribute", ll[6], t3))

                    else:
                        print "warning: no content in %s" % filename
                    writer.addDocument(doc)
            except :#SocketError as e:
                    #if e.errno != errno.ECONNRESET:
                    #    raise  # Not error we are looking for
                pass  # Handle error here.
            #except Exception, e:
            #    print "Failed in indexDocs:", e

if __name__ == '__main__':
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))
                   """
        analyzer = SimpleAnalyzer(Version.LUCENE_CURRENT)
        IndexFiles('Fi-index.txt', "Fi-html", "index1", analyzer)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e

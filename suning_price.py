"""
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtCore import *

import sys
import time

class BrowserRender(QWebView):
    def __init__(self, show=True):
        self.app = QApplication(sys.argv)
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
       for e in self.find(patter):
           e.evaluateJavaScript("this.click()")


    #def wait_load(self, pattern, timeout=60):
    #   deadline = time.time() + timeout
    #    while time.time() < deadline:
     #       self.app.processEvents()
     #       matches = self.find(pattern)
      #      if matches:
     #           return matches
      #  print("wait load time out")




if __name__=="__main__":
    br = BrowserRender(show=False)
    br.download("https://product.suning.com/0000000000/152709847.html? \
     srcpoint=index3_homepage1_32618213038_prod02")
    price = br.find("span.mainprice" )
    print (price[0].toPlainText().encode("utf-8").strip()) #如果不加encode("utf-8")会出现UnicodeEncodeError：gbk无法对u'\xa5'进行编码的错误

"""
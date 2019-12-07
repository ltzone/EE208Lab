# coding=UTF-8
import web

import sys, os, lucene
reload(sys)
sys.setdefaultencoding('utf-8')


from Search import search
from logo_sift import logo_recognition


try:
    vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
except:
    vm_env = lucene.getVMEnv()


urls = (
    '/', 'index',
    '/search', 'search',
    '/moreidx', 'moreidx',
    '/logoidx', 'logoidx',
    '/filter', 'filter',
)


render = web.template.render('templates') # your templates



class index:
    def GET(self):
        return render.index()

class moreidx:
    def GET(self):
        return render.moreidx()

class logoidx:
    def GET(self):
        return render.logoidx()
    def POST(self):
        x = web.input(input_img={})
        filedir = 'static/userupload'
        if 'input_img' in x:  # to check if the file-object is created
            fout = open(filedir + '/' + 'tmp', 'wb')
            # creates the file where the uploaded file should be stored
            fout.write(x.input_img.file.read())
            # writes the uploaded file to the newly created file.
            fout.close()  # closes the file, upload complete.

        kw = logo_recognition("static/userupload/tmp")
        vm_env.attachCurrentThread()
        contents = search(kw,'relativity')
        return render.result(kw, method, contents) # a demo for the input image

class search:
    def GET(self):
        user_data = web.input()
        kw = user_data.keyword
        method = web.input(method="relativity")
        vm_env.attachCurrentThread()
        contents = search(kw,method)
        return render.result(kw, method, contents)

class filter:
    def GET(self):
        user_data = web.input()
        kw = user_data.keyword
        vm_env.attachCurrentThread()
        contents = search(kw,method)
        return render.result(kw, method, contents)





if __name__ == "__main__":

    app = web.application(urls, globals())
    app.run()

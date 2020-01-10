# coding=UTF-8
import web

import sys, os, lucene
reload(sys)
sys.setdefaultencoding('utf-8')


from search import search_command, total, tag_filter, itemlis, pict_search
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
    '/pictsearch', 'pictsearch',
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

class pictsearch:
    def POST(self):
        x = web.input(input_img={})
        filedir = 'static/userupload'
        if 'input_img' in x:  # to check if the file-object is created
            fout = open(filedir + '/' + 'tmp', 'wb')
            # creates the file where the uploaded file should be stored
            fout.write(x.input_img.file.read())
            # writes the uploaded file to the newly created file.
            fout.close()  # closes the file, upload complete.
        if web.input().method == 'logo':
            kw = logo_recognition("static/userupload/tmp")
            vm_env.attachCurrentThread()
            contents = search_command(kw,'relativity'.decode('utf-8'))
            filtertags = total(contents)
            results = itemlis(contents)
            return render.result(kw, 'relativity', results, filtertags)
        else:
            vm_env.attachCurrentThread()
            contents = pict_search("static/userupload/tmp")
            filtertags = total(contents)
            results = itemlis(contents)
            return render.result('LSH Match', 'relativity', results, filtertags)

class search:
    def GET(self):
        user_data = web.input()
        kw = user_data.keyword
        method = web.input(method="relativity").method.decode('utf-8')
        vm_env.attachCurrentThread()
        contents = search_command(kw,method)           # 搜索结果
        filtertags = total(contents)           # 统计品牌、属性、特色的结果，即显示在页面左侧所必须的内容
        results = itemlis(contents)   # 要显示在页面右侧的所必需的内容
        return render.result(kw, method, results, filtertags)

class filter:
    def GET(self):
        user_data = web.input()
        kw = user_data.keyword
        method = web.input(method="relativity").method.decode('utf-8')
        category = web.input(category=[]).category
        features = web.input(feature=[]).feature
        brand = web.input(brand=[]).brand
        source = web.input(source=[]).source
        vm_env.attachCurrentThread()
        contents = search_command(kw,method) # 搜索结果
        filtertags = total(contents) # 统计品牌、属性、特色的结果，即显示在页面左侧所必须的内容
        filtered_contents = tag_filter(contents,category,features,brand,source)
                                     # 对搜索结果作筛选
        results = itemlis(filtered_contents) # 根据筛选结果提取出要显示在页面右侧的所必需的内容
        return render.result(kw, method, results, filtertags)





if __name__ == "__main__":

    app = web.application(urls, globals())
    app.run()

#!/usr/bin/env python
#coding=utf-8

import tornado.web
import sqlite3
    
import cStringIO
from PIL import Image

img = Image.new("RGBA",(256,256),(128,0,0,0))
tmp = cStringIO.StringIO()
img.save(tmp,'PNG')
blank = tmp.getvalue()

class SQLiteTile:
    #缓存
    CACHE = {}
    #缓存最大值
    CACHE_MAXIMUM = 10000
    #查询缓冲大小,请求某张图片时将连带下载周边的图片，以减少数据库查询次数
    BUF_SIZE = 1
    #图片标识符格式模板 "layer-x-y-z"
    TILE_ID_TMPL = "%s-%d-%d-%d"
    #图片查询SQL模板
    QUERY_TMPL = "select x,y,z,data from %s where x>%d and x< %d and y>%d and y<%d and z=%d"
    #数据库中没有相应记录的图片uid记录集
    NO_STORE = {}    

    def __init__(self,p):
        self.path = p

    def open(self):
        self.connect = sqlite3.connect(self.path)
        self.cursor = self.connect.cursor()

    def close(self):
        self.connect.close()

    def guid(self,layer,x,y,z):
        return self.TILE_ID_TMPL%(layer,x,y,z)

    def get(self,layer,x,y,z):
        guid = self.guid(layer,x,y,z)

        if guid in self.NO_STORE:
            print "tile %s not exsit"%guid
            return None

        data = self.CACHE.get(guid)

        if data is not None:
            return data

        sql = self.QUERY_TMPL%(layer,
            (x - self.BUF_SIZE),
            (x + self.BUF_SIZE),
            (y - self.BUF_SIZE),
            (y + self.BUF_SIZE),
            z)

        result = self.cursor.execute(sql).fetchall()
        d = dict([(self.guid(layer,*rec[:3]),rec[-1]) for rec in result])
        self.CACHE.update(d)

        data = self.CACHE.get(guid)

        if data is None:
            self.NO_STORE.update({guid:None})

        return data

class PGISTileHandler(tornado.web.RequestHandler):
    def initialize(self,st):
        self.st = st

    def get(self):
        x,y = int(self.get_argument("Col")),int(self.get_argument("Row"))
        z = int(self.get_argument("Zoom"))+int(self.get_argument("ZoomOffset"))
        tile = self.st.get("jiangsu",x,y,z)
        if tile is None:
            self.write(blank)
            return
        self.set_header("Content-Type", "image/png")
        self.write(str(tile))
        return

class TMSTileHandler(tornado.web.RequestHandler):
    def initialize(self,st):
        self.st = st

    def get(self, x, y, z):
        tile = self.st.get("layer", int(x), int(y), int(z))
        self.set_header("Content-Type", "image/png")
        if tile is None:
            self.write(blank)
            return
        self.write(str(tile))
        return


if __name__ == '__main__':
    import tornado.ioloop
    import tornado.web
    from tornado import httpserver

    st = SQLiteTile("huizhou.sqlite")
    st.open()
    # dta = st.get("jiangsu",481,126,11)
    # print str(dta)
    handlers = [
        (r"/tiles",PGISTileHandler,{"st":st},),
        (r"/TMS/(\w+)/(\w+)/(\w+)",TMSTileHandler,{"st":st},)
    ]

    application = tornado.web.Application(handlers)
    
    http_server = httpserver.HTTPServer(application)
    http_server.listen(9001)
    tornado.ioloop.IOLoop.instance().start()
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from email import charset

import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipelines(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path = value['path']
        item["front_image_path"] = image_file_path
        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

class JsonExporterPipleline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class MysqlPiplines(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', 'root', 'test', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """insert into tb_jobblog(title, url, create_date, fav_nums)  VALUES (%s, %s, %s, %s)"""
        # print("66666"+item)
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()

class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
       dbparms =  dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            password = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
       dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
       return cls(dbpool)

    def process_item(self, item, spider):

        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)

    def handle_error(self,failure,item,spider):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = """insert into tb_jobblog(title, url, create_date, fav_nums)  VALUES (%s, %s, %s, %s)"""
        # print("66666"+item)
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))

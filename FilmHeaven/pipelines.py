# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql


# 存入MySQL
class MySQLPipeline(object):
    # 初始化
    def __init__(self, host, port, user, password, db, charset):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    # 从配置中取东西
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("HOST"),
            port=crawler.settings.get("PORT"),
            user=crawler.settings.get("USER"),
            password=crawler.settings.get("PASSWORD"),
            db=crawler.settings.get("DB"),
            charset=crawler.settings.get("CHARSET")
        )

    # 打开爬虫
    def open_spider(self, spider):
        # 连接数据库
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset=self.charset)

        # 创建游标
        self.cursor = self.conn.cursor()

    # 爬虫中
    def process_item(self, item, spider):

        # sql语句
        sql = 'insert into dytt values (NULL,"{}","{}","{}","{}","{}")'.format(item['name'], item['data'], item['haibao'], item['info'], item['zhongzi'])

        print("李易阳：", sql)

        # 开始
        self.conn.begin()
        # 执行
        self.cursor.execute(sql)
        # 提交
        self.conn.commit()
        # 返回item
        return item

    # 关闭爬虫
    def close_spider(self, spider):
        # 关闭数据库链接
        self.cursor.close()
        self.conn.close()


# 存入MongoDB
class MongoDBPipeline(object):
    # 初始化
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    # 开启爬虫的时候初始化操作
    def open_spider(self, spider):
        # 连接mongodb
        self.client = pymongo.MongoClient(self.mongo_uri)
        # 相当于mysql的游标
        # 找到数据库
        self.db = self.client[self.mongo_db]

    # 爬虫进行中
    def process_item(self, item, spider):
        name = item.__class__.__name__
        print("李旺东：", name)
        # print("item['text']==", item["text"])
        # print("item['author']==", item["author"])
        # print("item['tags']==", item["tags"])
        self.db[name].insert(dict(item))
        return item

    # 关闭爬虫
    def close_spider(self, spider):
        self.client.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from .items import HomePageItem, HomePageInfoItem, PersonalInfoItem, PersonalProfileItem, PersonalWeiboItem, PersonalFollowItem, PersonalFollowerItem, PersonalWeiboCommentItem
import pymongo


class MongoDBPipeline(object):
    '''
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['Sina']
        self.HomePageItem = db['HomePageItem']
        self.HomePageInfoItem = db['HomePageInfoItem']
        self.PersonalInfoItem= db['PersonalInfoItem']

    def process_item(self, item, spider):
        if isinstance(item, HomePageItem):
            try:
                self.HomePageItem.insert_one(dict(item))
                print('Insert Successfuly')
            except Exception:
                print('HomePageItem is insert Failed')

        if isinstance(item, HomePageInfoItem):
            try:
                self.HomePageInfoItem.insert_one(dict(item))
                print('Insert Successfuly')
            except Exception:
                print('HomePageInfoItem is insert Failed')

        if isinstance(item, PersonalInfoItem):
            try:
                self.PersonalInfoItem.insert_one(dict(item))
                print('Insert Successfuly')
            except Exception:
                print('PersonalInfoItem is insert Failed')

        return item
    '''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'Sina')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, HomePageItem):
            try:
                self.db['HomePageItem'].insert_one(dict(item))
                print('Insert Successfuly')
            except Exception:
                print('HomePageItem is insert Failed')

        if isinstance(item, HomePageInfoItem):
            try:
                self.db['HomePageInfoItem'].insert_one(dict(item))
                print('HomePageInfoItem is inserted Successfuly')
            except Exception:
                print('HomePageInfoItem is inserted Failed')

        if isinstance(item, PersonalInfoItem):
            try:
                self.db['PersonalInfoItem'].insert_one(dict(item))
                print('PersonalInfoItem is inserted Successfuly')
            except Exception as e:
                print(e.with_traceback)
                print('PersonalInfoItem is inserted Failed')

        if isinstance(item, PersonalProfileItem):
            try:
                self.db['PersonalProfileItem'].insert_one(dict(item))
                print('PersonalProfileItem is inserted Successfuly')
            except Exception as e:
                print(e.with_traceback)
                print('PersonalProfileItem is inserted Failed')

        if isinstance(item, PersonalWeiboItem):
            try:
                self.db['PersonalWeiboItem'].insert_one(dict(item))
                print('PersonalWeiboItem is inserted Successfuly')
            except Exception as e:
                print(e.with_traceback)
                print('PersonalWeiboItem is inserted Failed')

        if isinstance(item, PersonalFollowItem):
            try:
                self.db['PersonalFollowItem'].insert_one(dict(item))
                print('PersonalFollowItem is inserted Successfuly')
            except Exception as e:
                print(e.with_traceback)
                print('PersonalFollowItem is inserted Failed')

        if isinstance(item, PersonalFollowerItem):
            try:
                self.db['PersonalFollowerItem'].insert_one(dict(item))
                print('PersonalFollowerItem is inserted Successfuly')
            except Exception as e:
                print(e.with_traceback)
                print('PersonalFollowerItem is inserted Failed')

        if isinstance(item, PersonalFollowerItem):
            try:
                self.db['PersonalWeiboCommentItem'].insert_one(dict(item))
                print('PersonalWeiboCommentItem is inserted Successfuly')
            except Exception as e:
                print(e.with_traceback)
                print('PersonalWeiboCommentItem is inserted Failed')

        return item

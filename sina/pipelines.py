# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from .items import HomePageItem, HomePageInfoItem, PersonalInfoItem


class MongoDBPipeline(object):
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

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from .items import HomePageItem, HomePageInfoItem, InformationItem


class MongoDBPipeline(object):
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['Sina']
        self.HomePageItem = db['HomePageItem']
        self.HomePageInfoItem = db['HomePageInfoItem']
        self.InformationItem = db['InformationItem']

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

        if isinstance(item, InformationItem):
            try:
                self.InformationItem.insert_one(dict(item))
                print('Insert Successfuly')
            except Exception:
                print('InformationItem is insert Failed')

        return item

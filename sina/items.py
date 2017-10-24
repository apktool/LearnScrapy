# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LearnscrapyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class InformationItem(Item):
    _id = Field()
    nickname = Field()
    authorization = Field()
    label = Field()
    gender = Field()
    place = Field()
    profile = Field()
    school = Field()
    blog = Field()
    level = Field()
    credit = Field()
    register = Field()

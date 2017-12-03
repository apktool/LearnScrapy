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


class HomePageItem(Item):
    blogger_name = Field()
    content = Field()
    detail = Field()

    upvote = Field()
    forward = Field()
    comment = Field()
    from_media = Field()

    photo_link = Field()
    multi_photo_link = Field()
    multi_photo_count = Field()

    original_blogger_name = Field()
    original_content = Field()
    original_upvote = Field()
    original_forward = Field()
    original_comment = Field()
    forward_reason = Field()

    original_at_people = Field()
    at_people = Field()


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

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
    servertime = Field()
    page_id = Field()
    location = Field()
    scheme = Field()
    sex = Field()
    colors_type = Field()
    miyou = Field()
    oid = Field()
    version = Field()
    onick = Field()
    bpType = Field()
    webim = Field()
    mCssPath = Field()
    isKrMember = Field()
    nick = Field()
    timeDiff = Field()
    brand = Field()
    avatar_large = Field()
    timeweibo = Field()
    mJsPath = Field()
    isAuto = Field()
    skin = Field()
    imgPath = Field()
    pageid = Field()
    bigpipe = Field()
    background = Field()
    watermark = Field()
    lang = Field()
    islogin = Field()
    cssPath = Field()
    jsPath = Field()
    uid = Field()
    title_value = Field()
    domain = Field()
    isVmember = Field()

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

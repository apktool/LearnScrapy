import scrapy
from scrapy_redis.spiders import RedisSpider
from sina.items import PersonalWeiboCommentItem, ErrorRquestItem
from sina.weibo_id import weibo_id
import json

import pymongo
from scrapy.utils.project import get_project_settings


class SinaSpider(RedisSpider):
    name = "SinaPersonalWeiboComment"
    redis_key = 'sina_personal_weibo_comment:start_urls'
    start_urls = list(set(weibo_id))
    url = 'https://m.weibo.cn/api/container/getIndex?'
    params = dict()
    mongo_uri = str()
    mongo_db = str()
    mongo_collection = dict()

    def connect_mongodb(self):
        settings = get_project_settings()
        self.mongo_uri = settings.get('MONGO_URI')
        self.mongo_db = settings.get('MONGO_DATABASE')
        self.db = pymongo.MongoClient(self.mongo_uri)[self.mongo_db]['PersonalWeiboItem']
        self.mongo_collection = self.db.find()

    def start_requests(self):
        self.connect_mongodb()
        for collection in self.mongo_collection:
            for entry in collection.get('cards'):
                mid = entry.get('mblog').get('mid')
                for page in range(10):
                    comment_url = 'https://m.weibo.cn/api/comments/show?id=' + mid + '&page=' + str(page)
                    yield scrapy.Request(url=comment_url, meta={'mid': mid}, callback=self.parse_personal_weibo_comment)

    def parse_personal_weibo_comment(self, response):
        self.logger.info('Parse function called on %s', response.url)

        error_request_item = ErrorRquestItem()
        if response.status == 418 or response.status == 404:
            print(response.url)
            ids = self.params['luicode'] + '#' + response.url.split('=')[-1]
            error_request_item['_id'] = ids
            error_request_item['response_status'] = response.status
            error_request_item['request_url'] = response.request.url
            yield error_request_item
            return

        jsonresponse = json.loads(response.body_as_unicode())
        personal_weibo_comment_item = PersonalWeiboCommentItem()
        personal_weibo_comment_item['_id'] = str(response.meta.get('mid')) + '#' + str(response.url.split('=')[-1])
        personal_weibo_comment_item['msg'] = jsonresponse.get('msg')
        personal_weibo_comment_item['data'] = jsonresponse.get('data')
        personal_weibo_comment_item['ok'] = jsonresponse.get('ok')

        if personal_weibo_comment_item['ok'] == 1:
            yield personal_weibo_comment_item

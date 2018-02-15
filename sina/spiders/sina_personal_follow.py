import scrapy
from scrapy_redis.spiders import RedisSpider
from sina.items import PersonalFollowItem, ErrorRquestItem
from sina.weibo_id import weibo_id
import json

import pymongo
from scrapy.utils.project import get_project_settings


class SinaSpider(RedisSpider):
    name = "SinaPersonalFollow"
    redis_key = 'sina_personal_follow:start_urls'
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
        self.db = pymongo.MongoClient(self.mongo_uri)[self.mongo_db]['PersonalInfoItem']
        self.mongo_collection = self.db.find()

    def start_requests(self):
        self.connect_mongodb()
        for collection in self.mongo_collection:
            follow_scheme = collection.get('follow_scheme')
            ids = collection.get('_id')
            follow_url = follow_scheme.replace('https://m.weibo.cn/p/index?', 'https://m.weibo.cn/api/container/getIndex?').replace('followersrecomm', 'follow')
            # TODO
            # follow, follows, follower, followers, fan, fans
            follow_count = collection.get('user_info').get('follow_count')

            for i in range(1, int(follow_count / 20 + 1)):
                temp = follow_url + '&page=%d' % i
                print(temp)
                yield scrapy.Request(url=temp, meta={'ids': ids}, callback=self.parse_personal_follow)

    def parse_personal_follow(self, response):
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
        personal_follow_item = PersonalFollowItem()
        personal_follow_item['_id'] = str(response.meta.get('ids')) + '#' + str(response.url.split('=')[-1])
        personal_follow_item['card_list_info'] = jsonresponse.get('data').get('cardlistInfo')
        personal_follow_item['cards'] = jsonresponse.get('data').get('cards')
        personal_follow_item['ok'] = jsonresponse.get('data').get('ok')

        yield personal_follow_item

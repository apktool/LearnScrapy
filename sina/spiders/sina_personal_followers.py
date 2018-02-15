import scrapy
from scrapy_redis.spiders import RedisSpider
from sina.items import PersonalFollowersItem, ErrorRquestItem
from sina.weibo_id import weibo_id
import json
import pymongo
from scrapy.utils.project import get_project_settings


class SinaSpider(RedisSpider):
    name = "SinaPersonalFollowers"
    redis_key = 'sina_personal_followers:start_urls'
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
            followers_scheme = collection.get('fans_scheme')
            ids = collection.get('_id')
            followers_url = followers_scheme.replace('https://m.weibo.cn/p/index?', 'https://m.weibo.cn/api/container/getIndex?').replace('fansrecomm', 'followers')
            # TODO
            # follow, follows, follower, followers, fan, fans
            followers_count = collection.get('user_info').get('followers_count')
            # Maybe it is error here, followers_count is not amount of followers

            for i in range(1, int(followers_count / 20 + 1)):
                temp = followers_url + '&page=%d' % i
                yield scrapy.Request(url=temp, meta={'ids': ids}, callback=self.parse_personal_followers)

    def parse_personal_followers(self, response):
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
        personal_followers_item = PersonalFollowersItem()
        personal_followers_item['_id'] = str(response.meta.get('ids')) + '#' + str(response.url.split('=')[-1])
        personal_followers_item['card_list_info'] = jsonresponse.get('data').get('cardlistInfo')
        personal_followers_item['cards'] = jsonresponse.get('data').get('cards')
        personal_followers_item['ok'] = jsonresponse.get('data').get('ok')

        yield personal_followers_item

import scrapy
from scrapy_redis.spiders import RedisSpider
from sina.items import PersonalProfileItem, ErrorRquestItem
from sina.weibo_id import weibo_id
from urllib.parse import urlencode, quote
import json


class SinaSpider(RedisSpider):
    name = "SinaPersonalProfile"
    redis_key = 'sina_personal_profile:start_urls'
    start_urls = list(set(weibo_id))
    url = 'https://m.weibo.cn/api/container/getIndex?'
    params = dict()

    def start_requests(self):
        for uid in self.start_urls:
            self.params.clear()
            self.params['containerid'] = '230283%d' % uid + '_-_INFO'
            self.params['title'] = quote('基本信息')
            self.params['luicode'] = '10000011'
            self.params['lfid'] = '230283%d' % uid
            self.params['featurecode'] = '20000320'
            url = self.url + urlencode(self.params)
            yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_profile)

    def parse_personal_profile(self, response):
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
        personal_profile_item = PersonalProfileItem()
        personal_profile_item['_id'] = str(response.meta.get('uid'))
        personal_profile_item['ok'] = jsonresponse.get('ok')
        personal_profile_item['card_list_info'] = jsonresponse.get('data').get('cardlistInfo')
        personal_profile_item['cards'] = jsonresponse.get('data').get('cards')
        yield personal_profile_item

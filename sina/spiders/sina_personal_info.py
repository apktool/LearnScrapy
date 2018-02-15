import scrapy
from scrapy_redis.spiders import RedisSpider
from sina.items import PersonalInfoItem, ErrorRquestItem
from sina.weibo_id import weibo_id
from urllib.parse import urlencode
import json


class SinaSpider(RedisSpider):
    name = "SinaPersonalInfo"
    redis_key = 'sina_personal_info:start_urls'
    start_urls = list(set(weibo_id))
    url = 'https://m.weibo.cn/api/container/getIndex?'
    params = dict()
    handle_httpstatus_list = [404, 405, 418]

    def start_requests(self):
        for uid in self.start_urls:
            self.params.clear()
            # self.params['luicode'] = '20000174'
            self.params['type'] = 'uid'
            # self.params['uid'] = uid
            self.params['value'] = uid
            self.params['containerid'] = '100505%d' % uid
            url = self.url + urlencode(self.params)
            yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_info)

    def parse_personal_info(self, response):
        self.logger.info('Parse function called on %s', response.url)
        # print(response.request.headers)
        # print(response.headers)

        error_request_item = ErrorRquestItem()
        if response.status == 418 or response.status == 404:
            ids = self.params['luicode'] + '#' + response.url.split('=')[-1]
            error_request_item['_id'] = ids
            error_request_item['response_status'] = response.status
            error_request_item['request_url'] = response.request.url
            yield error_request_item
            return

        if response.status == 405:
            print(response.request.url)

        jsonresponse = json.loads(response.body_as_unicode())
        personal_info_item = PersonalInfoItem()
        personal_info_item['_id'] = response.meta.get('uid')
        personal_info_item['tabs_info'] = jsonresponse.get('data').get('tabsInfo')
        personal_info_item['user_info'] = jsonresponse.get('data').get('userInfo')
        personal_info_item['fans_scheme'] = jsonresponse.get('data').get('fans_scheme')
        personal_info_item['follow_scheme'] = jsonresponse.get('data').get('follow_scheme')
        yield personal_info_item

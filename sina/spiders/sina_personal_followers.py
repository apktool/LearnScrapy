import scrapy
from scrapy_redis.spiders import RedisSpider
from sina.items import PersonalFollowersItem, ErrorRquestItem
from sina.weibo_id import weibo_id
import json

import pymongo
from scrapy.utils.project import get_project_settings
from urllib.parse import urlencode


class SinaSpider(RedisSpider):
    name = "SinaPersonalFollowers"
    redis_key = 'sina_personal_followers:start_urls'
    start_urls = list(set(weibo_id))
    basic_url = 'https://m.weibo.cn/api/container/getSecond?'
    params = dict()
    handle_httpstatus_list = [403, 404, 418]

    page = 0
    max_page = 100

    def start_requests(self):
        for uid in self.start_urls:
            if self.page < self.max_page:
                self.params.clear()
                self.params['containerid'] = '100505%d' % uid + '_-_FANS'
                self.params['page'] = self.page + 1

                url = self.basic_url + urlencode(self.params)
                yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_follow)

    def parse_personal_follow(self, response):
        self.logger.info('Parse function called on %s', response.url)

        error_request_item = ErrorRquestItem()
        if response.status == 418 or response.status == 404:
            print(response.url)
            error_request_item['_id'] = 'followers#%s#%s' % (response.meta.get('uid'), response.url.split('=')[-1])
            error_request_item['response_status'] = response.status
            error_request_item['request_url'] = response.request.url
            yield error_request_item
            return

        if response.status == 403:
            print(response.url)

        jsonresponse = json.loads(response.body_as_unicode())
        personal_followers_item = PersonalFollowersItem()
        personal_followers_item['_id'] = str(response.meta.get('uid')) + '#' + str(response.url.split('=')[-1])
        personal_followers_item['data'] = jsonresponse.get('data')
        personal_followers_item['ok'] = jsonresponse.get('ok')

        self.max_page = jsonresponse.get('data').get('maxPage')

        yield personal_followers_item

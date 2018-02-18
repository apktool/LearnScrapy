import scrapy
from scrapy_redis.spiders import RedisSpider
from sina.items import PersonalFollowItem, ErrorRquestItem
from sina.weibo_id import weibo_id
from urllib.parse import urlencode
import json


class SinaSpider(RedisSpider):
    name = "SinaPersonalFollow"
    redis_key = 'sina_personal_follow:start_urls'
    start_urls = list(set(weibo_id))
    basic_url = 'https://m.weibo.cn/api/container/getSecond?'
    params = dict()
    handle_httpstatus_list = [403, 404, 418]

    def start_requests(self):
        for uid in self.start_urls:
            self.params.clear()
            self.params['containerid'] = '100505%d' % uid + '_-_FOLLOWERS'
            for page in range(1, 100):
                self.params['page'] = page
                url = self.basic_url + urlencode(self.params)
                yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_follow)

    def parse_personal_follow(self, response):
        self.logger.info('Parse function called on %s', response.url)

        error_request_item = ErrorRquestItem()
        if response.status == 418 or response.status == 404:
            print(response.url)
            # follow#uid#page
            error_request_item['_id'] = 'follow#%s#%s' % (response.meta.get('uid'), response.url.split('=')[-1])
            error_request_item['response_status'] = response.status
            error_request_item['request_url'] = response.request.url
            yield error_request_item
            return

        if response.status == 403:
            print(response.url)

        jsonresponse = json.loads(response.body_as_unicode())
        personal_follow_item = PersonalFollowItem()
        personal_follow_item['_id'] = str(response.meta.get('uid')) + '#' + str(response.url.split('=')[-1])
        personal_follow_item['data'] = jsonresponse.get('data')
        personal_follow_item['ok'] = jsonresponse.get('ok')

        if personal_follow_item['ok'] == 0:
            return

        yield personal_follow_item

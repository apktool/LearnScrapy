import scrapy
from scrapy_redis.spiders import RedisSpider
from sina.items import PersonalWeiboItem, ErrorRquestItem
from sina.weibo_id import weibo_id
from urllib.parse import urlencode
import json


class SinaSpider(RedisSpider):
    name = "SinaPersonalWeibo"
    redis_key = 'sina_personal_weibo:start_urls'
    start_urls = list(set(weibo_id))
    basic_url = 'https://m.weibo.cn/api/container/getIndex?'
    handle_httpstatus_list = [400, 404, 405, 418]
    params = dict()

    def start_requests(self):
        for uid in self.start_urls:
            self.params.clear()
            self.params['type'] = 'uid'
            self.params['value'] = uid
            self.params['containerid'] = '107603%d' % uid
            for page in range(1, 100):
                self.params['page'] = page
                url = self.basic_url + urlencode(self.params)
                yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_weibo)

    def parse_personal_weibo(self, response):
        self.logger.info('Parse function called on %s', response.url)
        # print(response.request.headers)
        # print(response.headers)

        error_request_item = ErrorRquestItem()
        if response.status == 418 or response.status == 404:
            error_request_item['_id'] = 'weibo#%s#%s' % (response.meta.get('uid'), response.url.split('=')[-1])
            error_request_item['response_status'] = response.status
            error_request_item['request_url'] = response.request.url
            yield error_request_item
            return

        if response.status == 405:
            print(url)
            print(response.request.url)

        jsonresponse = json.loads(response.body_as_unicode())
        personal_weibo_item = PersonalWeiboItem()
        personal_weibo_item['_id'] = '%s#%s' % (response.meta.get('uid'), response.url.split('=')[-1])
        personal_weibo_item['data'] = jsonresponse.get('data')
        personal_weibo_item['ok'] = jsonresponse.get('ok')

        if personal_weibo_item['ok'] == 0:
            return

        yield personal_weibo_item

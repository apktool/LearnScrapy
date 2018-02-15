import scrapy
from scrapy_redis.spiders import RedisSpider
from sina.items import PersonalWeiboItem, ErrorRquestItem
from sina.weibo_id import weibo_id
from urllib.parse import urlencode, quote
import json


class SinaSpider(RedisSpider):
    name = "SinaPersonalWeibo"
    redis_key = 'sina_personal_weibo:start_urls'
    start_urls = list(set(weibo_id))
    url = 'https://m.weibo.cn/api/container/getIndex?'
    params = dict()
    stop_flag = False
    handle_httpstatus_list = [404, 405, 418]

    def start_requests(self):
        for uid in self.start_urls:
            self.params.clear()
            self.params['luicode'] = '20000174'
            self.params['type'] = 'uid'
            self.params['uid'] = uid
            self.params['value'] = uid
            self.params['containerid'] = '107603%d' % uid
            for page in range(1, 100):
                if self.stop_flag == False:
                    url = self.url + urlencode(self.params) + '&page=%d' % page
                    yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_weibo)
                else:
                    print('The amount of %s\' weibo is not enough')
                    break

    def parse_personal_weibo(self, response):
        self.logger.info('Parse function called on %s', response.url)
        # print(response.request.headers)
        # print(response.headers)
        error_request_item = ErrorRquestItem()

        if response.status == 418 or response.status == 404:
            ids = self.params['luicode'] + '#' + self.params['containerid'] + '#' + response.url.split('=')[-1]
            error_request_item['_id'] = ids
            error_request_item['response_status'] = response.status
            error_request_item['request_url'] = response.request.url
            yield error_request_item
            return

        if response.status == 405:
            print(response.request.url)

        jsonresponse = json.loads(response.body_as_unicode())
        personal_weibo_item = PersonalWeiboItem()
        uid = str(response.meta.get('uid'))
        personal_weibo_item['_id'] = uid + '#' + str(response.url.split('=')[-1])
        personal_weibo_item['ok'] = jsonresponse.get('ok')
        personal_weibo_item['card_list_info'] = jsonresponse.get('data').get('cardlistInfo')
        personal_weibo_item['cards'] = jsonresponse.get('data').get('cards')

        if personal_weibo_item['ok'] == 1:
            count = len(personal_weibo_item['cards'])
            if count == 0:
                self.stop_flag = True
            else:
                yield personal_weibo_item

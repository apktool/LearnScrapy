import scrapy
from sina.items import PersonalInfoItem, PersonalWeiboItem
from sina.weibo_id import weibo_id
from urllib.parse import urlencode
import json


class SinaSpider(scrapy.Spider):
    name = "sinaPersonalInfo"
    url = 'https://m.weibo.cn/api/container/getIndex?'
    params = {
            'uid': '',
            'luicode': '20000174',
            'type': 'uid',
            'value': '',
            'containerid': ''
            }

    def start_requests(self):
        for uid in weibo_id:
            self.params['uid'] = uid
            self.params['value'] = uid

            self.params['containerid'] = '107603%d' % uid
            for page in range(10):
                url = self.url + urlencode(self.params) + '&page=%d' % page
                yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_weibo)

            self.params['containerid'] = '100505%d' % uid
            url = self.url + urlencode(self.params)
            yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_info)

    def parse_personal_weibo(self, response):
        self.logger.info('Parse function called on %s', response.url)
        # print(response.request.headers)
        # print(response.headers)

        jsonresponse = json.loads(response.body_as_unicode())
        personal_weibo_item = PersonalWeiboItem()
        personal_weibo_item['_id'] = str(response.meta.get('uid')) + '#' + str(response.url.split('=')[-1])
        personal_weibo_item['ok'] = jsonresponse.get('ok')
        personal_weibo_item['card_list_info'] = jsonresponse.get('data').get('cardlistInfo')
        personal_weibo_item['cards'] = jsonresponse.get('data').get('cards')

        if personal_weibo_item['ok'] == 1:
            yield personal_weibo_item

    def parse_personal_info(self, response):
        self.logger.info('Parse function called on %s', response.url)
        # print(response.request.headers)
        # print(response.headers)

        jsonresponse = json.loads(response.body_as_unicode())
        personal_info_item = PersonalInfoItem()
        personal_info_item['_id'] = response.meta.get('uid')
        personal_info_item['tabs_info'] = jsonresponse.get('data').get('tabsInfo')
        personal_info_item['user_info'] = jsonresponse.get('data').get('userInfo')
        personal_info_item['fans_scheme'] = jsonresponse.get('data').get('fans_scheme')
        personal_info_item['follow_scheme'] = jsonresponse.get('data').get('follow_scheme')
        yield personal_info_item

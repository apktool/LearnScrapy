import scrapy
from sina.items import PersonalInfoItem
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
            self.params['containerid'] = '100505%d' % uid
            url = self.url + urlencode(self.params)
            yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_home)

    def parse_home(self, response):
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

import scrapy
from scrapy_redis.spiders import RedisSpider
from sina.items import PersonalInfoItem, PersonalWeiboItem, PersonalFollowItem, PersonalFollowerItem, PersonalInfoDetailItem
from sina.weibo_id import weibo_id
from urllib.parse import urlencode, quote
import json


class SinaSpider(RedisSpider):
    name = "sinaPersonalInfo"
    redis_key = 'sina_personal_info:start_urls'
    start_urls = list(set(weibo_id))
    url = 'https://m.weibo.cn/api/container/getIndex?'
    params = dict()

    def start_requests(self):
        for uid in self.start_urls:
            self.params.clear()
            self.params['luicode'] = '20000174'
            self.params['type'] = 'uid'
            self.params['uid'] = uid
            self.params['value'] = uid
            self.params['containerid'] = '107603%d' % uid
            for page in range(1, 10):
                url = self.url + urlencode(self.params) + '&page=%d' % page
                yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_weibo)

            self.params['containerid'] = '100505%d' % uid
            url = self.url + urlencode(self.params)
            yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_info)

            self.params.clear()
            self.params['containerid'] = '230283%d' % uid + '_-_INFO'
            self.params['title'] = quote('基本信息')
            self.params['luicode'] = '10000011'
            self.params['lfid'] = '230283%d' % uid
            self.params['featurecode'] = '20000320'
            url = self.url + urlencode(self.params)
            yield scrapy.Request(url=url, meta={'uid': uid}, callback=self.parse_personal_info_detail)

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

    def parse_personal_info_detail(self, response):
        self.logger.info('Parse function called on %s', response.url)
        jsonresponse = json.loads(response.body_as_unicode())
        personal_info_detial_item = PersonalInfoDetailItem()
        personal_info_detial_item['_id'] = str(response.meta.get('uid')) + '#' + str(response.url.split('=')[-1])
        personal_info_detial_item['ok'] = jsonresponse.get('ok')
        personal_info_detial_item['card_list_info'] = jsonresponse.get('data').get('cardlistInfo')
        personal_info_detial_item['cards'] = jsonresponse.get('data').get('cards')
        yield personal_info_detial_item

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

        # 粉丝
        followers_count = jsonresponse.get('data').get('userInfo').get('followers_count')
        for i in range(1, int(followers_count/20 + 1)):
            url_follower = personal_info_item['fans_scheme']
            url_follower = url_follower.replace('https://m.weibo.cn/p/index?', self.url)
            url_follower = url_follower.replace('fansrecomm', 'fans')
            url_follower = url_follower + '&since_id=%d' % i
            yield scrapy.Request(url=url_follower, meta={'uid': personal_info_item['_id']}, callback=self.parse_personal_follower)

        # 关注
        follow_count = jsonresponse.get('data').get('userInfo').get('follow_count')
        for i in range(1, int(follow_count/20 + 1)):
            url_follow = personal_info_item['follow_scheme']
            url_follow = url_follow.replace('https://m.weibo.cn/p/index?', self.url)
            url_follow = url_follow.replace('followersrecomm', 'followers')
            url_follow = url_follow + '&page=%d' % i
            yield scrapy.Request(url=url_follow, meta={'uid': personal_info_item['_id']}, callback=self.parse_personal_follow)

    def parse_personal_follower(self, response):
        self.logger.info('Parse function called on %s', response.url)

        jsonresponse = json.loads(response.body_as_unicode())
        personal_follower_item = PersonalFollowerItem()
        personal_follower_item['_id'] = str(response.meta.get('uid')) + '#' + str(response.url.split('=')[-1])
        personal_follower_item['card_list_info'] = jsonresponse.get('data').get('cardlistInfo')
        personal_follower_item['cards'] = jsonresponse.get('data').get('cards')
        personal_follower_item['ok'] = jsonresponse.get('data').get('ok')

        yield personal_follower_item

    def parse_personal_follow(self, response):
        self.logger.info('Parse function called on %s', response.url)

        jsonresponse = json.loads(response.body_as_unicode())
        personal_follow_item = PersonalFollowItem()
        personal_follow_item['_id'] = str(response.meta.get('uid')) + '#' + str(response.url.split('=')[-1])
        personal_follow_item['card_list_info'] = jsonresponse.get('data').get('cardlistInfo')
        personal_follow_item['cards'] = jsonresponse.get('data').get('cards')
        personal_follow_item['ok'] = jsonresponse.get('data').get('ok')

        yield personal_follow_item

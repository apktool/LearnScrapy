import scrapy
from sina.items import PersonalInfoItem
from sina.weibo_id import weibo_id


class SinaSpider(scrapy.Spider):
    name = "sinaPersonalInfo"
    url = 'https://weibo.cn/'
    host = url + '%s/info'
    tags = url + 'account/privacy/tags/?uid=%s'

    def start_requests(self):
        # cookies = get_cookies()[0]
        for item in weibo_id:
            host_url = self.host % str(item)
            yield scrapy.Request(url=host_url, callback=self.parse_home, priority=0)

    def parse_home(self, response):
        self.logger.info('Parse function called on %s', response.url)
        # print(response.request.headers)
        # print(response.headers)
        with open('c.html', 'wb') as f:
            f.write(response.body)

        info = dict()
        other = list()
        contents = response.selector.xpath('//div[@class="c"]/text()').extract()
        for content in contents:
            content = content.replace('：', ':')
            item = content.split(':', 1)
            if len(item) == 2:
                info[item[0]] = item[1]
            else:
                other.append(content)

        g = lambda s: s and s != '\xa0' and s != '.' and s != '|' and s != '彩版|'
        other = list(filter(g, other))

        user_id = response.url.split('/')[-2]
        personal_info_item = PersonalInfoItem()
        personal_info_item['_id'] = user_id
        personal_info_item['level'] = info.get('会员等级')
        personal_info_item['nickname'] = info.get('昵称')
        personal_info_item['authorization'] = info.get('认证')
        personal_info_item['gender'] = info.get('性别')
        personal_info_item['place'] = info.get('地区')
        personal_info_item['birthday'] = info.get('生日')
        personal_info_item['sexual_orientation'] = info.get('性取向')
        personal_info_item['authorization_info'] = info.get('认证信息')
        personal_info_item['profile'] = info.get('简介')
        personal_info_item['pc_version'] = info.get('互联网')
        personal_info_item['mobile_version'] = info.get('手机版')
        personal_info_item['other'] = other

        tags_url = self.tags % str(user_id)
        yield scrapy.Request(url=tags_url, callback=self.parse_tags, meta={'item': personal_info_item}, priority=1)

    def parse_tags(self, response):
        self.logger.info('Parse function called on %s', response.url)
        with open('d.html', 'wb') as f:
            f.write(response.body)

        personal_info_item = response.meta.get('item')
        tags = response.selector.xpath('//div[@class="c"]/a/text()').extract()[1:-6]
        personal_info_item['label'] = tags

        yield personal_info_item

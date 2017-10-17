import scrapy
import json
from sina.items import InformationItem


class SinaSpider(scrapy.Spider):
    name = "sinaspider"

    def start_requests(self):
        urls = [
                # 'https://weibo.com/p/1005052185608961/info'
                'https://m.weibo.cn/p/index?containerid=2302832185608961_-_INFO'
                #'https://weibo.cn/5825708520/info'
        ]
        for url in urls:
            yield scrapy.Request(url=url, meta={'cookiejar': 0}, callback=self.getcookie)

    def getcookie(self, response):
            url = "https://m.weibo.cn/api/container/getIndex?containerid=2302832185608961_-_INFO"
            yield scrapy.Request(url=url, meta=response.meta['cookiejar'], callback=self.parse_information)

    def parse_information(self, response):
        text = response.body.decode('unicode_escape')
        content = json.loads(text)
        meta_data = dict()

        for card in content['cards']:
            for card_group in card['card_group']:
                key = card_group.get('item_name', '微博认证')
                value = card_group.get('item_content')
                meta_data[key] = value

        info_items = InformationItem()
        info_items['_id'] = '2302832185608961'
        info_items['nickname'] = meta_data.get('昵称')
        info_items['authorization'] = meta_data.get('微博认证')
        info_items['label'] = meta_data.get('标签')
        info_items['gender'] = meta_data.get('性别') 
        info_items['place'] = meta_data.get('所在地')
        info_items['profile'] = meta_data.get('简介')
        info_items['school'] = meta_data.get('学校')
        info_items['blog'] = meta_data.get('博客')
        info_items['level'] = meta_data.get('等级')
        info_items['credit'] = meta_data.get('阳光信用')
        info_items['register'] = meta_data.get('注册时间')

        yield info_items

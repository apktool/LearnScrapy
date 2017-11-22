import scrapy
import time
from sina.items import HomePageItem


class SinaSpider(scrapy.Spider):
    name = "sinaInformation"
    host = 'https://weibo.com/'

    def start_requests(self):
        yield scrapy.Request(url=self.host, callback=self.parse_home)

    def parse_home(self, response):
        self.logger.info('Parse function called on %s', response.url)
        with open('a.html', 'wb') as f:
            f.write(response.body)

        info = response.xpath('//script/text()').re(r'(CONFIG.*?);')
        CONFIG = HomePageItem()
        for item in info[:-1]:
            if "$webim" in item:
                item = item.replace('$', '', 1)
            if "CONFIG['timeDiff']" in item:
                item = item.replace('new Date()', str(int(time.time()*1000)))
            exec(item)
        self.logger.info('Parsing home page result is \n{}'.format(CONFIG))

        yield CONFIG

import scrapy


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
        filename = 'sina.json'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

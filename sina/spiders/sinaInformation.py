import scrapy


class SinaSpider(scrapy.Spider):
    name = "sinaInformation"
    host = 'https://weibo.com/'

    def start_requests(self):
        yield scrapy.Request(url=self.host, callback=self.parse)

    def parse(self, response):
        cookie = response.request.headers.getlist('Cookie')
        print(cookie)

        self.logger.info('Parse function called on %s', response.url)
        text = response.body
        with open('a.html', 'wb') as f:
            f.write(text)

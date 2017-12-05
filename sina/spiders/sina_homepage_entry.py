import scrapy
from sina.items import HomePageItem, HomePageInfoItem
from scrapy.selector import Selector


class SinaSpider(scrapy.Spider):
    name = "sinaHomeEntry"
    host = 'https://weibo.cn/'

    def start_requests(self):
        # cookies = get_cookies()[0]
        yield scrapy.Request(url=self.host, callback=self.parse_home)

    def parse_home(self, response):
        self.logger.info('Parse function called on %s', response.url)
        # print(response.request.headers)
        # print(response.headers)
        with open('a.html', 'wb') as f:
            f.write(response.body)

        # 个人首页 | 微博, 关注, 粉丝, @我的
        home_info_item = self.storage_home_info(response)
        yield home_info_item

        # 个人首页 | 博主，内容，评论，转发...
        home_item = self.storage_home_entry(response)
        yield home_item

    def storage_home_info(self, response):

        info_name = response.selector.xpath('//div[@class="tip2"]/a/text()').extract()
        info_link = response.selector.xpath('//div[@class="tip2"]/a/@href').extract()
        info = list()

        for i in range(len(info_name)):
            temp = list()
            temp.append(info_name[i])
            temp.append(info_link[i])
            info.append(temp)

        home_info_item = HomePageInfoItem()
        home_info_item['weibo_count'] = info[0]
        home_info_item['notic_count'] = info[1]
        home_info_item['follower_count'] = info[2]
        home_info_item['at_count'] = info[3]

        return home_info_item

    def storage_home_entry(self, response):
        weibo_unit = response.selector.xpath('//div[@class="c"]').extract()
        with open('b.html', 'a') as f:
            for item in weibo_unit:
                f.write(item + '\n\n\n')

        for body in weibo_unit[2:-2]:
            item_list = Selector(text=body).xpath('//div/a/text()').extract()
            home_item = HomePageItem()

            home_item['blogger_name'] = item_list[0]
            home_item['content'] = Selector(text=body).xpath('//span[@class="ctt"]/text()').extract()[0]

            # 只有一张图片
            if '原图' in item_list[1]:
                home_item['photo_link'] = Selector(text=body).xpath('//a/img/@src').extract()[-1]

            # 存在多张图片
            if '组图' in item_list[1]:
                home_item['multi_photo_link'] = Selector(text=body).xpath('//a[@href]').re('\"(.*?)\">组图')[-1]
                home_item['multi_photo_count'] = Selector(text=body).xpath('//a[@href]').re('组图共\d+张')[-1]

            # 转发微博
            if '原文评论' in item_list[3] or '原文评论' in item_list[1]:
                home_item['original_blogger_name'] = Selector(text=body).xpath('//span[@class="cmt"]/a/text()').extract()[-1]
                home_item['original_content'] = Selector(text=body).xpath('//span[@class="ctt"]/text()').extract()[0]
                home_item['original_upvote'] = Selector(text=body).xpath('//span[@class="cmt"]/text()').extract()[-3]
                home_item['original_forward'] = Selector(text=body).xpath('//span[@class="cmt"]/text()').extract()[-2]
                home_item['original_comment'] = Selector(text=body).xpath('//a[@class="cc"]/text()').extract()[0]
                forward_reason = Selector(text=body).xpath('//div/text()').re('\S+')
                if forward_reason[0] != '[':
                    home_item['forward_reason'] = forward_reason[0]
                else:
                    home_item['forward_reason'] = forward_reason[2]
                home_item['content'] = home_item['forward_reason']

            home_item['upvote'] = item_list[-4]
            home_item['forward'] = item_list[-3]
            home_item['comment'] = item_list[-2]
            home_item['from_media'] = Selector(text=body).xpath('//span[@class="ct"]/text()').extract()[0]

            original_at_people = Selector(text=body).xpath('//span[@class="ctt"]/a/text()').extract()
            if len(original_at_people):

                # print(original_at_people) # 可能是@people，也可能是全文link
                home_item['original_at_people'] = original_at_people

                home_item['detail'] = Selector(text=body).xpath('//span[@class="ctt"]/a/@href').extract()[-1]

            home_item['at_people'] = Selector(text=body).xpath('//a/text()').re('@\S+')
            return home_item

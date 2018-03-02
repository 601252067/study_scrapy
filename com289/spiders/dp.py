# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from dianping.items import DianpingItem

from scrapy.http.cookies import CookieJar


class DpSpider(scrapy.Spider):
    name = 'dp'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shop/67330730/review_all/p1']


    # 提取链接
    link_extractor = {
        'link_one': LinkExtractor(allow=r'/shop/67330730/review_all/p\d+'),
    }

    # 重发请求操作
    def parse(self, response):
        for link in self.link_extractor['link_one'].extract_links(response):
            yield scrapy.Request(url=link.url, callback=self.parse_page, meta={'cookiejar': 1},)

    # 数据提取操作
    def parse_page(self, response):
        item = DianpingItem()
        print(response.url)

        for each in response.xpath("//div[@class='reviews-items']/ul/li/div[@class='main-review']"):
            username = each.xpath("./div[@class='dper-info']/a[@class='name']/text()").extract()[0].replace('\n', '').replace(' ', '')
            taste = each.xpath(
                "./div[@class='review-rank']/span[@class='score']/span[@class='item'][1]/text()").extract()[0].replace('\n', '').replace(' ', '')
            environment = each.xpath("./div[@class='review-rank']/span[@class='score']/span[@class='item'][2]/text()").extract()[0].replace('\n', '').replace(' ', '')
            service = each.xpath("./div[@class='review-rank']/span[@class='score']/span[@class='item'][3]/text()").extract()[0].replace('\n', '').replace(' ', '')
            pre_data = each.xpath("./div[@class='review-rank']/span[@class='score']/span[@class='item'][4]/text()").extract()
            if len(pre_data) > 0:
                pre = pre_data[0].replace('\n', '').replace(' ', '')
            else:
                pre = 'Null'
            comment_data = each.xpath("./div[@class='review-truncated-words']/text()").extract()
            if len(comment_data) > 0:
                comment = comment_data[0].replace('\n', '').replace('\t', '').replace(' ', '')
            else:
                comment = 'Null'
            cre_time = each.xpath("./div[@class='misc-info clearfix']/span[@class='time']/text()").extract()[0].replace('\n', '')
            star = each.xpath("./div[@class='review-rank']/span[1]/@class").extract()[0].replace('sml-rank-stars','').replace('sml-str','').replace('star','').replace(' ','').replace('0','')
            item['username'] = username
            item['taste'] = taste
            item['environment'] = environment
            item['service'] = service
            item['pre'] = pre
            item['comment'] = comment
            item['cre_time'] = cre_time
            item['star'] = star
            print(item)
            yield item


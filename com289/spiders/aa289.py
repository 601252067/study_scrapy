# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from com289.items import Com289Item

class Aa289Spider(scrapy.Spider):
    name = 'aa289'
    allowed_domains = ['www.364bb.com']
    start_urls = ['https://www.364bb.com/htm/mp4list7/1.htm']

    link_extractor = {
        'link_one': LinkExtractor(allow=r'/htm/mp4list7/\d+.htm$'),
        'link_two': LinkExtractor(allow='/htm/mp47/\d+.htm$'),
    }

    def parse(self, response):
        for link in self.link_extractor['link_one'].extract_links(response):
            yield scrapy.Request(url=link.url, callback=self.prase_page)

    def prase_page(self, response):
        for link in self.link_extractor['link_two'].extract_links(response):
            yield scrapy.Request(url=link.url, callback=self.data_handle)

    def data_handle(self, response):
        item = Com289Item()
        name = response.xpath("//div[@id='main']/div[@class='container']/h3/text()").extract()
        if len(name) > 0:
            print(name[0])
        else:
            print('name null')

        link = response.xpath("//div[@class='endpage clearfixpage']/div[2]/ul/div/a[1]/@href").extract()
        if len(link) > 0:
            print(link[0])
        else:
            print('link null')

        item['name'] = name
        item['link'] = link
        yield item



import scrapy
import requests
import re


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://muaban.net/mua-ban-nha-dat-cho-thue-toan-quoc-l0-c3?cp=0']

    headers = {
    }

    def start_requests(self):
        return [scrapy.Request("https://muaban.net/mua-ban-nha-dat-cho-thue-toan-quoc-l0-c3?cp=0",
                               headers=self.headers,
                               callback=self.parse)]

    def parse(self, response):
        for title in response.css('a.mbn-image'):
            yield scrapy.Request(title.css('a::attr(href)').extract_first(),
                                 headers=self.headers,
                                 callback=self.parse_detail_page)
        for x in range(1, 200):
            yield scrapy.Request("https://muaban.net/mua-ban-nha-dat-cho-thue-toan-quoc-l0-c3?cp={0}".format(x),
                                 headers=self.headers,
                                 callback=self.parse)

    def parse_detail_page(self, response):
        m = re.search("([0-9]{2}\/[0-9]{2}\/[0-9]{4})", (response.css(
            '#dvContent > div.cl-price-sm.clearfix > div.detail-price-top > div > span.detail-clock').extract_first() or "").encode(
            'utf-8').strip())
        yield {
            'title': (response.css(
                '#dvContent > div.cl-title.clearfix > h1::text').extract_first() or "").encode('utf-8').strip(),
            'price': (response.css(
                '#dvContent > div.ct-price.clearfix > div.col-md-10.col-sm-10.col-xs-9.price-value > span::text').extract_first() or "").encode(
                'utf-8').strip(),
            'address': (response.css(
                '#dvContent > div.ct-contact.clearfix > div:nth-child(5)::text').extract_first() or "").encode(
                'utf-8').strip(),
            'phone': (response.css(
                '#dvContent > div.ct-contact.clearfix > div:nth-child(5) > b.size18.color000::text,#dvContent > div.ct-contact.clearfix > div:nth-child(8) > b.size18.color000::text,#dvContent > div.ct-contact.clearfix > div.col-md-10.col-sm-10.col-xs-9 > b.size18.color000::text') or "").extract_first().encode(
                'utf-8').strip(),
            'url': response.url,
            'date': m.group(1),
        }

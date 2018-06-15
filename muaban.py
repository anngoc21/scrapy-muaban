import scrapy
import requests


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://muaban.net/mua-ban-nha-dat-cho-thue-toan-quoc-l0-c3?cp=1']

    def parse(self, response):
        for title in response.css('a.mbn-image'):
            yield response.follow(
                title.css('a::attr(href)').extract_first(),
                self.parse_detail_page)

            for next_page in response.css(
                    '#page-wrap > div.main-container.lazy > div:nth-child(3) > div.mbn-body.container > div.mbn-box-left > div:nth-child(5) > div.paging > ul > li:nth-child(14) > a,#page-wrap > div.main-container.lazy > div:nth-child(3) > div.mbn-body.container > div.mbn-box-left > div:nth-child(5) > div.paging > ul > li:nth-child(12) > a'):
                yield response.follow(next_page, self.parse)

    def parse_detail_page(self, response):
        print response.url
        yield {'type': response.css(
            '#page-wrap > div.main-container.lazy > div:nth-child(2) > div > div > div > div.breadcrumb-left > div > span:nth-child(8) > a::text').extract(),
               'title': response.css(
                   '#dvContent > div.cl-title.clearfix > h1::text').extract_first(),
               # 'id': response.css(
               #     '#MainContent_ctlDetailBox_lblContactPhone > a::attr(data-phoneext)').extract_first(),
               'price': response.css(
                   '#dvContent > div.ct-price.clearfix > div.col-md-10.col-sm-10.col-xs-9.price-value > span::text').extract_first(),
               'address': response.css(
                   '#dvContent > div.ct-contact.clearfix > div:nth-child(5)::text').extract_first(),
               'phone': response.css(
                   '#dvContent > div.ct-contact.clearfix > div:nth-child(5) > b.size18.color000::text,#dvContent > div.ct-contact.clearfix > div:nth-child(8) > b.size18.color000::text,#dvContent > div.ct-contact.clearfix > div.col-md-10.col-sm-10.col-xs-9 > b.size18.color000').extract_first(),
               'url': response.url
               }

import scrapy
import requests


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://www.muabannhadat.vn/nha-dat-3490?p=208']

    def parse(self, response):
        for title in response.css('a.title-filter-link'):
            yield response.follow(
                "http://www.muabannhadat.vn{0}".format(title.css('a::attr(href)').extract_first()),
                self.parse_detail_page)

        for next_page in response.css('a#MainContent_ctlList_ctlResults_ctlPager_lnkNext'):
            yield response.follow(next_page, self.parse)

    def parse_detail_page(self, response):
        headers = {
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "vi,en-US;q=0.9,en;q=0.8",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Content-Length': "0",
            'Cookie': "_ga=GA1.2.498331714.1528966523; _gid=GA1.2.2030000603.1528966523; register-popup=true; stg_returning_visitor=Thu, 14 Jun 2018 09:24:40 GMT; __RequestVerificationToken=QWfggdWBi58xgEakB5qdMQmqtGPwpWUFIQaXH09YcaA9ohuX5D-i86rGWngv7AMDVOandEdJQbIcDc96Fy-3UXMVRW81; stg_traffic_source_priority=1; _sp_ses.be73=*; _sp_id.be73=83f55d39-2d03-4236-954f-3c0130f2e79c.1528966524.6.1529056892.1529045862.5522f4c2-ad06-4f20-9459-2a4cb55b8a78; stg_last_interaction=Fri, 15 Jun 2018 10:02:17 GMT",
            'Host': "www.muabannhadat.vn",
            'Origin': "http://www.muabannhadat.vn",
            'Pragma': "no-cache",
            'Referer': "http://www.muabannhadat.vn/dat-ban-dat-tho-cu-3532/ban-gap-dat-tho-cu-cho-viet-kieu-tan-thong-hoi-cu-7217833",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
            'Postman-Token': "e44d0a09-c551-42d2-9c26-5802f203c255"
        }

        res = requests.request("POST", 'http://www.muabannhadat.vn/Services/Tracking/a{0}/GetPhoneCustom'.format(
            response.css(
                '#MainContent_ctlDetailBox_lblContactPhone > a::attr(data-phoneext)').extract_first()), headers=headers)
        print response
        yield {'type': response.css('p.cusp::text').extract(),
               'title': response.css(
                   '#ctl01 > div.body-content > div.container.padding-top-custom-devive > div > div > div > div.col-md-10.col-sm-8.col-xs-12.nav-title > h1 ::text').extract_first(),
               'id': response.css(
                   '#MainContent_ctlDetailBox_lblContactPhone > a::attr(data-phoneext)').extract_first(),
               'price': response.css('#MainContent_ctlDetailBox_lblPrice::text').extract_first(),
               'address': response.css('#MainContent_ctlDetailBox_lblAddressContact::text').extract_first(),
               'phone': res.text,
               'url': response.url
               }

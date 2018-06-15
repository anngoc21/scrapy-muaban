import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://www.muabannhadat.vn/nha-dat-3490']

    def parse(self, response):
        for title in response.css('a.title-filter-link'):
            yield {'title': title.css('a ::text').extract_first(), 'url': title.css('a::attr(href)').extract_first()}
            print(response.follow(
                "http://www.muabannhadat.vn{0}".format(title.css('a::attr(href)').extract_first()),
                self.parse_detail_page))

        for next_page in response.css('a#MainContent_ctlList_ctlResults_ctlPager_lnkNext'):
            yield response.follow(next_page, self.parse)

    def parse_detail_page(self, response):
        yield {'type': response.css('ol.breadcrumb > li > a > p.cusp ::text').extract_first()}

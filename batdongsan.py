import scrapy
import requests
import re


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://batdongsan.com.vn/nha-dat-ban']

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "vi,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "__cfduid=d748310e2d402deb2ac9f07781b9339ad1529901530; _ga=GA1.3.442035882.1529901531; _gid=GA1.3.818140085.1529901531; usidtb=64kfYxIe0qnJx0qFDGDZr0uw1jHNkLmk; __auc=106b0aec164353cd119e8113314; SERVERID=F; ASP.NET_SessionId=pwcsuuqeqqlcdt53nie20edo; __asc=ef8f3e801643a5045dc6bdcf5c5; sidtb=xyV0teViKP0GtVzPQefk9FnUqanIMSxR; USER_SEARCH_PRODUCT_CONTEXT=38%7C324%7CHN%7C7%7C9455%7C11392%7C2220%2C14616839",
        "Host": "batdongsan.com.vn",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }

    def start_requests(self):
        return [scrapy.Request("http://batdongsan.com.vn/nha-dat-ban",
                               headers=self.headers,
                               callback=self.parse)]

    def parse(self, response):
        for title in response.css('div.p-title > h3 > a'):
            yield scrapy.Request("https://batdongsan.com.vn{0}".format(title.css('a::attr(href)').extract_first()),
                                 headers=self.headers,
                                 callback=self.parse_detail_page)
        for x in range(2, 1000):
            yield scrapy.Request("https://batdongsan.com.vn/nha-dat-ban/p{0}".format(x),
                                 headers=self.headers,
                                 callback=self.parse)

    def parse_detail_page(self, response):
        m = re.search("([0-9]{2}\-[0-9]{2}\-[0-9]{4})", (response.css(
            '#product-detail > div.prd-more-info > div:nth-child(3)').extract_first() or "").encode(
            'utf-8').strip())
        yield {
            'title': (response.css(
                '#product-detail > div.pm-title > h1::text').extract_first() or "").encode('utf-8').strip(),
            'price': (response.css(
                '#product-detail > div.kqchitiet > span > span.gia-title.mar-right-15 > strong::text').extract_first() or "").encode(
                'utf-8').strip(),
            'address': (response.css(
                '#LeftMainContent__productDetail_contactAddress > div.right::text').extract_first() or "").encode(
                'utf-8').strip(),
            'phone': (response.css(
                '#LeftMainContent__productDetail_contactMobile > div.right::text') or "").extract_first().encode(
                'utf-8').strip(),
            'url': response.url,
            'date': m.group(1)
        }

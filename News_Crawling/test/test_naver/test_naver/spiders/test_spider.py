import scrapy


class QuotesSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page  #문자열 안에 또 다른 문자열을 삽입하기 위해 앞에서 사용한 문자열 포맷 코드  %s
        # 숫자는 %d 문자는 %s
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "news_test"
    # start_urls = [
    #     'http://news.einfomax.co.kr/news/articleList.html?page=1&total=87585&sc_sdate=2005-01-01&sc_edate=2017-05-31&sc_word=%EA%B8%88%EB%A6%AC&view_type=sm',
    # ]

    def start_requests(self):
        urls = []

        for i in range(1, 2920, 1):
            l = 'http://news.einfomax.co.kr/news/articleList.html?page={}&total=87585&sc_sdate=2005-01-01&sc_edate=2017-05-31&sc_word=%EA%B8%88%EB%A6%AC&view_type=sm'.format(i)
            urls.append(l)


        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)

    def parse(self, response):
        for con in response.xpath('//*[@id="user-container"]/div[3]/div[2]/section/article/div[2]/section/div'):
            yield {
                'link': con.xpath('div[1]/ a/@href').get(),
                'text': con.xpath('div[2]/text()').get()
            }
        

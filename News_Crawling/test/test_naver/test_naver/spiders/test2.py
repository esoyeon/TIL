import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "test2"
    start_urls = ['http://news.einfomax.co.kr/news/articleList.html?page=1&total=87585&sc_sdate=2005-01-01&sc_edate=2017-05-31&sc_word=%EA%B8%88%EB%A6%AC&view_type=sm']
        

    def parse(self, response):
        urls = [1]
        for con in response.xpath('//*[@id="user-container"]/div[3]/div[2]/section/article/div[2]/section/div'):
            yield {
                'link': con.xpath('div[1]/ a/@href').get(),
                'text': con.xpath('div[2]/text()').get()
            }
        
        if urls[0] == 1:
            page_num = 1
        else:
            page_num = int(re.findall('page=([0-9]+)', urls[0])[0])

        if page_num < 100:
            page_num += 1
            next_page = 'http://news.einfomax.co.kr/news/articleList.html?page={}&total=87585&sc_sdate=2005-01-01&sc_edate=2017-05-31&sc_word=%EA%B8%88%EB%A6%AC&view_type=sm'.format(page_num)
            urls[0] = next_page
            yield response.follow(next_page, callback=self.parse)
        

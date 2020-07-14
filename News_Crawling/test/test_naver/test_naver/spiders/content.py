import scrapy
import csv

class YnewsSpider(scrapy.Spider):
    name = "NewsContent"
    # start_urls = [
    #     'http://news.einfomax.co.kr/news/articleView.html?idxno=51513',
    #     'http://news.einfomax.co.kr/news/articleView.html?idxno=51515'
    # ]
    # def start_requests(self):
    #     with open('test\test_naver\test_link.csv') as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             yield scrapy.Request(row['link'], self.parse)


    def parse(self, response):
        yield {
                'content':response.xpath('//*[@id="article-view-content-div"]/text()').extract(),
            }
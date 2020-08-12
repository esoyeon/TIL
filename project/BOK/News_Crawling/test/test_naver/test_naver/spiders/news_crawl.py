import scrapy
from naver_crawler.items import NaverCrawlerItem
import datetime
# 이건 월별 기사수 나오는 함수긴 한데, 분명 허점이 존재할거 같이만 규호쓰가 한 방식으로는 중간중간 빈 날짜들이 좀 많이생겨서 월단위는 이렇게 한다고 그냥 복붙함
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)
begin = "2005.01.01"
end = "2017.12.31"
def monthlist(begin,end):
    begin = datetime.datetime.strptime(begin, "%Y.%m.%d")
    end = datetime.datetime.strptime(end, "%Y.%m.%d")
    result = []
    while True:
        if begin.month == 12:
            next_month = begin.replace(year=begin.year+1,month=1, day=1)
        else:
            next_month = begin.replace(month=begin.month+1, day=1)
        if next_month > end:
            break
        result.append ([begin.strftime("%Y.%m.%d"),last_day_of_month(begin).strftime("%Y.%m.%d")])
        begin = next_month
    result.append ([begin.strftime("%Y.%m.%d"),end.strftime("%Y.%m.%d")])
    return result
date_list = monthlist(begin,end)
# 새로운 데이트 리스트 생성, [['2005.01.01', '2005.12.31']] 형태로 돼있음
# [['2005.01.01', '2005.01.31'], ['2005.02.01', '2005.02.28'], 2런 느낌
new_date_list = []
for list_date in date_list:      # 여기서 URL 하나 change
    new_date_list.append("https://search.naver.com/search.naver?where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_opt&sort=2&photo=0&field=0&reporter_article=&pd=3&ds={}&de={}&docid=&mynews=1&refresh_start=0&related=0".format(list_date[0], list_date[1]))
    # 그래서 나온 date 순서쌍들을 처음 url에 넣어서, 리스트 url들을 만들고, 그 url리스트를  start request에 넣어버릴래! &nso=so%3Ar%2Cp%3Afrom20050101to20150131%2Ca%3Aall
import re
class NaverSpider(scrapy.Spider):
    name = "naver"
    def start_requests(self):
        urls = new_date_list # 여기에 넣는다 이말이야
        for url in urls:
            yield scrapy.Request(url=url, cookies = {'news_office_checked' : '1001,1018,2227'}, callback=self.ongoing_requests) 
    def ongoing_requests(self, response):
        num = response.xpath('//*[@id="main_pack"]/div[2]/div[1]/div[1]/span/text()').get()
        num = re.findall('[0-9]+,[0-9]+', num)
        num = int(re.sub(",","",num[0]))
        urls = []
        start_num = (num //10 )*10+ 1
        for start in range(1, start_num, 10): 
                               # 이 URL도 해당 페이지의 URL을 직접 받아서 거기서 for문을 돌리던가 해야함
            urls.append( response.url + '&start={}'.format(start))
        for url in urls:
            yield scrapy.Request(url=url,cookies = {'news_office_checked' : '1001,1018,2227'} ,callback=self.parse_page)
    # def parse_page(self, response): 
    #      urls = response.xpath("//dd[@class='txt_inline']/a/@href").extract() ## 이부분 확인해봐야함..
    #      for url in urls:
    #         yield scrapy.Request(url=url, callback=self.ongoing_requests)
    def parse_page(self, response):
        articles = response.xpath("//dd[@class='txt_inline']")
        urls = []
        for article in articles:
            urls.extend(article.xpath("./a/@href").extract())
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        item = NaverCrawlerItem()
        item['url'] = response.url
        item['content'] = response.xpath(
            "//div[@id='articleBodyContents']//text()").getall()
        item['media'] = response.xpath(
            "//div[@class='press_logo']/a/img/@alt").get()
        yield item
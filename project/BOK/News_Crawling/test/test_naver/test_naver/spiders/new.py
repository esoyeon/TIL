import scrapy
from naver_crawler.items import NaverCrawlerItem
import datetime
import re

# 이건 월별 기사수 나오는 함수긴 한데, 분명 허점이 존재할거 같이만 규호쓰가 한 방식으로는 중간중간 빈 날짜들이 좀 많이생겨서 월단위는 이렇게 한다고 그냥 복붙함
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)
begin = "2005.01.01"
end = "2005.12.31"
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
for list_date in date_list:
    new_date_list.append("https://search.naver.com/search.naver?where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds={}&de={}&docid=&nso=so%3Ar%2Cp%3Afrom20050101to20150131%2Ca%3Aall&mynews=1&refresh_start=0&related=0".format(list_date[0], list_date[1]))
    # 그래서 나온 date 순서쌍들을 처음 url에 넣어서, 리스트 url들을 만들고, 그 url리스트를  start request에 넣어버릴래!
class NaverSpider(scrapy.Spider):
    name = "new"
    def start_requests(self):
        urls = new_date_list # 여기에 넣는다 이말이야
        for url in urls:
            yield scrapy.Request(url=url, cookies = {'news_office_checked' : '1001,1018,2227'}, callback=self.ongoing_requests) # 이렇게 하면 3개 다 체크됨
    # 아마 이 부분에서 소연이가 한 pages 넣어서 챠라라랍 돌리면 될 듯.. 여기까진 무립니다.. 힘듭니다.... Xpath 따오는데 2시간 걸림 ^^;; ㅅㅂ ㅎㅎ !
    
    def ongoing_requests(self, response):
        num = response.xpath(
            '//*[@id="main_pack"]/div[2]/div[1]/div[1]/span/text()').get()
        num = re.findall('[0-9]+,[0-9]+', num)
        num = int(re.sub(",", "", num[0]))
        urls = []
        start_num = (num // 10)*10 + 10
        url = response.url

##url의 날짜를 포문으로 안던져주면 여기 append할때 url에 날짜가 빈칸이 되어버리니까... 위에서 url만드는 아이디어는 좋은데 아래로 페이지 바꾸면서 하나씩 던지려면 위에서 해준거를 활용할수가 없는거같은데..?ds,de{}{}되어있으면 제대로 안먹을테니...ㅠ 좋은방법있을까
        for start in range(1, start_num, 10):
            urls.append(
                url + '&start={}'.format(start)
                        )
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)
##그래서 생각한 아이디어는 1. 위에서 날짜/페이지까지 다 변경시켜줘서 url모음에 append해서 모든 케이스 만들고 아래는 던지기만 하게 한다
## 2. 아래에서 날짜돌게하고, start돌게 하는걸 for for(지금 한거)돌려서 아래로 던지게 한다...
## 으아 미안해 10시까지 하면 할만하겠지 했던 나의 착각인듯하다... 결국 의문점만 던지고 왜 잘 안되는지만 밝히고 대안을 찾지 못한듯ㅠ
    def parse_page(self, response):  # 이건 들어간 첫 페이지에서 url 따오는거고
         urls = response.xpath("//dd[@class='txt_inline']/a/@href").extract()
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
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class NaverCrawlerPipeline:
    def process_item(self, item, spider):
        f = open("news.csv", "wb")
        exporter = CsvItemExporter(f, encoding='utf-8')
        exporter.export_item(item)
        return item

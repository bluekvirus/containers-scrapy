# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlersPipeline(object):
    def process_item(self, item, spider):
        return item

class NowInStockPipeline(object):
    def process_item(self, item, spider):
        if spider.name is 'nv-gpu-nowinstock':
            spider.logger.info(item.gpu_type + ' Done!')
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

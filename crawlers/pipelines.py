# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json, datetime, requests, os

class CrawlersPipeline(object):
    def process_item(self, item, spider):
        return item

class NowInStockPipeline(object):

    def process_item(self, item, spider):
        if spider.name == 'nv-gpu-nowinstock':
            #spider.logger.info('\n' + json.dumps(list(item['new_entries_set'])) + '\n')
            if self.cache.get(item['gpu_type']) is not None:
                diff_entries = set(item['new_entries_set']) - set(self.cache.get(item['gpu_type']))
                for entry in diff_entries:
                    ## notify Slack ##
                    spider.logger.info('\n\n new entry found: ' + entry + '\n\n')

                    if('Preorder' in entry or 'In Stock' in entry):
                        requests.post(os.environ.get(
                            'SLACK_WEBHOOK', 'https://hooks.slack.com/services/x/y/z'),
                            json={"text": entry}
                            )
                    ##################
            self.cache[item['gpu_type']] = item['new_entries_set']
        return item

    def open_spider(self, spider):
        try:
            with open(spider.settings['SPIDER_CACHE_DIR'] + spider.name + '.json') as cache:
                self.cache = json.load(cache)
        except FileNotFoundError:
                self.cache = {}

    def close_spider(self, spider):
        with open(spider.settings['SPIDER_CACHE_DIR'] + spider.name + '.json', 'w') as cache:
            self.cache = self.cache or {}
            self.cache['updated'] = str(datetime.datetime.now())
            json.dump(self.cache, cache, indent=4)

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json, datetime, requests, os, re

class CrawlersPipeline(object):
    def process_item(self, item, spider):
        return item

class NowInStockPipeline(object):
    """nv-gpu NowInStock spider item pipline.

    This pipeline requires environment var SLACK_WEBHOOK to operate. 
    It extracts newly obtained history entries and compare with their 
    base price before posting onto a Slack channel of interest. 
    Old entries will be cached into a file and serve as a baseline for 
    the next crawl.

    Default environment var REPORT_RATIO_THRESHOLD is set to be 2.0, this means 
    item that has a price point over 200% of the base price will not be 
    sent to Slack channel.

    Note: 
        You can locate your channel webhook at https://api.slack.com/apps/<id>/incoming-webhooks? after creating the app.
    
    Author:
        Tim Lauv <bluekvirus@gmail.com>
    
    Created: 2018.02.14
    Updated: 2018.02.15
    """
    def process_item(self, item, spider):
        if spider.name == 'nv-gpu-nowinstock':
            #spider.logger.info('\n' + json.dumps(list(item['new_entries_set'])) + '\n')
            if self.cache.get(item['gpu_type']) is not None:
                diff_entries = set(item['new_entries_set']) - set(self.cache.get(item['gpu_type']))
                for entry in diff_entries:
                    ## notify Slack ##
                    spider.logger.info('\n\n new entry found: ' + entry + '\n\n')
                    if('Preorder' in entry or 'In Stock' in entry):
                        ## 1 compare to meta.price
                        dollar_match = re.search('\$[\.\d,]+', entry)
                        ratio = float(entry[dollar_match.start()+1:dollar_match.end()].replace(',', '')) / float(self.meta['price'][item['gpu_type']])
                        if ratio < 1.1:
                            emo = ':+1:'
                        elif ratio >= 1.2 and ratio < 1.4:
                            emo = ':dizzy_face:'
                        elif ratio >= 1.4:
                            emo = ':scream:'
                        else:
                            emo = ':confused:'
                        ## 2 send to webhook
                        if ratio < float(os.environ.get('REPORT_RATIO_THRESHOLD', 2.0)):
                            requests.post(os.environ.get(
                                'SLACK_WEBHOOK', 'https://hooks.slack.com/services/x/y/z'),
                                json={"text": entry + ' ' + emo + ' {:.1f}%'.format(ratio * 100)}
                                )
                        else:
                            spider.logger.info('Not reported, filtered by REPORT_RATIO_THRESHOLD\n')
                    ##################
            self.cache[item['gpu_type']] = item['new_entries_set']
        return item

    def open_spider(self, spider):

        with open(spider.settings['SPIDER_CACHE_DIR'] + 'nv-gpu-price-meta.json') as meta:
            self.meta = json.load(meta)

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

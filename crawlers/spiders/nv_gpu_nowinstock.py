# -*- coding: utf-8 -*-
import scrapy


class NvGpuNowinstockSpider(scrapy.Spider):
    name = 'nv-gpu-nowinstock'
    allowed_domains = ['www.nowinstock.net']
    start_urls = [
        'http://www.nowinstock.net/computers/videocards/nvidia/gtx1060/',
        'http://www.nowinstock.net/computers/videocards/nvidia/gtx1070/',
        'http://www.nowinstock.net/computers/videocards/nvidia/gtx1070ti/',
        'http://www.nowinstock.net/computers/videocards/nvidia/gtx1080/',
        'http://www.nowinstock.net/computers/videocards/nvidia/gtx1080ti/',
        ]

    def parse(self, response):
        gpu_type = response.css('div#trackerHeading h3::text').extract_first()
        history_list = response.css('div#history td::text').extract()
        new_entry_tuples = list(zip(history_list[::2], history_list[1::2]))
        new_entries_set = list(map(lambda item: item[0] + ' >>> ' + item[1], new_entry_tuples))
        item = {
            'gpu_type': gpu_type,
            'new_entry_tuples': new_entry_tuples,
            'new_entries_set': new_entries_set,
        }
        yield item

# -*- coding: utf-8 -*-
import scrapy, re


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
        new_entries = list(map(lambda item: list(item), zip(history_list[::2], history_list[1::2])))
        new_entries_set = list(map(lambda item: item[0] + ' >>> ' + item[1], new_entries))
        for entry in new_entries:
            brand_model = re.split('(In Stock|Out of Stock|Preorder)', entry[1])[0].split(' : ')
            model_brand = brand_model[1] + ': ' + brand_model[0]
            buy_link = response.css('div#trackerContent td').xpath(
                "a[contains(., '" + model_brand + "')]/@href").extract_first()
            entry.append(buy_link)
        item = {
            'gpu_type': gpu_type,
            'new_entries': new_entries, # time, brand : model, product link
            'new_entries_set': new_entries_set,
        }
        yield item

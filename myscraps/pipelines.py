# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

from myscraps.items import RestaurantInfor, ReviewItem


# class MyscrapsPipeline(object):
#     def process_item(self, item, spider):
#         if isinstance(item, RestaurantInfor):
#             return self.handleRestaurant(item, spider)
#         if isinstance(item, ReviewItem):
#             return self.handleReview(item, spider)
#
#     def handleRestaurant(item, spider):
#         return item
#
#     def handleReview(item, spider):
#         return item

# class RestaurantInforPipeline(object):
#     def process_item(self, item, spider):
#         # if isinstance(item, RestaurantInfor):
#             return item
#
# class ReviewItemPipeline(object):
#     def process_item(self, item, spider):
#         # if isinstance(item, ReviewItem):
#             return item


class MultiCSVItemPipeline(object):
    SaveTypes = ['RestaurantInfor', 'ReviewItem']

    def open_spider(self, spider):
        self.files = dict([ (name, open(name+'.csv', 'w+b')) for name in self.SaveTypes ])
        self.exporters = dict([ (name,CsvItemExporter(self.files[name])) for name in self.SaveTypes])
        [e.start_exporting() for e in self.exporters.values()]

    def close_spider(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = type(item).__name__
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item
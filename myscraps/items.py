# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy

class RestaurantInfor(scrapy.Item):
    restautant_id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    phoneNum = scrapy.Field()
    decription = scrapy.Field()
    detail = scrapy.Field()
    url = scrapy.Field()

class ReviewItem(scrapy.Item):
    # Items to get
    restautant_id = scrapy.Field()
    header = scrapy.Field()
    review = scrapy.Field()
    rating = scrapy.Field()
    review_Count = scrapy.Field()
    help_count = scrapy.Field()


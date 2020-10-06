#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from myscraps.items import ReviewItem
from myscraps.items import RestaurantInfor
from selenium import webdriver
import html2text
import re
from scrapy import Request


class TripAdvisorReview(scrapy.Spider):
    name = "tripadvisor"
    # Cities: Recife, Porto Alegre, Salvador, Brasilia, Fortaleza, Curitiba, Belo Horizonte, Vitoria, Florianopolis, Natal, Goiania.
    start_urls = ["https://www.tripadvisor.com/Restaurants-g293925-Ho_Chi_Minh_City.html"]

    def __init__(self):
        self.driver = webdriver.Edge('msedgedriver')
        # self.driver = webdriver.Edge()
        self.index = 1

    def parse(self, response):
        urls = []
        for href in response.xpath('//div[@class="wQjYiB7z"]//a/@href').extract():
            url = response.urljoin(href)
            if url not in urls:
                urls.append(url)
                yield scrapy.Request(url, callback=self.parse_page)

        # next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract()
        # if next_page:
        #     url = response.urljoin(next_page[-1])
        #     print url
        #     yield scrapy.Request(url, self.parse)
        # self.index += 1

    def parse_page(self, response):

        Restaurant = RestaurantInfor()

        CurrentURL = response.request.url
        try:
            RestID = re.search('-d(.+?)-', CurrentURL).group(1)
        except:
            RestID = 0
        Restaurant['restautant_id'] = RestID
        Restaurant['name'] = response.xpath('//h1[@data-test-target="top-info-header"]/text()').extract_first()
        Restaurant['address'] = response.xpath('//a[@class="_15QfMZ2L"]/text()').extract_first()
        Restaurant['phoneNum'] = response.xpath('//a[@class="_3S6pHEQs"]/text()').extract_first()
        Restaurant['url'] = CurrentURL

        print "=========================" + self.index.__str__() + "========================"
        self.driver.get(response.url)
        while True:
            try:
                ViewDetail = self.driver.find_element_by_xpath('//a[@class="_3xJIW2mF _39x9M0gt"]')
                ViewDetail.click()
                self.driver.implicitly_wait(2)
                # description = response.xpath('//div[@class="_2D5jETbG"]/text()').extract_first()
                try:
                    description = self.driver.find_element_by_class_name('_2D5jETbG').text
                    Restaurant['decription'] = description.replace('\n', '')
                    details = self.driver.find_element_by_xpath(
                        '//div[@class="ui_column  "]/following-sibling::div').get_attribute('innerHTML')
                    detail = html2text.html2text(details)
                except:
                    Restaurant['decription'] = "None"
                    details = self.driver.find_element_by_xpath(
                        '//div[@class="ui_column  "]').get_attribute('innerHTML')
                    detail = html2text.html2text(details)

                Restaurant['detail'] = detail
            except Exception as e:
                print "---------------------------Exception-------------------------------------------------"
                print e
                try:
                    try:
                        description = self.driver.find_element_by_class_name('_1lSTB9ov').text
                    except:
                        description = self.driver.find_element_by_class_name('_2D5jETbG').text
                    Restaurant['decription'] = description.replace('\n', '')
                    details = self.driver.find_element_by_xpath(
                        '//div[@class="ui_column  "]/following-sibling::div').get_attribute('innerHTML')
                    detail = html2text.html2text(details)
                except:
                    Restaurant['decription'] = "None"
                    details = self.driver.find_element_by_xpath(
                        '//div[@class="ui_columns "]').get_attribute('innerHTML')
                    detail = html2text.html2text(details)
                Restaurant['detail'] = detail
                break

        yield Restaurant

        # href = "https://www.tripadvisor.com/Restaurant_Review-g293925-d14973924-Reviews-Bollywood_Indian_Restaurant_Bar-Ho_Chi_Minh_City.html"
        #
        # url = response.urljoin(href)
        # # print "====================URL: " + url
        # yield scrapy.Request(url, callback=self.parse_review)
        # print "=============================debug========================"

        # self.index += 1
        # self.driver.close()

    def parse_review(self, response):
        print "=============================debug inside1========================"
        CurrentURL = response.request.url
        try:
            RestID = re.search('-d(.+?)-', CurrentURL).group(1)
        except:
            RestID = 0
        review_page = Selector(response).xpath(
            '//div[@class="listContainer hide-more-mobile"]/div/div[@class="review-container"]')
        print "=============================debug inside========================"
        if review_page:
            i = 0
            j = 0
            for review in review_page:
                item = ReviewItem()

                # while True:
                #     show_more = self.driver.find_element_by_xpath('//p[@class="partial_entry"]/span[@class="taLnk ulBlueLinks"]')
                #
                #     try:
                #         show_more.click()
                #         # get the data and write it to scrapy items
                #     except:
                #         break
                #
                # self.driver.close()

                contents = \
                    review.xpath('//div[@class="quote"]/following-sibling::div/div[@class="entry"]/p/text()').extract()[
                        i].replace('\n', '')

                # if "..." in contents:
                #     more = review.xpath('//div[@class="entry"]/p/span[@class="postSnippet"]/text()').extract()[j].replace('\n', '')
                #     contents = contents[:-3] + " " + more
                #     j = j + 1

                header = review.xpath('//div[@class="quote"]/a/span[@class="noQuotes"]/text()').extract()[i]
                ratings = review.css('span.ui_bubble_rating').extract()
                rating_index = ratings[0].find(' bubble_') + 8
                rating = int(ratings[0][rating_index:rating_index + 2]) / 10
                Review_count = review.xpath(
                    '//div[@class="reviewerBadge badge"]/span[@class="badgeText"]/text()').extract()[i]
                help_counts = review.css('span.helpful_text .numHelp::text').extract()
                if help_counts:
                    help_count = int(help_counts[0][:-1].strip())
                else:
                    help_count = 0

                item['restautant_id'] = RestID
                item['rating'] = rating
                item['header'] = header
                item['review'] = contents
                item['review_Count'] = Review_count
                item['help_count'] = help_count

                i = i + 1
                yield item

        next_page = response.xpath('//div[@class="unified ui_pagination "]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[-1])
            yield scrapy.Request(url, self.parse_review)

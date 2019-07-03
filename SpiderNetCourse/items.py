# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpideretcourseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QqCourseItem(scrapy.Item):
    title = scrapy.Field()
    icon = scrapy.Field()
    learner = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    course_id = scrapy.Field()
    introduction = scrapy.Field()

class UdacityCourseItem(scrapy.Item):
    title = scrapy.Field()
    icon = scrapy.Field()
    learner = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    course_id = scrapy.Field()
    introduction = scrapy.Field()
    graded = scrapy.Field()

class Study163CourseItem(scrapy.Item):
    title = scrapy.Field()
    icon = scrapy.Field()
    learner = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    course_id = scrapy.Field()
    introduction = scrapy.Field()
    graded = scrapy.Field()
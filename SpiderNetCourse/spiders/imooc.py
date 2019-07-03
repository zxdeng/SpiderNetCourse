# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re

from SpiderNetCourse.items import CourseItem

class ImoocSpider(scrapy.Spider):
    name = 'imooc'
    start_urls = ['https://coding.imooc.com/']

    def parse(self, response):

        list = response.xpath("//div[contains(@class,'shizhan-course-wrap')]").extract()
        for course_item in list:
            course = Selector(text=course_item)
            item = CourseItem()
            item['title'] = course.xpath("//p[contains(@class,'shizan-name')]/@title").extract_first()
            item['icon'] = course.xpath("//div[contains(@class,'img-box')]/img[contains(@class,'shizhan-course-img')]/@src").extract_first()
            item['learner'] = course.xpath("//div[contains(@class,'shizhan-info')]/span[2]/text()").extract_first()
            item['graded'] = course.xpath("//div[contains(@class,'shizhan-info')]/span[1]/text()").extract_first()
            item['author'] = course.xpath("//div[contains(@class,'lecturer-info')]/span/text()").extract_first()
            if course.xpath("//div[contains(@class,'course-card-price')]/text()"):
                item['price'] = course.xpath("//div[contains(@class,'course-card-price')]/text()").extract_first()
            else:
                item['price'] = course.xpath("//span[contains(@class,'discount-price')]/text()").extract_first()
            item['link'] = "https://coding.imooc.com" + course.xpath("//a/@href").extract_first()
            item['course_id'] = re.findall(r"\d+", course.xpath("//a/@href").extract_first())
            item['introduction'] = course.xpath("//p[contains(@class,'shizan-desc')]/text()").extract_first()
            yield item
        next_url = response.xpath("//div[@class='page']/a[contains(text(),'下一页')]/@href").extract_first()
        if next_url:
            yield scrapy.Request("https://coding.imooc.com"+next_url, self.parse)

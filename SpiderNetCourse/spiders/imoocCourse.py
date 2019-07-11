# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re

from SpiderNetCourse.items import CourseItem

class ImoocSpider(scrapy.Spider):
    name = 'imoocCourse'
    start_urls = ['https://www.imooc.com/course/list']

    def parse(self, response):

        list = response.xpath("//div[contains(@class,'course-card-container')]").extract()
        for course_item in list:
            course = Selector(text=course_item)
            item = CourseItem()
            item['title'] = course.xpath("//h3[contains(@class,'course-card-name')]/text()").extract_first()
            item['icon'] = course.xpath("//img[contains(@class,'course-banner')]/@src").extract_first()
            item['learner'] = course.xpath("//div[contains(@class,'course-card-info')]/span[2]/text()").extract_first()
            item['graded'] = course.xpath("//div[contains(@class,'course-card-info')]/span[1]/text()").extract_first()
            # item['author'] = course.xpath("//div[contains(@class,'lecturer-info')]/span/text()").extract_first()
            item['author'] = ''
            if course.xpath("//span[contains(@class,'price')]/text()"):
                item['price'] = course.xpath("//span[contains(@class,'price')]/text()").extract_first()
            else:
                item['price'] = course.xpath("//span[contains(@class,'discount-price')]/text()").extract_first()
            item['link'] = "https://www.imooc.com" + course.xpath("//a/@href").extract_first()
            item['course_id'] = re.findall(r"\d+", course.xpath("//a/@href").extract_first())[0]
            item['introduction'] = course.xpath("//p[contains(@class,'course-card-desc')]/text()").extract_first()
            yield item
        # next_url = response.xpath("//div[@class='page']/a[contains(text(),'下一页')]/@href").extract_first()
        # if next_url:
        #     yield scrapy.Request("https://www.imooc.com"+next_url, self.parse)

# -*- coding: utf-8 -*-
import scrapy

from SpiderNetCourse.items import UdacityCourseItem

class UdacitySpider(scrapy.Spider):
    name = 'udacity'
    # allowed_domains = ['https://cn.udacity.com/courses/all']
    start_urls = ['https://cn.udacity.com/courses/all/']

    def parse(self, response):
        course_list = response.xpath("//div[@class='course-summary-card row row-gap-medium ng-star-inserted']")
        for course in course_list:
            item = UdacityCourseItem()
            item['title'] = course.xpath(".//h3[@class='h-slim']/a/text()").extract()[0]
            item['icon'] = course.xpath(".//img/@src").extract()[0]
            # item['author'] = course.xpath(
            #     ".//a[@class='item-source-link']/text()").extract()[0]
            url = "https://cn.udacity.com/course" + course.xpath(".//h3[@class='h-slim']/a/@href").extract()[0]
            item['link'] = url
            print(url)
            # item['price'] = course.xpath(
            #     ".//div[@class='item-line item-line--bottom']/span/text()").extract()[0]
            # item['course_id'] = course.xpath("./a/@data-id").extract()[0]
            item['introduction'] = course.xpath(".//span[@class='ng-star-inserted']/text()").extract()[0]
            item['graded'] = course.xpath(".//span[@class='capitalize']/text()").extract()[0]
            yield item

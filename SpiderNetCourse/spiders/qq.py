# -*- coding: utf-8 -*-
import scrapy
import re
from SpiderNetCourse.items import QqCourseItem


class QqSpider(scrapy.Spider):
    name = 'qq'
    # allowed_domains = ['https://ke.qq.com']
    start_urls = ['https://ke.qq.com/course/list']
    index_num = 1
    def parse(self, response):
        course_list = response.xpath(
            "//div[@data-report-module='middle-course']//li")
        print(len(course_list))
        for course in course_list:
            print("当前数据总数为：" + str(self.index_num))
            self.index_num += 1
            item = QqCourseItem()
            item['title'] = course.xpath("./h4/a/text()").extract()[0]
            item['icon'] = course.xpath(
                ".//img[@class='item-img']/@src").extract()[0]
            item['learner'] = re.sub("\D", "", course.xpath(
                ".//span[@class='line-cell item-user']/text()").extract()[0] .strip())
            item['author'] = course.xpath(
                ".//a[@class='item-source-link']/text()").extract()[0]
            url = "https:" + course.xpath("./a/@href").extract()[0]
            item['link'] = url
            print(url)
            item['price'] = course.xpath(
                ".//div[@class='item-line item-line--bottom']/span/text()").extract()[0]
            item['course_id'] = course.xpath("./a/@data-id").extract()[0]
            # yield item
            yield scrapy.Request(url, callback=self.parse_course_detail, meta={'item': item})

        next_urls = response.xpath("//div[@class='sort-page']/a/@href").extract()
        next_url = next_urls[len(next_urls)-1]
        print("下一页地址："+next_url)
        if next_url != "javascript:void(0);":
            print("开始抓取下一页")
            yield scrapy.Request(next_url, self.parse)

    def parse_course_detail(self, response):
        item = response.meta['item']
        item['introduction'] = response.xpath(
            "//table[@class='tb-course']/tbody/tr/td/text()").extract()[0]
        yield item

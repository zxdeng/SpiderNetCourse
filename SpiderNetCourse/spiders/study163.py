# -*- coding: utf-8 -*-
import scrapy
from SpiderNetCourse.items import Study163CourseItem
from scrapy_splash import SplashRequest
import re
import time


class Study163Spider(scrapy.Spider):
    name = 'study163'
    start_urls = [
        'https://study.163.com/category/480000003131009#/',
        'https://study.163.com/category/480000003121024#/',
        'https://study.163.com/category/480000003127010#/',
        'https://study.163.com/category/480000003130008#/',
        'https://study.163.com/category/480000003132060#/',
        'https://study.163.com/category/480000003129033#/',
        'https://study.163.com/category/480000003126038#/',
        'https://study.163.com/category/400000001331002#/',
        'https://study.163.com/category/480000003125071#/'
    ]
    # 'https://study.163.com/category/480000003131009#/',
    index_num = 1

    def start_requests(self):
        for url in self.start_urls:
            print("开始调用链接为：" + url)
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        courses = response.xpath("//ul[@class='uc-course-list_ul']/li")
        # print(f'text = {response.text}')

        print(len(courses))
        for course in courses:
            print("current_count：" + str(self.index_num) + response.url)
            self.index_num += 1
            item = Study163CourseItem()
            item['title'] = course.xpath(
                ".//span[@class='uc-ykt-coursecard-wrap_tit_name']/text()").extract()[0]
            item['icon'] = 'https:' + \
                course.xpath(".//img[@class='imgPic j-img']/@data-src").extract()[0]
            # item['author'] = course.xpath(
            #     ".//a[@class='item-source-link']/text()").extract()[0]
            item['link'] = 'https:' + course.xpath(".//a/@href").extract()[0]
            try:
                item['price'] = course.xpath(
                    ".//span[@class='u-free' or @class='u-discount' or @class='u-normal' or @class='u-free f-fs0']/text()"
                ).extract()[0]
            except IndexError:
                item['price'] = '未知'

            item['course_id'] = re.compile(r'\d+').findall(item['link'])[1]

            yield item
            # yield SplashRequest(item['link'], self.pass_detail, args={'wait':
            # 0.5}, dont_filter=True, meta={'item': item})

        pages = response.xpath(
            "//div[@class='uc-course-list_content']//ul[@class='ux-pager']//a/text()").extract()
        if len(pages) < 4:
            with open("study163.txt", 'a', encoding="utf-8") as f:
                f.write(response.url + '数据长度为：' +
                        str(len(courses)) + '最大页码为：1' + '\n')
            return
        max_page = pages[len(pages) - 2]
        with open("study163.txt", 'a', encoding="utf-8") as f:
            f.write(response.url + '数据长度为：' + str(len(courses)) +
                    '最大页数为：' + str(max_page) + '\n')
        if len(re.compile(r'\d+').findall(response.url)) > 2:
            current_page = int(re.compile(r'\d+').findall(response.url)[2])
        else:
            current_page = 1
        if current_page < int(max_page):
            current_page += 1
            next_url = 'https://study.163.com/category/' + \
                re.compile(r'\d+').findall(response.url)[1] + '#/?p=' + str(current_page)
            yield SplashRequest(next_url, self.parse, args={'wait': 0.5}, dont_filter=True)

    # def pass_detail(self, response):
    #
    #     item = response.meta['item']
    #     item['introduction'] = response.xpath(
    #         "//div[contains(@class,'cintrocon j-courseintro')]/text()").extract()[0]
    #     item['author'] = response.xpath(
    #         "//a[@class='j-userNode']/text()").extract()[0]
    #     yield item

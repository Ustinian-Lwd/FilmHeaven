# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from FilmHeaven.items import FilmheavenItem
from selenium import webdriver


class Dytt8Spider(scrapy.Spider):
    name = 'dytt8'
    allowed_domains = ['dytt8.net']
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/']

    # 重写请求
    def start_requests(self):

        # 声明无头操作
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")
        brower = webdriver.Chrome(options=opt)
        brower.get(url="http://www.ygdy8.net/index.html")

        # 解析
        html_text = brower.page_source
        html_etree = etree.HTML(html_text)
        nav_list = html_etree.xpath('//div[@class="contain"]//li/a/@href')
        # 对导航栏连接发起请求
        for nav in nav_list:
            if nav == "/html/gndy/index.html":
                pass
            elif nav == "/html/gndy/jddy/20160320/50510.html":
                pass
            elif nav == "#":
                pass
            elif nav == "/app.htm":
                pass
            else:
                nav_url = "http://www.ygdy8.net" + nav
                yield scrapy.Request(url=nav_url, callback=self.parse_list)


    # 每个页面下的电影列表
    def parse_list(self, response):
        movie_list = response.xpath("//div[@class='co_content8']//table")
        for movie in movie_list:
            item = FilmheavenItem()
            item["name"] = movie.xpath(".//a[@class='ulink']/text()").extract_first()
            item["date"] = movie.xpath(".//font[@color='#8F8C89']/text()").extract_first().split("\r")[0]

            # 获取二级页面的url
            next_url = "http://www.dytt8.net" + movie.xpath(".//a[@class='ulink']/@href").extract_first()

            yield scrapy.Request(url=next_url, callback=self.parse_detail, meta={"item": item})

    # 电影详情
    # 主要是爬取电影下载的url
    def parse_detail(self, response):
        # 将item转接过来
        item = response.meta["item"]
        print(item)
        item["haibao"] = response.xpath("//div[@id='Zoom']//img[1]/@src").extract_first()
        item["info"] = r"\n".join(response.xpath("//div[@id='Zoom']//p[1]/text()").extract())
        item["zhongzi"] = response.xpath("//div[@id='Zoom']//td[@bgcolor='#fdfddf']//a/@href").extract_first()

        yield item


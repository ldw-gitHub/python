#coding=utf-8
import scrapy
from tutorial.items import TutorialItem
from sqlalchemy.sql.expression import except_

class DmozSpider(scrapy.Spider):
    #名称
    name = "dmoz"
    #允许域名
    allowed_domains = ["sz.fang.lianjia.com"]
    #入口url
    start_urls = ["https://sz.fang.lianjia.com/loupan/pg1"]

    #默认数据解析
    def parse(self,response):
        try:
            page_number = response.meta['page_number']
        except:
            page_number = 2
        try:
            house_list = response.xpath("//div[@class='resblock-list-container clearfix']//ul[2]/li");
            for i_items in house_list:
                #item文件导入
                item = TutorialItem()
                #数据处理
                item['title'] = i_items.xpath(".//div//div[1]//a/text()").extract_first()
                item['address'] = i_items.xpath(".//div//div[2]//span[1]/text()").extract_first() + i_items.xpath(".//div//div[2]//span[2]/text()").extract_first() + i_items.xpath(".//div//div[2]//a/text()").extract_first()
                try:
                    item['total'] = i_items.xpath(".//div//div[@class='resblock-price']//div[@class='second']/text()").extract_first()
                except:
                    item['total'] = 'none'
                item['unitprice'] = i_items.xpath(".//div//div[@class='resblock-price']//div[@class='main-price']//span[1]//text()").extract_first()
                try:
                    item['buildingface'] = i_items.xpath(".//div//div[@class='resblock-area']//span//text()").extract_first()
                except:
                    item['buildingface'] = 'none'
                #数据导入到pipeline
                yield item
            #解析下一页的规则
            #next_link = response.xpath("//div[@class='page-box']//a[@class='next']/@href")
            print(page_number)
            if page_number < 5:
                url = "https://sz.fang.lianjia.com/loupan/pg" + str(page_number)
                print(url)
                page_number = page_number + 1
                yield scrapy.Request(url=url,meta={"page_number": page_number},callback=self.parse)
            
        except Exception as e:
            self.logger.error("error=" + str(response.url) + ", " + str(e))   
            

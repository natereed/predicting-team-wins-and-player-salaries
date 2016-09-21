# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SalaryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    team = scrapy.Field()
    pos = scrapy.Field()
    salary = scrapy.Field()
    contract_years = scrapy.Field()
    total_value = scrapy.Field()
    avg_annual = scrapy.Field()


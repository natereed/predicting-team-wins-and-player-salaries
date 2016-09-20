# -*- coding: utf-8 -*-
import scrapy


class StatsSpider(scrapy.Spider):
    name = "stats"
    allowed_domains = ["mlb.com"]
    start_urls = (
        "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+pitching&game_type='R'&season=2016&season_type=ANY&league_code='MLB'&sectionType=sp&statType=pitching&page=1&ts=1474311607640&playerType=QUALIFIER&sportCode='mlb'&split=&team_id=&active_sw=&position='1'&page_type=SortablePlayer&sortOrder='desc'&sortColumn=avg&results=&perPage=50&timeframe=&last_x_days=&extended=0"
    )

    def parse(self, response):
        pass

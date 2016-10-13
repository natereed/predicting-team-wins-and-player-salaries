# -*- coding: utf-8 -*-
import scrapy
import os

class MlbSpider(scrapy.Spider):
    name = "mlbspider"
    allowed_domains = ["mlb.com"]

    def __init__(self, player_dir):
        self.player_dir = player_dir

    def start_requests(self):
        player_dirs = os.listdir(self.player_dir)
        for player_dir in player_dirs:
            url = 'http://mlb.mlb.com/team/player.jsp?player_id={}'.format(player_dir)
            print(url)
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'player_id' : player_dir})

    def parse(self, response):
        vitals = response.css('.player-vitals ul li::text').extract()
        position = vitals[0]
        batting_and_throwing = vitals[1]
        height_and_weight = vitals[2]

        yield {'player_id' : response.meta['player_id'],
               'name' : response.css('.player-name::text').extract()[0],
               'full-name' : response.css('.full-name::text').extract()[0],
               'number': response.css('.player-number::text').extract()[0],
               'position' : vitals[0],
               'batting_and_throwing' : vitals[1],
               'height_and_weight' : vitals[2],
               }

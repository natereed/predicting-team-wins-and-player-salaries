# -*- coding: utf-8 -*-
import scrapy
import os
import re

class MlbSpider(scrapy.Spider):
    name = "mlbspider"
    allowed_domains = ["mlb.com"]

    def __init__(self, player_ids_file):
        self.player_ids_file = player_ids_file

    def start_requests(self):
        player_ids = []
        with open(self.player_ids_file, "r") as player_ids_file:
            for line in player_ids_file.readlines():
                player_ids.append(line.strip())

        for player_id in player_ids:
            url = 'http://mlb.mlb.com/team/player.jsp?player_id={}'.format(player_id)
            #print(url)
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'player_id' : player_id})

    def parse(self, response):
        vitals = response.css('.player-vitals ul li::text').extract()
        position = vitals[0]
        batting_and_throwing = vitals[1]
        height_and_weight = vitals[2]
        player_numbers = response.css('.player-number::text').extract()
        if len(player_numbers) > 0:
            player_number = player_numbers[0]
        else:
            player_number = ''

        player_birthdate_and_place = response.css('.player-bio ul li::text')[1].extract()
        # Grep for a date-like string
        m = re.search(r'([0-9]{2}/[0-9]{2}/[0-9]{4})', player_birthdate_and_place)
        if m:
            birthdate = m.group(1)

        yield {'player_id' : response.meta['player_id'],
               'name' : response.css('.player-name::text').extract()[0],
               'full-name' : response.css('.full-name::text').extract()[0],
               'number': player_number,
               'position' : vitals[0],
               'batting_and_throwing' : vitals[1],
               'height_and_weight' : vitals[2],
               'birthday' : birthdate
               }

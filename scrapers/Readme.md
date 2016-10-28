# Scraping

This documents the web scraping tools that were developed. These, along with the processing scripts that 
convert scraped data into Performance.csv, are deprecated by the Lahman database, which has all the data we 
need for analysis and modeling.

## Season statistics

Season stats, including player rankings, are obtained from MLB.com. This data also includes a URL link to the player page, 
where complete statistics for every season played by this player are available.

Scripts:
* scrapers/scrape_season_stats.py: Takes seasons, stats types and optional page num
* scrapers/js/season_stats.js

## Player Statistics

Once season stats are obtained, url's are extracted from the data and used to drive a player scraping process.

Scripts:
* processing/extract_scraping_targets.json
* scrapers/scrape_player_stats.py
* scrapers/js/player_stats.js

## Player bio's

Scripts were written to scrape player names using their MLB id's and build an internal database (Players.csv) that links the MLB.com id
to a unique id generated from the full player name.

The "scrapenames" directory contains Scrapy code, including mlbspider.py. The full documentation for scrapy is available on 
the project website, https://scrapy.org/.

## Salaries

Salaries were scraped from USA Today using a Scrapy spider. This code is in the "scrapesalaries" directory.






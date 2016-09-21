import scrapy
from scrapesalaries.items import SalaryItem

class SalariesSpider(scrapy.Spider):
    name = "salaries"
    column_names = ['name', 'team', 'pos', 'salary', 'contract_years', 'total_value', 'avg_annual']

    def start_requests(self):
        for year in range(1988, 2016):
            yield scrapy.Request('http://www.usatoday.com/sports/mlb/salaries/%d/player/all/' % year,
                                 callback=self.parse,
                                 meta={'year' : year})

    def extract_column(self, row, index):
        return row.xpath("(td)[%d]//text()" % index).extract_first().strip()

    def extract_columns(self, row, start_index, column_names):
        item = SalaryItem()
        for i, column_name in enumerate(column_names):
            item[column_name] = self.extract_column(row, i + start_index)
        return item

    def parse_row(self, row):
        return self.extract_columns(row, 2, self.column_names)

    def parse(self, response):
        for row in response.xpath("//tr[@class='page']"):
            item = self.parse_row(row)
            item['year'] = response.meta['year']
            yield item


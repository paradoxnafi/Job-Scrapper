import scrapy


class UnjobsSpiderSpider(scrapy.Spider):
    name = "unjobs_spider"
    allowed_domains = ["unjobs.org"]
    start_urls = ["https://unjobs.org/duty_stations/dil"]

    def parse(self, response):
        pass

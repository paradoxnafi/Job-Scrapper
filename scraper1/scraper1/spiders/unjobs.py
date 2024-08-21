import scrapy


class UnjobsSpider(scrapy.Spider):
    name = "unjobs"
    allowed_domains = ["unjobs.org"]
    start_urls = ["https://unjobs.org/duty_stations/dil"]

    def parse(self, response):
        # jobs = response.css('div.jov')
        page = response.css('body')
        yield page
        # for job in jobs:
        #     yield {
        #         'title': job.css('a::text').get(),
        #     }

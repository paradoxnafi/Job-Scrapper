import scrapy
import time


class VagaservisuSpider(scrapy.Spider):
    name = "vagaservisu"
    allowed_domains = ["vagaservisu.com"]
    start_urls = ["https://www.vagaservisu.com/search"]

    def parse(self, response):
        # Extract job data from the page
        jobs = response.css('div.blog-post')
        for job in jobs:
            yield {
                'tag': job.css('.post-tag::text').get(),
                'title': job.css('.post-title a::text').get(),
                'post-date': job.css('.post-date::text').get(),
                'post-url': job.css('.post-title a::attr(href)').get(),
            }

        time.sleep(0.25)
        # Find the 'Load More' button and extract the URL from the 'data-load' attribute
        load_more_url = response.css('a#load-more-link::attr(data-load)').get()

        # If there's a 'Load More' button, follow the URL
        if load_more_url:
            yield scrapy.Request(url=load_more_url, callback=self.parse)

        # Check if there are no more pages to load (this condition happens when the 'Load More' button is gone)
        no_more_pages = response.css('span.no-more.load-more.show')
        if no_more_pages:
            self.log("No more pages to load.")
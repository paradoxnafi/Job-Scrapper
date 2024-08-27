import scrapy
import time
from datetime import datetime


def process_string(s):
    parts = s.split(' - ')
    if len(parts) == 4:
        return parts[-1]
    elif len(parts) == 3:
        return parts[-1]
    elif len(parts) == 2:
        return parts[-1]
    return ''


def format_datetime_iso8601(datetime_str):
    # Parse the datetime string
    dt = datetime.fromisoformat(datetime_str)
    # Return the date in yyyy-mm-dd format
    return dt.strftime('%Y-%m-%d')


class VagaservisuSpider(scrapy.Spider):
    name = "vagaservisu_spider"
    allowed_domains = ["vagaservisu.com"]
    start_urls = ["https://www.vagaservisu.com/search"]

    def parse(self, response):
        # Extract job data from the page
        jobs = response.css('div.blog-post')
        for job in jobs:
            title = job.css('.post-title a::text').get()
            company_name = process_string(title)

            tag = job.css('.post-tag::text').get()
            tag = tag.replace('\n', '') if tag else ''

            post_date = job.css('.post-date::attr(datetime)').get()
            post_date = format_datetime_iso8601(post_date)

            yield {
                'tag': tag,
                'title': title,
                'post_date': post_date,
                'post_url': job.css('.post-title a::attr(href)').get(),
                'company_name': company_name,
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
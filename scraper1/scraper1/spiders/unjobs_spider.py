import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time
from datetime import datetime


def format_datetime_utc(datetime_str):
    # Parse the datetime string with timezone information
    dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    # Return the date in yyyy-mm-dd format
    return dt.strftime('%Y-%m-%d')


def format_datetime_verbose(datetime_str):
    # Clean up the string and ensure it matches the expected format
    datetime_str = datetime_str.strip()  # Remove any leading or trailing spaces

    try:
        # Parse the cleaned string
        dt = datetime.strptime(datetime_str, '%A, %d %B %Y')
        # Return the date in yyyy-mm-dd format
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        # Handle cases where the date format doesn't match
        print(f"Date format error: {datetime_str}")
        return ''


class UnjobsSpider(scrapy.Spider):
    name = "unjobs"
    allowed_domains = ["unjobs.org"]
    start_urls = ["https://unjobs.org/duty_stations/dil"]

    def __init__(self, *args, **kwargs):
        super(UnjobsSpider, self).__init__(*args, **kwargs)

        # Set up Selenium WebDriver with Chrome
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)

        time.sleep(5)

        sel = Selector(text=self.driver.page_source)
        job_posts = sel.css('.job[id]')

        for job in job_posts:
            title = job.css('.jtitle::text').get()
            post_date = job.css('time::attr(datetime)').get()
            post_date = format_datetime_utc(post_date) if post_date else post_date
            post_url = job.css('.jtitle::attr(href)').get()
            company_name = job.css('div.job::text').get()
            closing_date = job.css('div.job span::text').get()
            closing_date = closing_date.split(':')[-1].strip() if closing_date else ''
            closing_date = format_datetime_verbose(closing_date) if closing_date else ''

            yield {
                'title': title,
                'post_date': post_date,
                'post_url': post_url,
                'company_name': company_name,
                'closing_date': closing_date,
            }

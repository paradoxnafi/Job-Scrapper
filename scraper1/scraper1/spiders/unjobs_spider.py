import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time

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
            post_url = job.css('.jtitle::attr(href)').get()
            company_name = job.css('div.job::text').get()

            # company_name = company_name.strip() if company_name else ''
            yield {
                'title': title,
                'post_date': post_date,
                'post_url': post_url,
                'company_name': company_name,
            }
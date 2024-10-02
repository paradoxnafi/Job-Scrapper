import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time


class LinkedInJobSpider(scrapy.Spider):
    name = 'linkedin_spider'
    start_urls = ['https://www.linkedin.com/jobs/search?location=Timor-Leste&geoId=101101678&currentJobId=3977525047&position=1&pageNum=0']

    def __init__(self, *args, **kwargs):
        super(LinkedInJobSpider, self).__init__(*args, **kwargs)

        # Set up Selenium WebDriver with Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)

        time.sleep(5)

        # Scroll to the bottom of the page to load all job listings
        scroll_pause_time = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Extract the job posts available at the current scroll position
            sel = Selector(text=self.driver.page_source)
            job_posts = sel.css('ul.jobs-search__results-list li')

            # Scroll down to the bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load the page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                for job in job_posts:
                    # Extract the data as specified
                    post_link = job.css('a.base-card__full-link::attr(href), a.base-card::attr(href)').get()
                    job_title = job.css('h3.base-search-card__title::text').get()
                    company_name = job.css('h4.base-search-card__subtitle a::text').get()
                    posted_date = job.css('time.job-search-card__listdate::attr(datetime), time.job-search-card__listdate--new::attr(datetime)').get()
                    job_urn = job.css('div.base-card.relative.w-full.job-search-card::attr(data-entity-urn)').get()

                    # Handle potential None values and strip whitespace if possible
                    job_title = job_title.strip() if job_title else ''
                    company_name = company_name.strip() if company_name else ''
                    job_id = job_urn.split(':')[-1] if job_urn else ''

                    # Yield the extracted data as a dictionary
                    yield {
                        'title': job_title,
                        'post_date': posted_date,
                        'post_url': post_link,
                        'company_name': company_name,
                        'job_id': job_id,
                    }
                break
            last_height = new_height

    def closed(self, reason):
        self.driver.quit()

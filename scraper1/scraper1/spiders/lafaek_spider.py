import scrapy
import time
from datetime import datetime, timedelta


def format_date(datetime_str):
    try:
        if 'hours ago' in datetime_str:
            hours = int(datetime_str.split(' ')[0])
            adjusted_time = datetime.now() - timedelta(hours=hours)
            return adjusted_time.strftime("%Y-%d-%m")
        
        dt = datetime.strptime(datetime_str, "%B %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return "Unknown"


class LafaekSpider(scrapy.Spider):
    name = "lafaek_spider"
    allowed_domains = ["www.lafaek.tl"]
    start_urls = ["https://www.lafaek.tl/category/about-care/vaga-serbisu/"]

    def parse(self, response):
        posts = response.css('.posts_container article')
        for post in posts:
            url = post.css('.post_title a').attrib.get('href')
            if url:
                yield scrapy.Request(url=url, callback=self.parse_post)
            else:
                self.log("Post URL missing.")

            time.sleep(0.25)

        load_more_url = response.css('a.next.page-numbers').attrib.get('href')
        if load_more_url:
            yield scrapy.Request(url=load_more_url, callback=self.parse)
        else:
            self.log("No more pages to load or 'Next' button missing.")

    def parse_post(self, response):
        title = response.css('.sc_layouts_title_caption::text').get(default='Untitled')
        
        post_date_str = response.css('.post_meta_item.post_date::text').get()
        post_date = format_date(post_date_str) if post_date_str else "Unknown"
        # closing_date = response.css('.post_content p strong::text').getall()[-1]
        
        job_description_doc = response.css('a.wp-block-file__button.wp-element-button').attrib.get('href', '')

        yield {
            'title': title,
            'post_date': post_date,
            'post_url': response.url,
            # 'closing_date': closing_date,
            'company_name': '',
            'job_description_doc': job_description_doc,
        }

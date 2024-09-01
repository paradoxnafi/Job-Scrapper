## Job listing urls
1. https://unjobs.org/duty_stations/dil (done)
2. https://www.linkedin.com/jobs/search?location=Timor-Leste (done)
3. www.vagaservisu.com (done)
4. www.vagaservisutimorleste.wordpress.com (Last post was in 2017, to do)
5. https://vagas.cfp.gov.tl/ (not suitable, all pdf images)
6. https://www.facebook.com/groups/383284709293856/ (to do)
7. https://www.lafaek.tl/category/about-care/vaga-serbisu/ (to do)
8. https://simuweb.sefope.gov.tl/ (password protected)

## Create a scrapy project
    scrapy startproject name

## Create a spider
    scrapy genspider name url

## scrapy interactive shell
1. start interactive shell <br>
    `scrapy shell`
2. Fetch html content of a website <br>
    `fetch("https://books.toscrape.com/")` This is stored under variable `response`
3. Access css elements <br>
    `response.css('div.product_price')`
4. Save specific css element in another variable <br>
    `books = response.css('div.product_price')`
5. Get text from a `a tag` <br>
    `book0 = books[0]` <br>
    `book0.css('h3 a::text').get()`
6. Traverse through multiple tags and classes <br>
    `book0.css('.product_price .price_color::text').get()`
7. Get an attribute <br>
    `book0.css('h3 a').attrib['href]`
8. Get nested tags and attributes <br>
    `response.css('li.next a ::attr(href)').get()`


## Run a spider
Navigate to project root and run <br>
    `crapy crawl spider_name`

## Run a specific file with output stored in a file
    `scrapy runspider quotes_spider.py -o quotes.jsonl`
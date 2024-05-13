import scrapy

class Telegraph(scrapy.Spider):
    name = "abcnews_spider"
    allowed_domains = ["abcnews.go.com"]
    start_urls = [
        "https://abcnews.go.com/"
    ]

    def parse(self, response):
        print(response)
        categories_to_scrap = ['politics', 'sports', 'business', 'lifestyle']

        news_categories = response.css('#global-nav > ul > li.none.more > div > ul > li > a::text').getall()
        news_categories_urls = response.css('#global-nav > ul > li.none.more > div > ul > li > a::attr(href)').getall()

        for category, url in zip(news_categories, news_categories_urls):
            if category.strip().lower() in categories_to_scrap:
                yield scrapy.Request(url, self.parse_articles, cb_kwargs=dict(category=category.strip().lower()))


    def parse_articles(self, response, category):
        section_1 = response.css('div.band__lead.band > div > div > div > a::attr(href)').getall()
        section_2 = response.css('div.block__double-column.block > section > section > div > h2 > a::attr(href)').getall()

        for url in section_1 + section_2:
            yield scrapy.Request(url, self.parse_story, cb_kwargs=dict(category=category))


    def parse_story(self, response, category):
        heading = response.css('header > div > h1::text').get()
        article = response.css('div.Article > section > article > section > p::text').getall()

        article = ' '.join([paragraph for paragraph in article])

        yield dict(url=response.url, category=category, heading=heading, article=article)

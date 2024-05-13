import scrapy

class Telegraph(scrapy.Spider):
    name = "foxnews_spider"
    allowed_domains = ["foxnews.com"]
    start_urls = [
        "https://www.foxnews.com/"
    ]

    def parse(self, response):
        categories_to_scrap = ['politics', 'sports', 'lifestyle']

        news_categories = response.css('#main-nav > ul > li > a::text').getall()
        news_categories_urls = response.css('#main-nav > ul > li > a::attr(href)').getall()

        for category, url in zip(news_categories, news_categories_urls):
            if category.lower() in categories_to_scrap:
                yield scrapy.Request(url, self.parse_articles, cb_kwargs=dict(category=category.lower()))

    
    def parse_articles(self, response, category):
        section_1 = response.css('div.info > header > h2 > a::attr(href)').getall()
        section_2 = response.css('div.info > header > h4 > a::attr(href)').getall()

        for url in section_1 + section_2:
            article_url = "https://www.foxnews.com/" + url

            yield scrapy.Request(article_url, self.parse_story, cb_kwargs=dict(category=category))

    
    def parse_story(self, response, category):
        heading = response.css('main > article > header > h1::text').get()
        article = response.css(' div.article-content > div.article-body > p::text').getall()

        article = ' '.join([paragraph for paragraph in article])

        yield dict(url=response.url, category=category, heading=heading, article=article)


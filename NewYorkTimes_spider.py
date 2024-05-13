import scrapy

class Telegraph(scrapy.Spider):
    name = "newyorktimes_spider"
    allowed_domains = ["nytimes.com"]
    start_urls = [
        "https://www.nytimes.com/"
    ]

    def parse(self, response):
        categories_to_scrap = ['politics', 'sports', 'business', 'arts']

        news_categories = response.css('header > div.css-1d8a290 > ul > li > a::text').getall()
        news_categories_urls = response.css('header > div.css-1d8a290 > ul > li > a::attr(href)').getall()

        for category, url in zip(news_categories, news_categories_urls):
            if category.lower() in categories_to_scrap:
                yield scrapy.Request(url, self.parse_articles, cb_kwargs=dict(category=category.lower()))

    
    def parse_articles(self, response, category):
        section_1 = response.css('ol > li > article > div > h2 > a::attr(href)').getall()
        section_2 = response.css('ol > li > div > div.css-1l4spti > a::attr(href)').getall()

        for url in section_1 + section_2:
            article_url = "https://www.nytimes.com" + url
            yield scrapy.Request(article_url, self.parse_story, cb_kwargs=dict(category=category))

    
    def parse_story(self, response, category):
        heading = response.css('header > div.css-1vkm6nb > h1::text').get()
        article = response.css('#story > section > div.css-1fanzo5  > div > p::text').getall()

        story = ' '.join([paragraph for paragraph in article])

        yield dict(url=response.url, category=category, heading=heading, article=article)

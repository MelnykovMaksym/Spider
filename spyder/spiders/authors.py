import scrapy
from spyder.items import SpyderItem


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            Item = SpyderItem()
            Item['keywords'] = quote.xpath("div[@class='tags']/a/text()").extract()
            Item['author'] = quote.xpath("span/small/text()").extract_first()
            Item['quote'] = ''.join(
                    c for c in quote.xpath("span[@class='text']/text()").extract_first() if c not in '\r\t\n"“”"”')
            Item['url'] = 'quotes.toscrape.com' + quote.xpath("span/a/@href").extract_first()
            yield Item

        # for quote in response.xpath("/html//div[@class='quote']"):
        #     yield {
        #         "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
        #         "author": quote.xpath("span/small/text()").extract_first(),
        #         "quote": ''.join(
        #             c for c in quote.xpath("span[@class='text']/text()").extract_first() if c not in '\r\t\n"“”"”'),
        #         "url": 'quotes.toscrape.com' + quote.xpath("span/a/@href").extract_first()
        #     }

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)



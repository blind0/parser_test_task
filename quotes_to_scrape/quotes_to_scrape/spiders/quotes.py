import scrapy
from scrapy.exceptions import CloseSpider


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ["https://quotes.toscrape.com/page/1/"]



    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                "author": quote.xpath("span/small[@class='author']/text()").get(),
                "text": quote.xpath("span[@class='text']/text()").get(),
                "tags": quote.xpath("div[@class='tags']/a[@class='tag']/text()").getall()
            }
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is None:
            raise CloseSpider("last page")
        
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page, callback=self.parse)

import scrapy
from scrapy.exceptions import CloseSpider

from quotes_to_scrape.items import Quotes


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ["https://quotes.toscrape.com/page/1/"]



    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            item = Quotes()
            
            item["author"] = quote.xpath("span/small[@class='author']/text()").get()
            item["text"] = quote.xpath("span[@class='text']/text()").get()
            item["tags"] = quote.xpath("div[@class='tags']/a[@class='tag']/text()").getall()
            
            about_link = quote.xpath("span/a[1]/@href").get()
            
            yield response.follow(about_link, callback=self.parse_about, meta={"item":item})

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is None:
            raise CloseSpider("last page")
        
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page, callback=self.parse)

    def parse_about(self, response):
        item = response.meta['item']
        item["born_date"] = response.xpath("//span[@class='author-born-date']/text()").get()
        item["born_place"] = response.xpath("//span[@class='author-born-location']/text()").get()
        item["description"] = response.xpath("//div[@class='author-description']/text()").get()
        return item
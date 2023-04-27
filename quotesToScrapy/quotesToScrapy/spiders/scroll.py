import scrapy
from scrapy.loader import ItemLoader
from ..items import Quotes
from scrapy_playwright.page import PageMethod


class ScrollSpider(scrapy.Spider):
    name = "scroll"

    def start_requests(self):
        yield scrapy.Request(
            url="http://quotes.toscrape.com/scroll",
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.quote"),
                    PageMethod(
                        "evaluate",
                        "setInterval(function () {var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;}, 200);",
                    ),
                    PageMethod("wait_for_load_state", "networkidle"),
                ],
            },
        )

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            item = ItemLoader(Quotes(), quote)
            item.add_xpath("phrase", ".//span[@class='text']/text()")
            item.add_xpath("author", ".//span[2]/small/text()")
            yield item.load_item()
        
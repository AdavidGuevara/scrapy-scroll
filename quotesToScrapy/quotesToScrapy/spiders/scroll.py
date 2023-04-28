from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from ..items import Quotes
import scrapy


class ScrollSpider(scrapy.Spider):
    name = "scroll"

    def start_requests(self):
        yield scrapy.Request(
            url="http://quotes.toscrape.com/scroll",
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [PageMethod("wait_for_selector", ".quote")],
                "playwright_include_page": True,
            },
            errback=self.close_page,
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        # Se indica de manera explicita el numero de items:
        contador = 2
        while True:
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await page.wait_for_selector(f".quote:nth-child({contador * 10})")
            if contador == 10:
                break
            contador += 1
        s = Selector(text=await page.content())
        await page.close()
        for quote in s.xpath("//div[@class='quote']"):
            item = ItemLoader(Quotes(), quote)
            item.add_xpath("phrase", ".//span[@class='text']/text()")
            item.add_xpath("author", ".//span[2]/small/text()")
            yield item.load_item()

    async def close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

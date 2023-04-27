import scrapy


class Quotes(scrapy.Item):
    phrase = scrapy.Field()
    author = scrapy.Field()

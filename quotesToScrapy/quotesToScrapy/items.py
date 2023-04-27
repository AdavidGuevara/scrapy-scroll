import scrapy


class Quotes(scrapy.Item):
    phrase = scrapy.Field()
    autor = scrapy.Field()

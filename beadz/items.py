import scrapy


class BeadzItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()

import scrapy

from scrapy.loader import ItemLoader

from ..items import BeadzItem
from itemloaders.processors import TakeFirst


class BeadzSpider(scrapy.Spider):
	name = 'beadz'
	start_urls = ['https://bea.dz/publication.html']

	def parse(self, response):
		post_links = response.xpath('//div[@class="banner-img"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="main_blog_details"]//h4/text()').get()
		description = response.xpath('//div[@class="main_blog_details"]//text()[normalize-space() and not(ancestor::h4)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BeadzItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()

import scrapy

from scrapy.loader import ItemLoader

from ..items import BagbankdeItem
from itemloaders.processors import TakeFirst


class BagbankdeSpider(scrapy.Spider):
	name = 'bagbankde'
	start_urls = ['https://www.bag-bank.de/aktuelles/presse/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="col-sm-6 presseTitle"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="col-lg-8 col-md-10 cke-box"]//p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="col-sm-12"]/text()').get()

		item = ItemLoader(item=BagbankdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

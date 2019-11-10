# -*- coding: utf-8 -*-
import scrapy
from Scraper.items import Article

import re



class BostonHeraldSpider(scrapy.Spider):
	name = 'boston_herald'
	
	allowed_domains = ['www.bostonherald.com']
	start_urls = ['https://www.bostonherald.com']

	year_limit = 2014


	def parse(self, response):
		print('\n\n STARTING \n\n')

		categories = response.css('ul#primary-menu ul.sub-menu li a::attr(href)').getall()

		for category_url in categories:
			if not category_url.startswith(self.start_urls[0]):
				category_url = self.start_urls[0] + category_url

			yield scrapy.Request(
				url = category_url, 
				callback = self.parse_categories
			)


	def parse_categories(self, response):
		print('\n\n PARSING CATEGORIES \n\n')

		next_page = response.css('a.load-more::attr(href)').get()


		if next_page is not None or '/page/' in response.url:
			articles = response.css('div.article-info a.article-title::attr(href)').getall()

			if next_page:
				regex = re.search(r'^' + re.escape(self.start_urls[0]) + r'/(.+?)/page.*', next_page)
			else:
				regex = re.search(r'^' + re.escape(self.start_urls[0]) + r'/(.+?)/page.*', response.url)
			
			categories_tags = regex.group(1).split('/')

			for article_url in articles:
				yield scrapy.Request(
					url = article_url, 
					callback = self.parse_article, 
					meta = {
						'category' : categories_tags
					}
				)

			yield scrapy.Request(
				url = next_page, 
				callback = self.parse_categories
			)


	def parse_article(self, response):
		print('\n\n PARSING ARTICLE \n\n')

		article = Article()

		datetime = response.css('div.meta div.time time::attr(datetime)').getall()


		if self.year_limit is not None and int(datetime[0].split('-')[0]) < self.year_limit:
			raise CloseSpider('Reached Year Limit')


		article['url'] = response.url
		
		article['title'] = response.css('head title::text').get()
		
		article['date'] = datetime
		
		article['journal'] = 'Boston Herald'

		article['author'] =  response.css('div.by-line a.author-name::text').get()
		
		article['category'] = response.meta['category']
		
		article['body'] = ' '.join(response.css('div.body-copy p::text').getall())
		
		article['tags'] = response.css('div.tags li a::text').getall()

		article['media'] = response.css('div#content main#main article div.article-content img::attr(src)').getall()


		yield(article)










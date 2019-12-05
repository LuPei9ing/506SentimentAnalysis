# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from Scraper.items import Article
from scrapy.exceptions import CloseSpider

import re
from datetime import datetime


class BostonGlobeSpider(scrapy.Spider):
	name = 'boston_globe'
	allowed_domains = ['www.bostonglobe.com']
	start_urls = ['https://www.bostonglobe.com/']

	base_url = 'https://www.bostonglobe.com'

	visited, to_crawl = [], []
	
	year_limit = 2014
	old_articles_counter = 0
	old_articles_limit = 10


	def parse(self, response):
		outgoing_links = response.css('a::attr(href)').getall()

		for url in outgoing_links:
			if url not in self.visited and (url.startswith(self.allowed_domains[0]) or url.startswith('/')):
				if url.startswith('/'):
					url = self.base_url + url

				self.visited.append(url)
				is_article = re.search(r'^' + self.base_url + r'(.*/story.html).*', url)

				if is_article:
					yield SplashRequest(
						url = self.base_url + is_article.group(1), 
						callback = self.parse_article, 
						args = {
							'wait' : 0.5
						}
					)
				else:
					yield scrapy.Request(
						url = url, 
						callback = self.parse
					)


	def parse_article(self, response):
		article = Article()

		date = response.css('div#header-container div.article span.datetime span.date::text').get().replace('Updated ', '')
		time = response.css('div#header-container div.article span.datetime span.time::text').get().replace('.', '')

		try:
			year = int(date.replace(', ', ' ').split(' ')[-2])
		except:
			year = 2019

		if year >= self.year_limit:
			self.old_articles_counter = 0

			article['title'] = response.css('div#header-container div.article h1.headline::text').get()
			
			article['journal'] = 'Boston Globe'
			
			article['author'] = response.css('div#header-container div.article div.authors span.author span.bold:not(.seperator)::text').getall()
			
			article['date'] = str(datetime.strptime(''.join([date, time]), '%B %d, %Y, %I:%M %p'))
			
			article['body'] = ' '.join(response.css('div.article p.paragraph span::text').getall())

			article['media'] = response.css('div.fusion-app article img::attr(src)').getall()
		else:
			self.old_articles_counter += 1

			if self.old_articles_counter > self.old_articles_limit:
				raise CloseSpider('Too many consecutive old articles')

		
		yield(article)












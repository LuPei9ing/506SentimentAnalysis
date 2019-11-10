# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from Scraper.items import Article


class WburSpider(scrapy.Spider):
	name = 'wbur'
	allowed_domains = ['www.wbur.org']
	base_url = 'https://www.wbur.org'
	start_urls = [
		'https://www.wbur.org/onpoint/archive/1', 
		'https://www.wbur.org/hereandnow/archive/1', 
		'https://www.wbur.org/radioboston/archive/1', 
		'https://www.wbur.org/onlyagame/archive/1', 
		'https://www.wbur.org/modernlove/archive/1', 
		'https://www.wbur.org/commonhealth/archive/1', 
		'https://www.wbur.org/cognoscenti/archive/1'
	]

	year_limit = 2014


	def parse(self, response):
		curr_url = response.url.split('/')
		next_page = int(curr_url[-1]) + 1
		
		date = response.css('section.section--island div.row:last-child span.card-date::text').get()
		try:
			curr_year = int(date.split(', ')[-1])
		except:
			curr_year = 2019

		if curr_year >= self.year_limit:
			yield scrapy.Request(
				url = '/'.join(curr_url[:-1]) + '/' + str(next_page), 
				callback = self.parse
			)

		articles = response.css('div#root div.surface div.view div.row a::attr(href)').getall()

		for article_url in articles:
			yield scrapy.Request(
				url = self.base_url + article_url, 
				callback = self.parse_article
			)


	def parse_article(self, response):
		article = Article()


		article['title'] = response.css('head title::text').get()
		
		article['journal'] = 'WBUR'
		
		article['source'] = response.url.split('/')[3]
		
		article['date'] = response.css('header.article-section--title div.article-meta span.article-meta-item--date span::text').get()
		
		article['author'] = response.css('header.article-section--title div.article-meta li.article-meta-item--author a::text').getall()
		
		article['body'] = ' '.join(response.css('div#root div.surface section.article-section--content p::text').getall())

		article['media'] = response.css('article.article img::attr(src)').getall()

		
		yield(article)











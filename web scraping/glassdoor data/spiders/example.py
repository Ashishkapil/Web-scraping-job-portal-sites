# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
main_url = "https://www.glassdoor.ca"
class ExampleSpider(scrapy.Spider):
    name = 'example'
    #allowed_domains = ['https://www.glassdoor.co.in/Job/canada-data-jobs-SRCH_IL.0,6_IN3_KE7,11.htm']
    start_urls = ['https://www.glassdoor.ca/Job/canada-data-jobs-SRCH_IL.0,6_IN3_KE7,11.htm']
    main_url = "https://www.glassdoor.ca"
    #handling javascript pages
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
               endpoint='render.html',
                args={'wait': 0.5},
            )
    
    def parse(self, response):
        urls = response.css('li.jl > div > div.flexbox > div > a::attr(href)').extract_first()
        urls = main_url + urls
        self.log(urls)
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse_details)
            

    def parse_details(self, response):
       
            if response.css('div[id = JobDescription] > span[id = TrackingJobBody] > ul'):
              yield {         
                      'Job Post' : response.css('div.opening.col-sm-12 > h1::text').extract_first(),
                      'Location' : response.css('div.opening.col-sm-12 > h2::text').extract_first(),
                      'Description' : "\n".join(response.css('div[id = JobDescription] > span[id = TrackingJobBody] > ul > li::text').extract())
                     }
            elif response.css('div[id = JobDescription] > span[id = TrackingJobBody]'):
             yield {         
                      'Job Post' : response.css('div.opening.col-sm-12 > h1::text').extract_first(),
                      'Location' : response.css('div.opening.col-sm-12 > h2::text').extract_first(),
                      'Description' : "\n".join(response.css('div[id = JobDescription] > span[id = TrackingJobBody]').xpath(".//text()").extract()),
                      'Description2' : "\n".join(response.css('div[id = JobDescription] > span[id = TrackingJobBody]::text').extract())
                     }
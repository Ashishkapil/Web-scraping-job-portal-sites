# -*- coding: utf-8 -*-
import scrapy
class MonsterComSpider(scrapy.Spider):
    name = 'monsterca'
    #allowed_domains = ['www.monster.ca']
    start_urls = ['https://www.monster.ca/jobs/search/?q=data-analyst&page=1']
    def parse(self, response):
        urls = response.css('div.jobTitle > h2 > a::attr(href)').extract()
       
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse_details)

    #crawling all the pages
        next_page_url = response.xpath('//head/link[@rel="next"]/@href').extract_first()
        
        if next_page_url:
           next_page_url = response.urljoin(next_page_url) 
           yield scrapy.Request(url = next_page_url, callback = self.parse)            


    def parse_details(self,response):
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
             
 
       
        #'Description' : response.css('div[id = JobDescription]').extract()
                  
            
        
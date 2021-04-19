# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 20:44:39 2021

@author: Shirin
"""

import scrapy
import json
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

"""
from urllib.parse import urlencode
API = 'd2086abf-21dc-43cc-b75c-2817f7eea899'


def get_url(url):
    payload = {'api_key': API, 'proxy': 'residential', 'timeout': '20000', 'url': url}
    proxy_url = 'https://api.webscraping.ai/html?' + urlencode(payload)
    return proxy_url
"""
class InstaScraper(scrapy.Spider):
 name = "instaScraper"

 def start_requests(self):
        urls = [
            'https://www.instagram.com/accounts/login/',
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
    
 def parse(self, response):
       token = response.css('form input::attr(value)').extract_first()
       return FormRequest.from_response(response, formdata={
           'csrf_token': token,
           'username' : "shirin__ebadi",
           'password':"password"},callback = self.start_scraping)
   
 

   
 def start_scraping(self,response):
      open_in_browser(response)
      x = response.xpath("//script[starts-with(.,'window._sharedData')]/text()").extract_first()
      json_string = x.strip().split('= ')[1][:-1]
      jsondata = json.loads(json_string)
      full_name = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']
      biography = jsondata['entry_data']['ProfilePage'][0]["graphql"]["user"]["biography"]
      website = jsondata['entry_data']['ProfilePage'][0]["graphql"]["user"]["external_url"]
      numberOfollowers = jsondata['entry_data']['ProfilePage'][0]["graphql"]["user"]["edge_followed_by"]["count"]
      numberOfollowing = jsondata['entry_data']['ProfilePage'][0]["graphql"]["user"]["edge_follow"]["count"]
      businessacount = jsondata['entry_data']['ProfilePage'][0]["graphql"]["user"]["is_business_account"]
      if businessacount:
       typeP = "Business"
      isprivate = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']
      if isprivate:
       public = "private"
      numberOfPosts = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count']
  
      BasicInfo = [{"full_name": full_name,
                "biography": biography,
                "Website": website,
                "No. followers": numberOfollowers,
                "No. following": numberOfollowing,
                "Type of Account": typeP,
                "Public/Private": public,
                "No. posts": numberOfPosts}]
      if numberOfPosts != 0 and numberOfPosts > 11 :
       numberOfPosts = 11
      
      PostInfo = []
      for n in range (numberOfPosts):
        typeOfPost = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['__typename']
        dimensions =  jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['dimensions']
        urlDisplay =  jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['display_url']
        caption =  jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['edge_media_to_caption']['edges'][0]['node']['text']
        comments = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['edge_media_to_comment']['count']
        likes = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][n]['node']['edge_liked_by']['count']
        
        PostInfo.append([{"typeOfPost": typeOfPost,
                          "dimension":dimensions,
                          "url": urlDisplay,
                          "caption": caption,
                          "No. comments": comments,
                          "No. likes": likes}])
      
      
      
      totalInfo = BasicInfo,PostInfo
      json.dumps(totalInfo)
      
      file = open("scrapy.txt", "w", encoding='utf-8')
      file.write(repr(totalInfo))
      file.close() 
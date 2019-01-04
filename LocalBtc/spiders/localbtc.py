# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 21:19:18 2018

@author: Talha.Iftikhar
"""
import csv
import scrapy
from datetime import datetime
from LocalBtc.items import LocalbtcItem
import os.path
class localbtc(scrapy.Spider):
    name="localbtcvalues"
    start_urls=["https://localbitcoins.com"]
    
    
        
#         with open('localbtc.csv', 'a', newline = '') as csvFile:
#             csvWriter = csv.writer(csvFile, delimiter = ',')
#             csvWriter.writerow(itemres)
    
    def parse(self,response):
        url="https://localbitcoins.com/instant-bitcoins/?action=buy&country_code=PK&amount=&currency=PKR&place_country=PK&online_provider=ALL_ONLINE&find-offers=Search"
        yield scrapy.Request(url,callback=self.parse_value)
        
    def parse_value(self,response):
        item=LocalbtcItem()
        item["price"]=response.xpath("//td[contains(@class,'column-price')]/text()").extract_first().strip()
        item["date"]=datetime.now().date()
        item["hourmin"]=str(datetime.now().hour)+":"+ str(datetime.now().minute) if len(str(datetime.now().minute))>1 else str(datetime.now().hour)+":"+"0"+str(datetime.now().minute)
        yield scrapy.Request(url ="https://localbitcoins.com/instant-bitcoins/?action=sell&country_code=PK&amount=&currency=PKR&place_country=PK&online_provider=ALL_ONLINE&find-offers=Search",callback=self.save_results, meta={'price': item["price"],'date':item["date"],'hourmin':item["hourmin"]})
        
    def save_results(self,response):
        date = response.meta['date']
        price = response.meta['price']
        hourmin=response.meta['hourmin']
        for r in ((",", ""), ("\"", "")):
            price = price.replace(*r)
            
        new = ''
        for letter in price:
            if not(letter.isalpha()):
    	        new+=letter
        price = new    
        price=price.strip()
        
        file_exists = os.path.isfile('C:/Users/Talha.Iftikhar/LocalBtc/LocalBtc/localbtc.csv')

        with open('C:/Users/Talha.Iftikhar/LocalBtc/LocalBtc/localbtc.csv', "a",newline='\n') as csv_file:
#             price=price.replace(',','')
#             price=price.replace('"','')
            #print(price)
             fieldnames = ['price', 'date','hourmin']
             
             writer = csv.DictWriter(csv_file,fieldnames=fieldnames)#delimiter=','
            #for line in text:
             if not file_exists:
                 writer.writeheader()
             writer.writerow({'price':price,'date':date,'hourmin':hourmin})
            
from pathlib import Path 
import scrapy 
import logging
from array import array
import os
from scrapy.http import Request
from lockdocsearcher.items import LockdocItem
logging.getLogger('scrapy').setLevel(logging.WARNING)

class lockbitspider(scrapy.Spider):
    name = "spiderlockbit"

    start_urls = [
        "http://lockbit7z2jwcskxpbokpemdxmltipntwlkmidcll2qirbu7ykg46eyd.onion/secret/" # top directory you want to search through
    ]
    
    def parse(self,response):
        for link in response.xpath('//td[@class="link"]'):
            url = link.xpath('./a/@href').get()
            if str(url) != "../":
                urlcheck = str(url)
                if urlcheck.endswith("/") == True:
                    url = response.urljoin(url)
                    urllist = open("urllist.txt", "a")
                    urllist.write(str(url) + ",\n")
                    urllist.close
                    yield response.follow(url, callback=self.parse)
                filetypecheck = urlcheck.split('.')[-1]
                if filetypecheck in ("pdf","docx","doc","txt","xls","xlsx","csv","eml","msg"): #file types you want to download
                    item = LockdocItem()
                    file_url = response.urljoin(url)
                    item['file_urls'] = [file_url]
                    item['original_file_name'] = file_url.split('/')[-1]
                    yield item
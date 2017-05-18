#!/usr/bin/env python2
 
import scrapy

class RoomSpider(scrapy.Spider):
   
    #CONCURRENT_REQUESTS = 200    
    CONCURRENT_REQUESTS = 20    
    URL = 'https://sws.unimelb.edu.au/2017/'
    
    name = "room"
    start_urls = [URL]
    rooms = []
    custom_settings = {
        'CONCURRENT_REQUESTS': 1
    }

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata = {'__EVENTTARGET': 'LinkBtn_locations', '__EVENTARGUMENT': ''},
            callback = self.process_rooms
        )

    def process_rooms(self, response):
        self.rooms = response.xpath('//select[@id="dlObject"]/option/@value').extract()
        self.submission_response = response
        return self.post_data()

    def post_data(self):
        c = self.CONCURRENT_REQUESTS
        _d = []
        while c > 0 and len(self.rooms) > 0:
            c -= 1
            _d.append(self.rooms.pop())

        return scrapy.FormRequest.from_response(
            self.submission_response, 
            clickdata = {'name': 'bGetTimetable'}, 
            formdata = {'dlObject': _d,'lbWeeks': 't', 'RadioType': 'location_list;cyon_reports_list_url;dummy'}, 
            dont_filter = True,
            callback = self.get_data
        )

    def get_data(self, response):
        return scrapy.Request(
            url = self.URL + "Reports/List.aspx", 
            dont_filter = True,
            callback = self._save
        )

    def _save(self, response):
        self.save_room(response)
        return self.post_data()

    def save_room(self, response):
        print(response.text);


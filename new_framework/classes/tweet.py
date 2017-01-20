
import json
import re

import time_functions
import datetime

class Tweet:
    """
    Class containing the characteristics of a tweet that mentions 
        an entity and time
    """
    def __init__(self):
        self.dict = {}
        self.id = False
        self.user = False
        self.text = False
        self.datetime = False
        self.string_refdates = []
        self.refdates = []
        self.entities = []
        self.entities_score = []
        self.cityrefs = []

    def import_tweetdict(self,tweetdict):
        keys = tweetdict.keys()
        self.id = tweetdict['id']
        self.user = tweetdict['user']
        self.text = tweetdict['text']
        self.datetime = self.import_datetime(tweetdict['datetime'])
        self.string_refdates, self.refdates = self.import_refdates(tweetdict['refdates']) 
        self.entities, self.entities_score = self.import_entities(tweetdict['entities']) 
        self.cityrefs = tweetdict['cityrefs'] 

    def import_twiqsdict(self,twiqsdict):
        month = {"Jan" : "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", "May" : "05", "Jun" : "06", "Jul" : "07", 
            "Aug" : "08", "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"}
        date_time = re.compile(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d+) (\d{2}:\d{2}:\d{2}) \+\d+ (\d{4})")
        self.id = twiqsdict['id']
        self.user = twiqsdict['user']['screen_name']
        self.text = twiqsdict['text']
        dt = date_time.search(twiqsdict['created_at']).groups()
        timefields = [int(f) for f in dt[2].split(':')]
        self.datetime = datetime.datetime(int(dt[3]), int(month[dt[0]]), int(dt[1]), timefields[0], timefields[1], timefields[2])

    def return_dict(self):
        tweetdict = {
            'id':self.id, 
            'user':self.user, 
            'text':self.text, 
            'datetime':str(self.datetime),
            'refdates':dict([(x[0],str(x[1])) for x in self.string_refdates]),
            'entities':dict(self.entities_score),
            'cityrefs':self.cityrefs
        }
        return tweetdict

    def set_id(self,tid):
        self.id = tid

    def set_user(self,user):
        self.user = user

    def set_tweettext(self,text):
        self.text = text

    def set_datetime(self,datetime):
        self.datetime = datetime

    def import_datetime(self,datetime):
        date,time = datetime.split()
        dt = time_functions.return_datetime(date,time,minute=True,setting='vs')
        return dt

    def import_refdates(self,refdates):        
        imported_string_refdates = [(x[0],time_functions.return_datetime(x[1].split()[0],x[1].split()[1],minute=True,setting='vs')) for x in list(refdates.items())]
        imported_refdates = [x[1] for x in imported_string_refdates]
        return imported_string_refdates,imported_refdates

    def set_refdates(self,refdates):
        self.string_refdates = refdates
        self.refdates = [x[1] for x in refdates]

    def import_entities(self,entities_score_dict):
        entities_score = entities_score_dict.items()
        entities = [x[0] for x in entities_score]
        return entities, entities_score

    def set_entities(self,entities_score):
        self.entities = [x[0] for x in entities_score]
        self.entities_score = entities_score

    def set_cityrefs(self,cityrefs):
        self.cityrefs = cityrefs

    def set_emotions(self,emotions):
        pass
        #self.emotions = emotions
        #self.dict['emotions'] = dict(emotions)

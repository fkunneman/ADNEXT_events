
import json

import time_functions

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
        self.string_refdates = False
        self.refdates = False
        self.entities = False

    def import_tweetdict(self,tweetdict):
        keys = tweetdict.keys()
        self.id = tweetdict['id']
        self.user = tweetdict['user']
        self.text = tweetdict['text']
        self.datetime = self.import_datetime(tweetdict['datetime'])
        self.string_refdates, self.refdates = self.import_refdates(tweetdict['refdates']) if 'refdates' in keys else False, False
        #self.cityrefs = self.import_cityrefs(tweetdict['cityrefs']) if 'cityrefs' in keys else False
        self.entities, self.entities_score = self.import_entities(tweetdict['entities']) if 'entities' in keys else False, False
        
    def return_dict(self):
        tweetdict = {
            'id':self.id, 
            'user':self.user, 
            'text':self.text, 
            'datetime':str(self.datetime),
            'refdates':dict([(x[0],str(x[1])) for x in self.string_refdates]),
            'entities':dict(self.entities_score)
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

    def import_entities(self,entities_score):
        imported_entities = [x[0] for x in entities_score]
        imported_entities_score = [(x[0],float(x[1])) for x in entities_score]
        return entities, entities_score

    def set_entities(self,entities_score):
        self.entities = [x[0] for x in entities_score]
        self.entities_score = entities_score
        self.dict['entities'] = dict(entities_score)

    def import_cityrefs(self,cityrefs):
        pass

    def set_cityrefs(self,cityrefs):
        pass
#self.cityrefs = cityrefs
        #self.dict['cityrefs'] = cityrefs

    def set_emotions(self,emotions):
        pass
        #self.emotions = emotions
        #self.dict['emotions'] = dict(emotions)

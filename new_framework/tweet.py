
class Tweet:
    """
    Class containing the characteristics of a tweet that mentions 
        an entity and time
    """
    def __init__(self,tweetdict):

        self.import_dict(tweetdict)
        self.refdates = False
        self.cityrefs = False
        self.entities = False

    def import_dict(self,tweetdict):

        self.dict = tweetdict
        self.set_id(tweetdict['id'])
        self.set_user(tweetdict['user'])
        self.set_datetime(tweetdict['datetime'])
        self.set_text(tweetdict['text'])

    def return_dict(self):
        return self.dict

    def set_id(self,tid):
        self.id = tid

    def set_user(self,user):
        self.user = user

    def set_datetime(self,dt):
        self.datetime = dt

    def set_text(self,text):
        self.text = text

    def set_refdates(self,refdates):
        self.refdates = refdates
        self.dict['refdates'] = refdates

    def set_entities(self,entities_score):
        self.entities = [es[0] for es in entities_score]
        self.entities_score = entities_score
        self.dict['entities'] = dict(entities_score)

    def set_cityrefs(self,cityrefs):
        self.cityrefs = cityrefs
        self.dict['cityrefs'] = cityrefs

    def set_emotions(self,emotions):
        self.emotions = emotions
        self.dict['emotions'] = dict(emotions)

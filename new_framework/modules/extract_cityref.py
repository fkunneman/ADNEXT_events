

from luiginlp.engine import Task, StandardWorkflowComponent, InputFormat, InputComponent, registercomponent, InputSlot, Parameter, BoolParameter

import json

from functions import cityref_extractor, helpers
from classes import tweet
from modules.extract_daterefs import ExtractDateref 

class ExtractCityrefTask(Task):

    in_dateref = InputSlot()

    citylist = Parameter()

    def out_cityref(self):
        return self.outputfrominput(inputformat='dateref', stripextension='.json', addextension='.cityref.json')

    def run(self):
        
        # read in citylist
        with open(self.citylist,'r',encoding='utf-8') as file_in:
            citylist = [line.strip() for line in file_in.read().strip().split('\n')]

        # read in tweets
        with open(self.in_dateref().path, 'r', encoding = 'utf-8') as file_in:
            tweetdicts = json.loads(file_in.read())

        # format as tweet objects
        tweets = []
        for td in tweetdicts:
            tweetobj = tweet.Tweet()
            tweetobj.import_tweetdict(td)
            tweets.append(tweetobj)

        # extract location
        for tweetobj in tweets:
            # remove already extracted time from the tweet, forming it into chunks
            datestrings = [sr[0] for sr in tweetobj.string_refdates]
            tweet_chunks = helpers.remove_pattern_from_string(tweetobj.text,datestrings)
            # extract city from chunks
            ce = cityref_extractor.CityrefExtractor(citylist)
            for chunk in tweet_chunks:
                ce.find_cityrefs(chunk)
            tweetobj.set_cityrefs(ce.return_cityrefs())

        # write to file
        outtweets = [tweet.return_dict() for tweet in tweets]
        with open(self.out_cityref().path,'w',encoding='utf-8') as file_out:
            json.dump(outtweets,file_out)
        
@registercomponent
class ExtractCityref(StandardWorkflowComponent):

    citylist = Parameter()

    config = Parameter()
    strip_punctuation = BoolParameter()
    to_lowercase = BoolParameter()
    skip_date = BoolParameter()
    skip_month = BoolParameter()
    skip_timeunit = BoolParameter()
    skip_day = BoolParameter()

    def accepts(self):
        return (
            InputFormat(self, format_id='dateref', extension='.dateref.json'),
            InputComponent(self, ExtractDateref, config=self.config, strip_punctuation=self.strip_punctuation, to_lowercase=self.to_lowercase, skip_datematch=self.skip_date, skip_monthmatch=self.skip_month, skip_timeunitmatch=self.skip_timeunit, skip_daymatch=self.skip_day)
        )
                    
    def autosetup(self):
        return ExtractCityrefTask

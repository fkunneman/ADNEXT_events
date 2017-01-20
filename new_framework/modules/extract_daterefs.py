

from luiginlp.engine import Task, StandardWorkflowComponent, InputFormat, InputComponent, registercomponent, InputSlot, Parameter, BoolParameter

import json

from functions import dutch_timex_extractor
from classes import tweet
from modules.tokenize_instances import Tokenize

class ExtractDaterefTask(Task):

    in_tokenized = InputSlot()

    skip_datematch = BoolParameter()
    skip_monthmatch = BoolParameter()
    skip_timeunitmatch = BoolParameter()
    skip_daymatch = BoolParameter()

    def out_dateref(self):
        return self.outputfrominput(inputformat='tokenized', stripextension='.tok.json', addextension='.dateref.json')

    def run(self):
        
        # read in tweets
        with open(self.in_tokenized().path, 'r', encoding = 'utf-8') as file_in:
            tweetdicts = json.loads(file_in.read())

        # format as tweet objects
        tweets = []
        for td in tweetdicts:
            tweetobj = tweet.Tweet()
            tweetobj.import_tweetdict(td)
            tweets.append(tweetobj)

        # extract daterefs
        for tweetobj in tweets:
            dte = dutch_timex_extractor.Dutch_timex_extractor(tweetobj.text, tweetobj.datetime)
            dte.extract_refdates(self.skip_datematch,self.skip_monthmatch,self.skip_timeunitmatch,self.skip_daymatch)
            dte.filter_future_refdates()
            tweetobj.set_refdates(dte.refdates)

        # write to file
        outtweets = [tweet.return_dict() for tweet in tweets]
        with open(self.out_dateref().path,'w',encoding='utf-8') as file_out:
            json.dump(outtweets,file_out)
        
@registercomponent
class ExtractDateref(StandardWorkflowComponent):

    skip_datematch = BoolParameter()
    skip_monthmatch = BoolParameter()
    skip_timeunitmatch = BoolParameter()
    skip_daymatch = BoolParameter()

    config = Parameter()
    strip_punctuation = BoolParameter()
    to_lowercase = BoolParameter()

    def accepts(self):
        return (
            InputFormat(self, format_id='tokenized', extension='tok.json'),
            InputComponent(self, Tokenize, config=self.config, strip_punctuation=self.strip_punctuation, lowercase=self.to_lowercase)
        )
                    
    def autosetup(self):
        return ExtractDaterefTask



from luiginlp.engine import Task, StandardWorkflowComponent, InputFormat, InputComponent, registercomponent, InputSlot, Parameter, IntParameter, BoolParameter

import json
import glob

from functions import event_ranker, helpers
from classes import event, tweet

class ExtractEventsTask(Task):

    in_entity = InputSlot()

    window_size = IntParameter()
    minimum_event_mentions = IntParameter()
    cut_off = IntParameter()

    def out_events(self):
        return self.outputfrominput(inputformat='entity', stripextension='-00.out.dateref.cityref.json', addextension='.events.json')

    def run(self):

        # collect tweet files
        tweet_directory = '/'.join(self.in_entity().path.split('/')[:-2])
        days_tweetfiles = helpers.return_tweetfiles_window(self.in_entity().path,self.window_size)
        tweetfiles = []
        for day in days_tweetfiles:
            tweetfiles.extend([ filename for filename in glob.glob(tweet_directory + '/' + day + '*') ])
    
        # read in tweets
        print('Reading in tweets')
        tweetdicts = []
        for tweetfile in tweetfiles:
            with open(tweetfile, 'r', encoding = 'utf-8') as file_in:
                tweetdicts.extend(json.loads(file_in.read()))

        # format as tweet objects
        tweets = []
        for td in tweetdicts:
            tweetobj = tweet.Tweet()
            tweetobj.import_tweetdict(td)
            tweets.append(tweetobj)

        # extract events
        print('Starting event extraction with',len(tweets),'tweets')
        er = event_ranker.EventRanker(tweets)
        events = er.extract_events(self.minimum_event_mentions,self.cut_off)

        # write to file
        outevents = [event.return_dict() for event in events]
        with open(self.out_events().path,'w',encoding='utf-8') as file_out:
            json.dump(outevents,file_out)
        
@registercomponent
class ExtractEvents(StandardWorkflowComponent):

    window_size = IntParameter(default=30)
    minimum_event_mentions = IntParameter(default=5)
    cut_off = IntParameter(default=2500)

    def accepts(self):
        return InputFormat(self, format_id='entity', extension='.entity.json')

    def autosetup(self):
        return ExtractEventsTask

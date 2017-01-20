

from luiginlp.engine import Task, StandardWorkflowComponent, InputFormat, InputComponent, registercomponent, InputSlot, Parameter, IntParameter, BoolParameter

import json
import glob
import os
import datetime 

from functions import event_ranker, helpers
from classes import event, tweet

class ExtractEventsTask(Task):

    in_tweetdir = InputSlot()

    end_date = Parameter()
    window_size = IntParameter()
    minimum_event_mentions = IntParameter()
    cut_off = IntParameter()

    def out_eventdir(self):
        return self.outputfrominput(inputformat='tweetdir', stripextension='.tweets', addextension='.events')

    def out_events(self):
        return self.outputfrominput(inputformat='tweetdir', stripextension='.tweets', addextension='.events/' + str(self.window_size) + '_' + self.end_date + '.events.json')

    def run(self):

        # if directory does not exist, create directory
        if not os.path.isdir(self.out_eventdir().path):        
            self.setup_output_dir(self.out_eventdir().path)

        # collect tweet files
        end_date_year = self.end_date[:4]
        end_date_month = self.end_date[4:6]
        end_date_day = self.end_date[6:]
        last_date = datetime.date(int(end_date_year),int(end_date_month),int(end_date_day))
        first_date = last_date - datetime.timedelta(days = self.window_size)
        last_tweetfile = self.in_tweetdir().path + '/' + end_date_year + end_date_month + '/' + end_date_year + end_date_month + end_date_day + '-23.out.dateref.cityref.entity.json'
        days_tweetfiles = helpers.return_tweetfiles_window(last_tweetfile,self.window_size)
        tweetfiles = []
        for day in days_tweetfiles:
            tweetfiles.extend([ filename for filename in glob.glob(self.in_tweetdir().path + '/' + day + '*') ])

        # extract events
        er = event_ranker.EventRanker()
        # read in tweets
        print('Reading in tweets')
        for tweetfile in tweetfiles:
            print(tweetfile)
            date = helpers.return_date_entitytweetfile(tweetfile)
            with open(tweetfile, 'r', encoding = 'utf-8') as file_in:
                tweetdicts = json.loads(file_in.read())
            # format as tweet objects
            for td in tweetdicts:
                if not td['refdates'] == {} and td['entities'] == {}:
                    tweetobj = tweet.Tweet()
                    tweetobj.import_tweetdict(td)
                    er.add_tweet(tweetobj)
                er.tweet_counts[date] += 1

        # extract events
        print('Performing event extraction')
        ranked_events = er.extract_events(first_date,self.window_size,self.minimum_event_mentions,self.cut_off)

        print('Done. Extracted',len(ranked_events),'events')

        # write to file
        outevents = [event.return_dict() for event in ranked_events]
        with open(self.out_events().path,'w',encoding='utf-8') as file_out:
            json.dump(outevents,file_out)
        
@registercomponent
class ExtractEvents(StandardWorkflowComponent):

    end_date = Parameter()
    window_size = IntParameter(default=30)
    minimum_event_mentions = IntParameter(default=5)
    cut_off = IntParameter(default=2500)

    def accepts(self):
        return InputFormat(self, format_id='tweetdir', extension='.tweets')

    def autosetup(self):
        return ExtractEventsTask

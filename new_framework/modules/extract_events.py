

from luiginlp.engine import Task, StandardWorkflowComponent, InputFormat, InputComponent, registercomponent, InputSlot, Parameter, IntParameter, BoolParameter

import json
import glob
import os
import datetime 

from functions import event_ranker, helpers
from classes import event, tweet


################################################################################
###Event extraction by slider
################################################################################

@registercomponent
class ExtractEventsSlider(StandardWorkflowComponent):

    start_date = Parameter()
    end_date = Parameter()
    window_size = IntParameter(default=30)
    slider = IntParameter(default=1)
    minimum_event_mentions = IntParameter(default=5)
    cut_off = IntParameter(default=2500)

    def accepts(self):
        return InputFormat(self, format_id='tweetdir', extension='.tweets')

    def autosetup(self):
        return ExtractEventsSliderTask


class ExtractEventsSliderTask(Task):

    in_tweetdir = InputSlot()

    start_date = Parameter()
    end_date = Parameter()
    window_size = IntParameter()
    slider = IntParameter()
    minimum_event_mentions = IntParameter()
    cut_off = IntParameter()

    def out_eventdir(self):
        return self.outputfrominput(inputformat='tweetdir', stripextension='.tweets', addextension='.' + start_date + '_' + end_date + '.events')

    def run(self):

        # create directory      
        self.setup_output_dir(self.out_eventdir().path)

        # set dates
        end_date_year = self.end_date[:4]
        end_date_month = self.end_date[4:6]
        end_date_day = self.end_date[6:]
        last_date = datetime.date(int(end_date_year),int(end_date_month),int(end_date_day))
        start_date_year = self.start_date[:4]
        start_date_month = self.start_date[4:6]
        start_date_day = self.start_date[6:]
        first_date = datetime.date(int(start_date_year),int(start_date_month),int(start_date_day))
        
        # perform event extraction on first tweet window
        print('Reading in first window of tweets')
        er = event_ranker.EventRanker()
        cursor_date = first_date
        while cursor_date < firstdate+datetime.timedelta(days=self.window_size):
            print(cursor_date)
            tweetfiles = helpers.return_timeobj_date(cursor_date)
            for tweetfile in tweetfiles:
                # read in tweets
                with open(self.in_tweetdir().path + '/' + tweetfile, 'r', encoding = 'utf-8') as file_in:
                    tweetdicts = json.loads(file_in.read())
                # add tweets to event ranker
                for td in tweetdicts:
                    if not (td['refdates'] == {} and td['entities'] == {}):
                        tweetobj = tweet.Tweet()
                        tweetobj.import_tweetdict(td)
                        er.add_tweet(tweetobj)
                    er.tweet_counts[cursor_date] += 1               
            cursor_date += datetime.timedelta(days=1)
        print('Performing event extraction')
        ranked_events = er.extract_events(first_date,self.window_size,self.minimum_event_mentions,self.cut_off)
        print('Done. Extracted',len(ranked_events),'events')        
        # write to file
        outevents = [event.return_dict() for event in ranked_events]
        with open(self.out_eventdir().path + '/' + str(cursor_date).replace('-','') + '.events','w',encoding='utf-8') as file_out:
            json.dump(outevents,file_out)


        # slide window forward and perform event extraction until last date 
        print('Starting slider')
        window_tail = first_date
        window_head = cursor_date
        while window_head <= last_date:
            print('new window; tail:',window_tail,'head:',window_head)
            while window_head < window_head+datetime.timedelta(days=self.slider):
                window_tail = window_tail + datetime.timedelta(days=1)
                window_head = window_head + datetime.timedelta(days=1)
                # remove tweets of tail
                er.discard_tweets(window_tail)
                tweetfiles = helpers.return_timeobj_date(window_head)
                for tweetfile in tweetfiles:
                    # read in tweets
                    with open(self.in_tweetdir().path + '/' + tweetfile, 'r', encoding = 'utf-8') as file_in:
                        tweetdicts = json.loads(file_in.read())
                    # add tweets to event ranker
                    for td in tweetdicts:
                        if not (td['refdates'] == {} and td['entities'] == {}):
                            tweetobj = tweet.Tweet()
                            tweetobj.import_tweetdict(td)
                            er.add_tweet(tweetobj)
                        er.tweet_counts[cursor_date] += 1               
            print('Performing event extraction')
            ranked_events = er.extract_events(window_tail,self.window_size,self.minimum_event_mentions,self.cut_off)
            print('Done. Extracted',len(ranked_events),'events')                    
            # write to file
            outevents = [event.return_dict() for event in ranked_events]
            with open(self.out_eventdir().path + '/' + str(window_head).replace('-','') + '.events','w',encoding='utf-8') as file_out:
                json.dump(outevents,file_out)


################################################################################
###Event extraction in single run
################################################################################

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
        first_date = last_date - datetime.timedelta(days = self.window_size-1)
        last_tweetfile = self.in_tweetdir().path + '/' + end_date_year + end_date_month + '/' + end_date_year + end_date_month + end_date_day + '-23.out.dateref.cityref.entity.json'
        days_tweetfiles = helpers.return_tweetfiles_window(last_tweetfile,self.window_size-1)
        tweetfiles = []
        for day in days_tweetfiles:
            tweetfiles.extend([ filename for filename in glob.glob(self.in_tweetdir().path + '/' + day + '*') ])

        # extract events
        er = event_ranker.EventRanker()
        # read in tweets
        print('Reading in tweets')
        for tweetfile in tweetfiles:
            date = helpers.return_date_entitytweetfile(tweetfile)
            with open(tweetfile, 'r', encoding = 'utf-8') as file_in:
                tweetdicts = json.loads(file_in.read())
            # format as tweet objects
            for td in tweetdicts:
                if not (td['refdates'] == {} and td['entities'] == {}):
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
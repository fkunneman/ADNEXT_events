
import sys
import os
import glob
from pynlpl.formats import folia
import luiginlp
from luiginlp.engine import Task, StandardWorkflowComponent, InputFormat, InputComponent, registercomponent, InputSlot, Parameter
from luiginlp.modules.ucto import Ucto_dir
import simple_featurizer

import gzip
import io
import json

from functions import tweetfilter
import json_tweets_parser
from classes import tweet

class FilterTweetsTask(Task):

    in_tweets = InputSlot() #input slot for a gzipped tweet file

    def out_filtered(self):
        return self.outputfrominput(inputformat='tweets', stripextension='.xml', addextension='.filtered.json')

    def run(self):
        # read in gzipped tweet file
        tweets = []
        for line in io.TextIOWrapper(io.BufferedReader(gzip.open(self.in_tweets().path)), encoding='utf-8', errors='ignore'):
            tweets.append(t.append(json.loads(line.strip())))
        print(self.in_tweets().path,'contains',len(tweets),'before filtering')
        tf = tweetfilter.Tweetfilter(tweets)
        tf.discard_retweets()
        tf.discard_nondutch()
        filtered_tweets = ft.return_tweets()
        print('after filtering:',len(filtered_tweets))
        # write filtered tweets
        outtweets = []
        for filtered_tweet in filtered_tweets:
            tweetobj = tweet.Tweet()
            tweetobj.import_twiqsdict(filtered_tweet)
            outtweets.append(tweetobj.return_dict())
        # write to file
        with open(self.out_filtered().path,'w',encoding='utf-8') as outfile:
            json.dump(outtweets,outfile)

@registercomponent
class FilterTweets(StandardWorkflowComponent):

    def autosetup(self):
        return FilterTweetsTask

    def accepts(self):
        return InputFormat(self, format_id='tweets', extension='.gz'),

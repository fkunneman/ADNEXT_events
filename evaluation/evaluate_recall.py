
import sys
import datetime

import time_functions

fgs = sys.argv[1] # gold standard
fee = sys.argv[2] # extracted events
of = sys.argv[3] # outfile
tfs = sys.argv[4:] # stream of tweets

# 1: read in gold standard --> sorted event term - time
print('Reading gold standard file')
gold_standard = []
with open(fgs, encoding = 'utf-8') as gs:
    for line in gs.readlines():
        event_date = line.strip().split('\t')
        event_date[1] = time_functions.return_datetime(event_date[1])
        gold_standard.append(event_date)
gold_standard = sorted(gold_standard, key = lambda k : k[1])

# 2: read in extracted events --> sorted event terms, time
print('Reading extracted events file')
extracted_events = []
with open(fee, encoding = 'utf-8') as ee:
    for line in ee.readlines():
        date_event = line.strip().split('\t')
        event_date = [date_event[1].split(', '), time_functions.return_datetime(date_event[0], setting = 'vs')]
        extracted_events.append(event_date)
extracted_events = sorted(extracted_events, key = lambda k : k[1])

# 3: read in tweets
print('Reading tweet files')
tweets = []
for tweetfile in tfs:
    with open(tweetfile, encoding = 'utf-8') as tf:
        for tweet in tf.readlines()[1:]:
            columns = tweet.strip().split('\t')
            tweets.append(columns[-1])








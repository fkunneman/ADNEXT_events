
import sys
import datetime

import time_functions

fgs = sys.argv[1] # gold standard
fee = sys.argv[2] # extracted events
of = sys.argv[3] # outfile
tfs = sys.argv[4:] # stream of tweets

# 1: read in gold standard --> sorted event term - time
print('Reading gold standard file')
gold_standard_events = []
gold_standard_events_hashtag = []
gold_standard = []
with open(fgs, encoding = 'utf-8') as gs:
    for line in gs.readlines():
        event_date = line.strip().split('\t')
        event_date[1] = time_functions.return_datetime(event_date[1])
        if event_date[0] not in gold_standard_events:
            gold_standard.append(event_date)
            gold_standard_events.append(event_date[0])
            event_hashtag = '#' + ''.join(event_date[0].split())
            gold_standard_events_hashtag.append(event_hashtag)
gold_standard = sorted(gold_standard, key = lambda k : k[1])
# for event in gold_standard:
#     sys.stdout.buffer.write(event[0].encode('utf8'))
#     print(' ', event[1])
    
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

# match extracted events with gold standard
matches = []
non_matches = []
for event_date in extracted_events:
    event_terms = event_date[0].split(', ')
    match = False
    for event_term in event_terms:
        if event_term[0] == '#':
            if event_term in gold_standard_events_hashtag:
                matches.append(event_date[0])
                match = True
                break
        else:
            for part in event_term.split(' '):
                if part in gold_standard_events:
                    matches.append(event_date[0])
                    match = True
                    break
            if match:
                break
    if not match:
        non_matches.append(event_date[0])

with open(of[:-4] + '_matches.txt') as outfile:
    outfile.write('\n'.join(matches))

with open(of[:-4] + '_non-matches.txt') as outfile:
    outfile.write('\n'.join(non_matches))

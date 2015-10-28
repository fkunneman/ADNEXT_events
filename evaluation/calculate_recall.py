
import sys
from collections import defaultdict

import time_functions

gsf = sys.argv[1]
eem = sys.argv[2]
tm = sys.argv[3]
out = sys.argv[4]
eredivisie = int(sys.argv[5])

# 1: collect num gold standard
with open(gsf, encoding = 'utf-8') as gsfo:
    gold_standard = gsfo.read().split('\n')    
num_gold_standard = len(gold_standard)

# 2: collect num event extraction
with open(eem, encoding = 'utf-8') as eemo:
    extracted_events = eemo.read().split('\n')

# 3: collect num tweet matching
with open(tm, encoding = 'utf-8') as tmo:
    tweet_all = tmo.read().split('\n')
tweet_matches = []
for x in tweet_all:
    if len(x.split('\t')) >= 3:
        if x.split('\t')[2] != '0':
            tweet_matches.append(x)

# 4: make calculations and output results
month_gold_standard = defaultdict(int)
event_month = {}
for event in gold_standard:
    parts = event.split('\t')
    if len(parts) < 2:
        break
    else:
        date = time_functions.return_datetime(parts[1])
        event_month[parts[0].lower()] = date.month
        month_gold_standard[date.month] += 1

month_extracted_events = defaultdict(int)
for ee in extracted_events:
    parts = ee.split('\t')
    if len(parts) > 1:
#        print('extract match', event_month[parts[2]], parts[2])
        month_extracted_events[event_month[parts[2]]] += 1

month_tweet_matches = defaultdict(int)
month_tweet_matches_threshold = defaultdict(int)
for twma in tweet_matches:
    parts = twma.split('\t')
    num = int(parts[2])
    if eredivisie:
        date = time_functions.return_datetime(parts[1], setting = 'vs')
        if num >= 0:
            month_tweet_matches[date.month] += 1
            if num >= 5:
                month_tweet_matches_threshold[date.month] += 1
    else:
        if num >= 0:
            month = event_month[parts[0].lower()]
#            print('tweet match', month, parts[0])
            month_tweet_matches[month] += 1
            if num >= 5:
                month_tweet_matches_threshold[month] += 1

scores = [['period', '# gold standard events', '# tweets mentioning gold standard', '\% tweets mentioning gs', '# > 4 tweets mentioning gs', 
    '\% tweets > 4 mentioning gs', '# extracted events', '\% extracted events of gold standard', '\% extracted events of tweets mentioning gs',
    '\% extracted events of tweets > 4 mentioning gs']]

gold_standard = 0
extracted_events = 0
tweet_matches = 0
tweet_matches_threshold = 0

#for month in [8, 9, 10, 11, 12]:
for month in [8, 9]:
    try:
#        mgs = month_gold_standard[month]
        gold_standard += month_gold_standard[month]
        extracted_events += month_extracted_events[month]
        tweet_matches += month_tweet_matches[month]
        tweet_matches_threshold += month_tweet_matches_threshold[month]
    except:
        results = [0,0,0,0,0,0,0,0,0,0]
    #scores.append([str(x) for x in results])

matched = extracted_events / gold_standard
matched_tweets = tweet_matches / gold_standard
matched_tweets_threshold = tweet_matches_threshold / gold_standard
percentage_tweets = extracted_events / tweet_matches
percentage_tweets_threshold = extracted_events / tweet_matches_threshold
results = ['August and September', gold_standard, tweet_matches, matched_tweets, tweet_matches_threshold, matched_tweets_threshold, extracted_events, matched, percentage_tweets, percentage_tweets_threshold]  

#matched = len(extracted_events) / num_gold_standard
#matched_tweets = len(tweet_matches) / num_gold_standard
#matched_tweets_threshold = [x for x in tweet_matches if int(x.split('\t')[2]) >= 5]
#matched_tweets_threshold_score = len(matched_tweets_threshold) / num_gold_standard
#percentage_tweets = len(extracted_events) / len(tweet_matches)
#percentage_tweets_threshold = len(extracted_events) / len(matched_tweets_threshold)
#results_total = ['total', num_gold_standard, len(tweet_matches), matched_tweets, len(matched_tweets_threshold),
#    matched_tweets_threshold_score, len(extracted_events), matched, matched_tweets, 
#    percentage_tweets, percentage_tweets_threshold]
scores.append([str(x) for x in results])

with open(out, 'w', encoding = 'utf-8') as outfile:
    outfile.write('\n'.join(['\t'.join(x) for x in scores]))

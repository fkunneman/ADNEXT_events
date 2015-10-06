
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
    date = time_functions.return_datetime(parts[1])
    event_month[parts[0].lower()] = date.month
    month_gold_standard[date.month] += 1

month_extracted_events = defaultdict(int)
for ee in extracted_events:
    parts = ee.split('\t')
    if len(parts) > 1:
        month_extracted_events[event_month[parts[2]]] += 1

month_tweet_matches = defaultdict(int)
month_tweet_matches_threshold = defaultdict(int)
for twma in tweet_matches:
    parts = twma.split('\t')
    num = int(parts[2])
    if eredivisie:
        date = time_functions.return_datetime(parts[1])
        if num >= 0:
            month_tweet_matches[date.month] += 1
            if num >= 5:
                month_tweet_matches_threshold[date.month] += 1
    else:
        if num >= 0:
            month = event_month[parts[0]]
            month_tweet_matches[month] += 1
            if num >= 5:
                month_tweet_matches_threshold[month] += 1

scores = ['period', '# gold standard events', '# tweets mentioning gold standard', '\% tweets mentioning gs', '# > 4 tweets mentioning gs', 
    '\% tweets > 4 mentioning gs', '# extracted events', '\% extracted events of gold standard', '\% extracted events of tweets mentioning gs',
    '\% extracted events of tweets > 4 mentioning gs']

for month in [8, 9, 10, 11, 12]:
    mgs = month_gold_standard[month]
    matched = month_extracted_events[month] / mgs
    matched_tweets = month_tweet_matches[month] / mgs
    matched_tweets_threshold = month_tweet_matches_threshold / mgs
    percentage_tweets = month_extracted_events[month] / month_tweet_matches[month]
    percentage_tweets_threshold = month_extracted_events[month] / month_tweet_matches_threshold[month]
    results = [month, mgs, month_tweet_matches[month], matched_tweets, month_tweet_matches_threshold[month], matched_tweets_threshold,
    month_extracted_events[month], matched, percentage_tweets, percentage_tweets_threshold]  
    scores.append([str(x) for x in results])

matched = len(extracted_events) / num_gold_standard
matched_tweets = len(tweet_matches) / num_gold_standard
matched_tweets_threshold = [x for x in tweet_matches if int(x.split('\t')[2]) >= 5]
matched_tweets_threshold_score = len(matched_tweets_threshold) / num_gold_standard
percentage_tweets = len(extracted_events) / len(tweet_matches)
percentage_tweets_threshold = len(extracted_events) / len(matched_tweets_threshold)
results_total = ['total', num_gold_standard, len(tweet_matches), matched_tweets, len(matched_tweets_threshold),
    matched_tweets_threshold_score, len(extracted_events), matched, matched_tweets, 
    percentage_tweets, percentage_tweets_threshold]
scores.append([str(x) for x in results_total])

with open(out, 'w', encoding = 'utf-8') as outfile:
    outfile.write('\n'.join(['\t'.join(x) for x in scores]))

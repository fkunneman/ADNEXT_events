
import sys
from collections import defaultdict

import query_defs

keyterms = sys.argv[1]
outdir = sys.argv[2]
id_included = sys.argv[3]
stats_tweets = sys.argv[4:]

#read in events
events = []
event_terms = []
with open(keyterms, 'r', encoding = 'utf-8') as kts:
    for line in kts.read().split('\n'):
        if line != '':
            tokens = line.split('\t')
            eid = tokens[0].strip()
            keyterms = tokens[1].strip().split(',')
            date_begin = tokens[2].strip()
            date_end = tokens[3].strip()
            events.append([eid, keyterms, date_begin, date_end])
            event_terms.extend(keyterms)
event_terms_set = set(event_terms)





half = int(len(stats_tweets) / 2)
stats = stats_tweets[:half]
tweets = stats_tweets[half:]
date_statfile = {}
date_tweetfile = {}
for stat in stats:
    date = int(stat.split('/')[-1][:8])
    date_statfile[date] = stat
for tweet in tweets:
    date = int(tweet.split('/')[-1][:8])
    date_tweetfile[date] = tweet

term_date_tweets = defaultdict(lambda : {})
dates = sorted([int(x.split('/')[-1][:8]) for x in stats])
for date in dates:
    print(date)
    stat = date_statfile[date]
    with open(stat, 'r', encoding = 'utf-8') as stat_open:
        statlines = stat_open.readlines()
    tweet = date_tweetfile[date]
    with open(tweet, 'r', encoding = 'utf-8') as tweet_open:
        tweetlines = tweet_open.read().split('\n')
    tweetlines_cleaned = []

    for line in statlines:
        tokens = line.strip().split('\t')
        term = tokens[0]
        if term in event_terms:
            begin = int(tokens[2])
            end = int(tokens[3])
            if not (begin == 0 and end == 0):
                tweets = tweetlines_cleaned[begin:end]
                term_date_tweets[term][date] = tweets

for event in events:
    print((','.join(event[1]) + ' ' + event[2] + ' ' + event[3]).encode('utf-8'))
    eid = event[0]
    event_terms = event[1]
    date_begin = int(event[2])
    date_end = int(event[3])
    if date_begin in dates and date_end in dates:
        outfile = outdir + eid + '.txt'
        with open(outfile, 'w', encoding = 'utf-8') as out:
            date_begin_index = dates.index(date_begin)
            date_end_index = dates.index(date_end)
            event_term_tweets = defaultdict(list)
            for date in dates[date_begin_index:date_end_index+1]:
                for event_term in event_terms:
                    if date in term_date_tweets[event_term].keys():
                        event_term_tweets[event_term].extend(term_date_tweets[event_term][date])
        # write to file
            for event_term in event_terms:
                for tweet in event_term_tweets[event_term]:
                    out.write(event_term + '-----' + tweet + '\n')
            if len(event_terms) > 1: # write combis to file
                combis = query_defs.return_combis(event_terms)
                combi_tweets = query_defs.extract_andpatterns(event_term_tweets, combis)
                for combi in combi_tweets.keys():
                    for tweet in combi_tweets[combi]:
                        out.write(combi + '-----' + tweet + '\n')

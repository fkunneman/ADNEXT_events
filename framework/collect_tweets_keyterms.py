
import sys
from collections import defaultdict

import query_defs

keyterms = sys.argv[1]
outdir = sys.argv[2]
stats_tweets = sys.argv[3:]

events = []
event_terms = []
with open(keyterms, 'r', encoding = 'utf-8') as kts:
    for line in kts.read().split('\n'):
        if line != '':
            tokens = line.split('\t')
            keyterms = tokens[1].split(',')
            date_begin = tokens[2]
            date_end = tokens[3]
            events.append([keyterms, date_begin, date_end])
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
        tweetlines = tweet_open.readlines()
    for line in statlines:
        tokens = line.strip().split('\t')
        term = tokens[0]
        if len(list(set(term) & event_terms_set)) > 0:
            begin = int(tokens[2])
            end = int(tokens[3])
            tweets = tweetlines[begin:end]
            term_date_tweets[term][date] = tweets

for event in events:
    print(event)
    event_terms = event[0]
    date_begin = event[1]
    date_end = event[2]
    if date_begin in dates and date_end in dates:
        date_begin_index = dates.index(date_begin)
        date_end_index = dates.index(date_end)
        event_term_tweets = {}
        for date in dates[date_begin_index:date_end_index+1]:
            for event_term in event_terms:
                event_term_tweets[event_term].extend(term_date_tweets[event_term][date])
        # write to file
        for event_term in event_terms:
            outfile = outdir + event_term + '_' + date_begin + '-' + date_end + '.txt'
            with open(outfile, 'w', encoding = 'utf-8') as out:
                out.write('\n'.join(event_term_tweets[event_term]))
        if len(event_terms) > 1: # write combis to file
            combis = query_defs.return_combis(event_terms)
            combi_tweets = query_defs.extract_andpatterns(event_term_tweets, combis)
            for combi in combi_tweets.keys():
                outfile = outdir + combi + '_' + date_begin + '-' + date_end + '.txt'
                with open(outfile, 'w', encoding = 'utf-8') as out:
                    out.write('\n'.join(combi_tweets[combi]))

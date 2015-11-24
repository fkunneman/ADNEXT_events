
import sys
import os
from collections import defaultdict
import datetime

import query_defs
import time_functions

keyterms = sys.argv[1]
datadir = sys.argv[2]
outdir = sys.argv[3]

sequences = defaultdict(lambda : defaultdict(list))

#read in events
events = []
with open(keyterms, 'r', encoding = 'utf-8') as kts:
    for i, line in enumerate(kts.readlines()):
        tokens = line.strip().split('---')
        eid = str(i)
        date = time_functions.return_datetime(tokens[0], setting = 'vs')
        date_begin = date - datetime.timedelta(days = 30)
        date_end = date + datetime.timedelta(days = 30)
        keyterms = tokens[1].split('_')
        events.append([eid, keyterms, date_begin, date_end, date])

files = os.listdir(datadir)
num_events = len(events)
for i, event in enumerate(events):
    print(i, 'of', num_events, ':', event[0])
    event_terms = event[1]
    combine = True if len(event_terms) > 1 else False
    date_cursor = event[2]
    date_end = event[3]
    date = event[4]
    term_sequence = defaultdict(list)
    outtweets = outdir + 'tweets_' + str(event[0]) + '.txt'
    firstseen = False
    end_date = date_cursor
    while date_cursor <= date_end:
        month = '0' + str(date_cursor.month) if len(str(date_cursor.month)) == 1 else str(date_cursor.month) 
        day = '0' + str(date_cursor.day) if len(str(date_cursor.day)) == 1 else str(date_cursor.day) 
        statfile = str(date_cursor.year) + month + day + '_eventstats.txt'
        if statfile in files:
            if not firstseen:
                firstseen = date_cursor
            end_date = date_cursor
            statfile = datadir + statfile
            with open(statfile, 'r', encoding = 'utf-8') as stat_in:
                stats = [line.split('\t') for line in stat_in.read().split('\n')]
                terms = [line[0] for line in stats]
            tweetsfile = datadir + str(date_cursor.year) + month + day + '_tweets_cleaned.txt'
            with open(tweetsfile, 'r', encoding = 'utf-8') as tweets_in:
                tweets = tweets_in.read().split('\n')
            with open(outtweets, 'a', encoding = 'utf-8') as tweets_out:
                term_tweets = defaultdict(list)
                for event_term in event_terms:
                    term_index = terms.index(event_term)
                    term_stats = stats[term_index]
                    term_sequence[event_term].append(int(term_stats[1]))
                    tweet_segment = tweets[int(term_stats[2]) : int(term_stats[3])]
                    for tweet in tweet_segment:
                        tweets_out.write(event_term + '-----' + tweet + '\n')
                    term_tweets[event_term].extend(tweet_segment)
                if combine: # write combis to file
                    combis = query_defs.return_combis(event_terms)
                    combi_tweets = query_defs.extract_and_patterns(term_tweets, combis)
                    for combi in combi_tweets.keys():
                        term_sequence[combi].append(len(combi_tweets[combi]))
                        for tweet in combi_tweets[combi]:
                            tweets_out.write(combi + '-----' + tweet + '\n')
        else:
            print('no existing file', statfile)
        date_cursor += datetime.timedelta(days = 1)
    outstats = outdir + 'sequence_' + str(event[0]) + '.txt'
    with open(outstats, 'w', encoding = 'utf-8') as stats_out:
        stats_out.write(', '.join(event_terms) + '\t' + str(date.date()) + '\t' + str(firstseen.date()) + '-' + str(end_date.date()) + '\n')
        for k in term_sequence.keys():
            stats_out.write(k + '\t' + ' '.join([str(x) for x in term_sequence[k]]) + '\n')

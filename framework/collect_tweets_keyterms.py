
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
    for i, x in enumerate(tweetlines):
        fields = x.split('\t')
        if len(fields) == 6:
            #tid = (x.split('\t')[0])
            tweetlines_cleaned.append(x)
        else:
#            print(x.encode('utf-8'))
            if len(fields) > 6:
                for f in fields[6:]:
                    fields[5] = fields[5] + ' ' + f
                tweetlines_cleaned.append('\t'.join(fields))
            else: # len(fields) < 6
                if not i == 0:
                    tweetlines_cleaned[-1] = tweetlines_cleaned[-1] + x
       #     print(i, x.encode('utf-8'), tweetlines[i-1].encode('utf-8'))
        #try:
#        except:
#            continue
#    for i, x in enumerate(tweetlines_cleaned):
#        print(i, x.encode('utf-8'))
    #print(len(tweetlines_cleaned))
    #quit()
    for line in statlines:
        tokens = line.strip().split('\t')
        term = tokens[0]
#        print(term.encode('utf-8'))        
#        print(len(list(set(term) & event_terms_set)))
        if term in event_terms:
#        print(' '.join(list(event_terms_set)).encode('utf-8'))
            begin = int(tokens[2])
            end = int(tokens[3])
            if not (begin == 0 and end == 0):
                tweets = tweetlines_cleaned[begin:end]
#                print(term.encode('utf-8'), begin, end, tweet, stat)
#                print(''.join(tweets).encode('utf-8'))
#                print(line.encode('utf-8'))
            #print(begin, end)
            #print(tweets)
            #print(term)
            #print(date)
#            print('yes')
                term_date_tweets[term][date] = tweets
#    quit()
#print(term_date_tweets)
#quit()

for event in events:
    print((','.join(event[1]) + ' ' + event[2] + ' ' + event[3]).encode('utf-8'))
    eid = event[0]
    event_terms = event[1]
    date_begin = int(event[2])
    date_end = int(event[3])
#    print(date_begin, date_end, dates)
    if date_begin in dates and date_end in dates:
        outfile = outdir + eid + '.txt'
        with open(outfile, 'w', encoding = 'utf-8') as out:
 #       print('yes')
            date_begin_index = dates.index(date_begin)
            date_end_index = dates.index(date_end)
            event_term_tweets = defaultdict(list)
            for date in dates[date_begin_index:date_end_index+1]:
                for event_term in event_terms:
#                print(event_term, date, term_date_tweets[event_term].keys())
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

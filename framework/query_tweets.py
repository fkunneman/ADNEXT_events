
import sys
from collections import defaultdict
import timeit

import coco

def query_event_terms(event_terms, tweets, tmpdir = False):
    if tmpdir:
        cc = coco.Coco(tmpdir)
        tweets_text = []
        for tweet in tweets:
            #columns = tweet.split('\t')
            tweets_text.append(tweet.lower())
        cc.set_lines(tweets_text)
        cc.simple_tokenize()
        cc.set_file()
        cc.model_ngramperline(event_terms)
        matches = cc.match(event_terms)
        return matches

event_eventterms = defaultdict(list)
eventterm_event = {}
eventfile = sys.argv[1]
tdir = sys.argv[2]
outfile = sys.argv[3]
tfs = sys.argv[4:]

events = [] 
with open(eventfile, 'r', encoding = 'utf-8') as ef:
    for line in ef.readlines():
        tokens = line.strip().split('\t')
        date = tokens[0]
        if date[5:7] == '08':
            day = int(date[8:])
            if day > 6 and day < 25:
                events.append([date, tokens[2].replace(', ', '|')])  
print('|'.join([x[1] for x in events]).encode('utf-8'))

for event in events:
    e = '|'.join(event)
    terms = event[1].split(',')
    for term in terms:
        event_eventterms[e].append(term)
        eventterm_event[term] = e

eventterm_tweets = defaultdict(list)
for tf in tfs:
    print(tf)
    d = tf[:8]
    tweets = []
    with open(tf, encoding = 'utf-8') as tf:
        for tweet in tf.readlines()[1:]:
            tweets.append(tweet.strip())

    m = query_event_terms(eventterm_event.keys(), tweets, tmpdir = tdir)

    for t in m.keys():
        if m[t][0] > 0:
            match_tweets = [tweets[i] for i in m[t][1]]
            eventterm_tweets[t].extend(match_tweets)

with open(outfile, 'w', encoding = 'utf-8') as out:
    for event in event_eventterms.keys():
        out.write('***' + event + '\n')
        for eventterm in event_eventterms[event]:
            out.write('---' + eventterm + '\n' + '----------'.join(eventterm_tweets[eventterm]) + '\n')


import sys
from collections import defaultdict
import timeit

import coco

def query_event_terms(event_terms, tweetfile, tmpdir = False):
    if tmpdir:
        cc = coco.Coco(tmpdir)
        tweets = []
        with open(tweetfile, encoding = 'utf-8') as tf:
            for tweet in tf.readlines()[1:]:
                columns = tweet.strip().split('\t')
                tweets.append(columns[-1])
        cc.set_lines(tweets)
        cc.simple_tokenize()
        cc.set_file()
        cc.model_ngramperline(event_terms)
        matches = cc.match(event_terms)
        return matches

event_eventterms = defaultdict(list)
eventterm_event = {}
eventfile = sys.argv[1]
tdir = sys.argv[2]
tf = sys.argv[3]

events = [] 
with open(eventfile, 'r', encoding = 'utf-8') as ef:
    for line in ef.readlines():
        tokens = line.strip().split('\t')
        date = tokens[0]
        if date[5:7] == '08':
            day = int(date[8:])
            if day > 6 and day < 25:
                events.append([date, tokens[2]])  

for event in events:
    e = '|'.join(event)
    terms = event[1].split(',')
    for term in terms:
        event_eventterms[e].append(term)
        eventterm_event[term] = e

tic = timeit.default_timer()
m = query_event_terms(eventterm_event.keys(), sys.argv[3], tmpdir = tdir)
toc = timeit.default_timer()
print('time in seconds', toc - tic)
#for t in m.keys():
#    info = t + '\t' + ' '.join([str(x) for x in m[t]])
#    print(info.encode('utf-8'))

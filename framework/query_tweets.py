
import sys
from collections import defaultdict
import timeit

import coco

def query_event_terms(event_terms, tweetfile, tmpdir = False):
    if tmpdir:
        cc = coco.Coco(tmpdir)
        with open(tweetfile, encoding = 'utf-8') as tf:
            for tweet in tf.readlines()[1:]:
                columns = tweet.strip().split('\t')
                tweets.append(columns[-1])
        cc.set_lines(tweets)
        cc.simple_tokenize()
        cc.set_file()
        cc.model_ngramperline(gold_standard_events)
        matches = cc.match(gold_standard_events)
        print(matches)

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
                events.append((date, tokens[2]))  

print(events)


# >>> tic=timeit.default_timer()
# >>> # Do Stuff
# >>> toc=timeit.default_timer()
# >>> toc - tic #elapsed time in seconds
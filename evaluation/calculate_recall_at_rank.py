
import sys
from collections import defaultdict

import time_functions

tm = sys.argv[1]
rank = sys.argv[2]
eem = sys.argv[3]
out = sys.argv[4]

# 1: collect num tweet matching
with open(tm, encoding = 'utf-8') as tmo:
    tweet_all = tmo.read().split('\n')
tweet_matches = 0
for x in tweet_all:
    parts = x.split('\t')
    if len(parts) >= 3:
        if int(parts[2]) >= 5:
            if parts[1][6] == '8' or parts[1][6] == '9':
                tweet_matches += 1
print(tweet_matches)

event_rank = defaultdict(lambda : {})
# 2: collect event rank
with open(rank, encoding = 'utf-8') as r:
    ranked_events = r.read().split('\n')
    for i, er in enumerate(ranked_events[:-1]):
        parts = er.strip().split('\t')
        event_rank[parts[2]][parts[0]] = i

# 3: collect recalled events
events = []
with open(eem, encoding = 'utf-8') as eemo:
    extracted_events = eemo.read().split('\n')
    for event in extracted_events:
        parts = event.split('\t')
        events.append((parts[0], parts[-1]))

event_score = [0] * len(ranked_events)
for event in events:
    if not event[0] == '':
        try:
            rank = event_rank[event[0]][event[1]]
        except:
            rank = event_rank[event[0]][list(event_rank[event[0]].keys())[0]]
        event_score[rank] = 1

recall_at = []
print(len(event_score))
with open(out, 'w') as wout:
    count = 0
    for i, score in enumerate(event_score):
        if score == 1:
            count += 1
        recall = round(count / (tweet_matches+1), 2)
        wout.write(str(i+1) + '\t' + str(recall) + '\n')

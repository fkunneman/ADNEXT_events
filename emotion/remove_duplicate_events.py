
import sys
import os
from collections import defaultdict

import docreader
import time_functions

event_tweet_dir = sys.argv[1]
outfile = sys.argv[2]

events = [x for x in os.listdir(event_tweet_dir) if x[-7:] == 'zin.txt']

date_events = defaultdict(list)
print('collecting events')
for event in events:
    event_id = event.split('_')[0]
    dr = docreader.Docreader()
    dr.parse_doc(event_tweet_dir + event)
    event_date = time_functions.return_datetime(dr.lines[0][1], setting = 'vs')
    event_terms = dr.lines[0][0].split(', ')
    event_tweets = [x[1] for x in dr.lines[1:]]
    date_events[event_date].append([event_id, event_terms, event_tweets])

print('finding duplicates')
keeps = []
for date in date_events.keys():
    final_events = []
    events = date_events[date]
    print(date.date(), 'begin', len(events), 'events')
    while len(events) > 0:
        working_event = events.pop(0)
        i = 0
        final = True
        while i < len(events):
            event = events[i]
            if set(working_event[1]) & set(event[1]): # event terms are overlapping
                overlap = list(set(working_event[2]) & set(event[2]))
                if len(overlap) / len(working_event[2]) > 0.5:
                    if len(working_event[2]) <= len(event[2]):
                        # remove matching event
                        del events[i]
                        continue
                    else:
                        # remove working event
                        final = False
                        break
                else:
                    i += 1
            else:
                i += 1
        if final:
            final_events.append(working_event)
    print(date.date(), 'end', len(final_events), 'events')
    keeps.extend([x[0] for x in final_events])

with open(outfile, 'w') as out:
    out.write('\n'.join(keeps))

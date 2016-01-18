
import sys
import os
from collections import defaultdict
import random

import docreader
import linewriter

partsdir = sys.argv[1]
textdir = sys.argv[2]

print('collecting events')
nums = ['0', '1', '2', '3', '4', '5', '6', '7' ,'8', '9']
textevents = [x for x in os.listdir(textdir) if x[7] in nums]
partsevents = [x for x in os.listdir(partsdir) if [0[]]] 

print('num text events is', len(textevents))
print('num parts events is', len(partsevents))

dr = docreader.Docreader()
seen = {}
event_indices = defaultdict(list)
total = 0

print('collecting unique tweets')
for event in textevents:
    eid = event[7:-4]
    elines = dr.parse_csv(textdir + event)
    for l in elines:
        seen[l[0]] = False

for event in textevents:
    eid = event[7:-4]
    elines = dr.parse_csv(textdir + event)
    for i, l in enumerate(elines):
        if not seen[l[0]]:
            seen[l[0]] = True
            total += 1
            event_indices[eid].append(i)

print('num unique tweets is', total)
print('num event keys is', len(event_indices.keys()))

print('dividing train - test')
tee = random.sample(partsevents, int(0.20 * len(partsevents)))
tre = list(set(partsevents) - set(tee))
print(len(tre), 'train events,', len(tee), 'test events,', len(tre) + len(tee), 'total events')

print('collecting lines')
etest = []
ptest = []
for event in tee:
    elines = dr.parse_csv(textdir + 'tweets_' + event + '.csv')
    plines = dr.parse_txt(partsdir + event + '.txt', delimiter = '\t', header = False)
    if len(elines) != len(plines):
        print(event, ': num parts (', len(plines), ') not equal to num tweets (', len(elines))
        quit()
    for i in event_indices[event]:
        etest.append(elines[i])
        ptest.append(plines[i])

etrain = []
ptrain = []
for event in tre:
    elines = dr.parse_csv(textdir + 'tweets_' + event + '.csv')
    plines = dr.parse_txt(partsdir + event + '.txt', delimiter = '\t', header = False)
    if len(elines) != len(plines):
        print(event, ': num parts (', len(plines), ') not equal to num tweets (', len(elines))
        quit()
    for i in event_indices[event]:
        etrain.append(elines[i])
        ptrain.append(plines[i])

print('writing to files')
with open(partsdir + 'parts_train_complete.txt', 'w', encoding = 'utf-8') as ptr_out:
    ptr_out.write('\n'.join(ptrain))
with open(partsdir + 'parts_test_complete.txt', 'w', encoding = 'utf-8') as ptt_out:
    ptt_out.write('\n'.join(ptest))

lw = linewriter.Linewriter(etest)
lw.write_csv(textdir + 'tweets_test_complete.csv')
lw = linewriter.Linewriter(etrain)
lw.write_csv(textdir + 'tweets_train_complete.csv')

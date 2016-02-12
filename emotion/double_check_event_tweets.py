
import sys
import re

classifications_dir = sys.argv[1]
unique_events_file = sys.argv[2]
report_file = sys.argv[3]

with open(unique_events_file) as ue:
    unique_events = ue.read().split('\n')

blacklist = []
for event in unique_events:
    print(event)
    misplaced = []
    with open(classifications_dir + event + '_zin.txt', 'r', encoding = 'utf-8') as eo:
        lines = eo.readlines()
    event_terms = lines[0].split('\t')[0].split(', ')
    for i, tweet in enumerate(lines[1:]):
        match = False
        for et in event_terms:
            if re.search(et, tweet):
                match = True
                break
        if not match:
            misplaced.append(i)
    if len(misplaced) > 0:
        percent = len(misplaced) / len(lines[1:])
        blacklist.append([event, percent])

with open(report_file, 'w') as ro:
    ro.write('\n'.join([' '.join(x) for x in blacklist]) + '\n')
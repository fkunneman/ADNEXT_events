
import os
import sys

import docreader

eventdir = sys.argv[1]
outfile_overlaps = sys.argv[2]
outfile_no_overlap = sys.argv[3]

eventfiles = os.listdir(eventdir)

print('Reading in eventfiles')
event_ids = []
efs = len(eventfiles)
for i, eventfile in enumerate(eventfiles):
    print(eventfile, i, 'of', efs)
    try:
        dr = docreader.Docreader()
        dr.parse_doc(eventdir + eventfile)
        ids = [l[0] for l in dr.lines]
        event_ids.append((eventfile, ids))
    except:
        continue

num_events = len(event_ids)
overlaps = []
event_overlap = {}
for event in eventfiles:
    event_overlap[event] = False
for i, event in enumerate(event_ids[:-1]):
    j = i + 1
    while j < num_events:
        event2 = event_ids[j]
        print(i, '+', j, 'of', num_events)
        if set(event[1]) & set(event2[1]):
            event_overlap[event[0]] = True
            event_overlap[event2[0]] = True
            num_overlap1 = len(list(set(event[1]) - set(event2[1])))
            percent_overlap1 = num_overlap1 / len(event[1])
            num_overlap2 = len(list(set(event2[1]) - set(event[1])))
            percent_overlap2 = num_overlap2 / len(event2[1])
            overlaps.append([event[0], event2[0], num_overlap1, percent_overlap1, num_overlap2, percent_overlap2])
        j += 1

with open(outfile_overlaps, 'w') as w_out:
    for ov in overlaps:
        w_out.write(' '.join(ov) + '\n')

with open(outfile_no_overlap, 'w') as w_out:
    for event in eventfiles:   
        if not event_overlap[event]:
            w_out.write(event + '\n')

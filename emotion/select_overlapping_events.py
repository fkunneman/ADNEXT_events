
import os
import sys

import docreader

eventdir = sys.argv[1]
outfile = sys.argv[2]

eventfiles = os.listdir(eventdir)

event_ids = []
for eventfile in eventfiles:
    dr = docreader.Docreader()
    dr.parse_doc(eventdir + eventfile)
    ids = [l[0] for l in dr.lines]
    event_ids.append((eventfile, ids))

num_events = len(event_ids)
overlaps = []
for i, event in enumerate(event_ids[-1]):
    j = i + 1
    while j < num_events:
        event2 = event_ids[j]
        print(i, '+', j, 'of', num_events)
        if set(event[1]) & set(event2[1]): 
            num_overlap1 = len(list(set(event[1]) - set(event2[1])))
            percent_overlap1 = num_overlap1 / len(event[1])
            num_overlap2 = len(list(set(event2[1]) - set(event[1])))
            percent_overlap2 = num_overlap2 / len(event2[1])
            overlaps.append([num_overlap1, percent_overlap1, num_overlap2, percent_overlap2])

with open(outfile, 'w') as w_out:
    for ov in overlaps:
        w_out.write(' '.join(ov) + '\n')
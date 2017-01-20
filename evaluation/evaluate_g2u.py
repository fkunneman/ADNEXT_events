
import sys
from collections import defaultdict
import annotation_calcs

g2u = sys.argv[1]
g2u_performance = sys.argv[2]
g2 = sys.argv[3]
plot = sys.argv[4]
out = sys.argv[5]

events_g2u = []
with open(g2u, 'r', encoding = 'utf-8') as go:
    for line in go.readlines():
        tokens = line.strip().split('\t')
        events_g2u.append((tokens[0], tokens[2].split(', ')))

events_g2 = []
date_event = defaultdict(list)
with open(g2, 'r', encoding = 'utf-8') as go:
    for line in go.readlines():
        tokens = line.strip().split('\t')
        event = (tokens[0], float(tokens[1]), tokens[2].split(', '))
        date_event[tokens[0]].append(event)

with open(g2u_performance) as gp:
    annotations = [x.split('\t') for x in gp.read().split('\n')]
    annotations = [[int(x) for x in line] for line in annotations[:-1]]

#link events
linked_events = []
for i, event in enumerate(events_g2u):
    date = event[0]
    link = False
    for g2_event in date_event[date]:
        if set(g2_event[2]) & set(event[1]):
            linked_events.append((g2_event, annotations[i]))
            link = True
            break
    if not link:
        print('no matching event found', event, annotations[i])

        #quit()
        continue

#print('before', linked_events)
ranked_linked_events = sorted(linked_events, key = lambda k : k[0][1], reverse = True)
#print('after', ranked_linked_events)


annotations_reranked = [x[1] for x in ranked_linked_events]
precisions2 = annotation_calcs.calculate_precision(annotations, lax = True, plot = plot)
precisions = annotation_calcs.calculate_precision(annotations_reranked, lax = True, plot = plot)

p = list(zip(precisions, precisions2))
#print(p)
#print(precisions)
with open(out, 'w', encoding = 'utf-8') as o:
    o.write('\n'.join([' '.join([str(y) for y in x]) for x in p]))

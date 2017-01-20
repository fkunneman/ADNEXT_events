
import sys
import re
from collections import defaultdict

import calculations

eventfile = sys.argv[1]
cities = sys.argv[2]
outfile = sys.argv[3]

# 1: rangschik op score
print('reading events')
score_event = []
with open(eventfile, encoding = 'utf-8') as er:
    for line in er.readlines():
        tokens = line.strip().split('\t')
        date = tokens[0]
        score = float(tokens[1])
        keyterms = tokens[2].split(',')
        tweets = tokens[4].split('-----')
        score_event.append([score, [date, keyterms, tweets]])

score_event_sorted = sorted(score_event, key = lambda k : k[0], reverse = True)
events = [x[1] for x in score_event_sorted][:5000]

# 2: extraheer plaatsnamen
print('extracting cities')
cityfile = open(cities,"r",encoding='iso-8859-1')
cts = [x.strip().lower() for x in cityfile.read().split("\n")]
cityfile.close()
li = sorted(cts, key=len, reverse=True)
li = [tx.replace('.','\.').replace('*','\*') for tx in li] # not to match anything with . (dot) or *
citylist = re.compile('\\b' + '\\b|\\b'.join(li) + '\\b')
events_out = open(outfile, 'w', encoding='utf-8')
for event in events:
    places = defaultdict(int)
    total = 0
    tweets = event[2]
    for tweet in tweets:
        cities = calculations.return_cities([tweet], citylist)[1]
        for city in cities:
#            print(' '.join(city).encode('utf-8'))
            if not (city == "nederland" or city == "--"):
                places[city] += 1
                total += 1
    if len(places.keys()) > 0:
        places_out = []
        sorted_places = sorted(places, key=places.get, reverse=True)
        for place in sorted_places:
            tp_score = places[place]/total
            places_out.append([place, str(tp_score)])
    else:
        places_out = [['---', '---']]
    events_out.write('\t'.join([event[0], ', '.join(event[1]), '|'.join(' / '.join(x) for x in places_out), '-----'.join(event[2])]) + '\n')


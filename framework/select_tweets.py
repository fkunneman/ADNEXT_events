
import sys
import datetime
from collections import defaultdict
import numpy

import time_functions


tweetfile = sys.argv[1]
outfile = sys.argv[2]

def dict2list(d):
    date = datetime.date(2014, 8, 1)
    keys = d.keys()
    l = []
    while date < datetime.date(2014, 9, 1):
        if date in keys:
            l.append(d[date])
        else:
            l.append(0)
    return l

def score_burstiness(sequence, position):
    mean = numpy.mean(sequence)
    burstiness = sequence[position] / mean
    return burstiness

event_bursti_scores = defaultdict(lambda : {})
with open(tweetfile, 'r', encoding = 'utf-8') as infile:
    for line in infile.readlines():
        if line[:4] == '***':
            # start new event
            event_date = time_functions.return_datetime(line[3:13], setting = 'vs')
            event = line.strip()
            event_terms = event[13:].split(', ')
            event_term_ids = {}
            combi_timelist = {}
            id_date = {}
        elif line[:4] == '---':
            # start new event term
            event_term = line.strip()[3:]
        else:
            # collect tweets by date
            tweets = line.strip().split('---------')
            timedict = defaultdict(int)
            ids = []
            for tweet in tweets:
                tokens = tweet.split('\t')
                date = time_functions.return_datetime(tokens[2], setting = 'vs')
                timedict[date] += 1
                ids.append(tokens[1])
                id_date[tokens[1]] = date
            timelist = dict2list(timedict)
            combi_timelist[event_term] = timelist
            event_term_ids[event_term] = ids
            if event_term == event_terms[-1]:
                # append event to list
                if len(event_terms) > 1: # there exist combis
                    combis = [event_terms]
                    if len(event_terms) > 2:
                        for i in range(2, len(event_terms)):
                            for combi in (list(itertools.combinations(event_terms, i))):
                                combis.append(list(combi))
                    print(combis)
                    for combi in combis: # combine
                        overlap = set(event_term_ids[combi[0]]) & set(event_term_ids[combi[1]])
                        if len(combi) > 2:
                            for et in combi[2:]:
                                overlap = overlap & set(event_term_ids[et])
                        overlap_timedict = defaultdict(int)
                        for tid in list(overlap):
                            overlap_timedict[id_date[tid]] += 1
                        timelist = dict2list(timedict)
                        combi_timelist[', '.join(list(combi))] = timelist
                # calculate burstiness
                position = event_date - datetime.date(2014, 8, 1)
                print(event_date, position)
                for combi in combi_timelist.keys():
                    burstiscore = score_burstiness(combi_timelist[combi], position)
                    event_bursti_scores[event][combi] = str(burstiscore)
            
with open(outfile, 'w', encoding = 'utf-8') as out:
    for event in event_bursti_scores.keys():
        out.write('***' + event + '\n')
        for combi in event_bursti_scores[event]:
            out.write(combi + ' - ' + event_bursti_scores[event][combi] + '\n')

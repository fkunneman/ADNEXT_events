
import sys
import datetime
from collections import defaultdict
import numpy
import itertools

import time_functions


tweetfile = sys.argv[1]
outfile = sys.argv[2]

def dict2list(d):
    date = datetime.date(2014, 8, 1)
    keys = d.keys()
    l = []
    print(date, keys)
    while date < datetime.date(2014, 9, 1):
        if str(date) in keys:
            l.append(d[str(date)])
        else:
            l.append(0)
 #       print(date)
        date += datetime.timedelta(days = 1)
  #  print(l)
    return l

def score_burstiness(sequence, position):
    mean = numpy.mean(sequence)
    burstiness = sequence[position] / mean
    #print(sequence, position, mean, burstiness)    
    return burstiness

event_bursti_scores = defaultdict(list)
with open(tweetfile, 'r', encoding = 'utf-8') as infile:
    for line in infile.readlines():
        #print(line.encode('utf-8'))
        if line[:3] == '***':
            # start new event
            event_date = time_functions.return_datetime(line[3:13], setting = 'vs')
            event = line.strip()
            event_terms = event[14:].split(', ')
            event_term_ids = {}
            combi_timelist = {}
            id_date = {}
#            print(event.encode('utf-8'), event_date, event_terms)
            print(event.encode('utf-8'))
        elif line[:3] == '---':
            # start new event term
            event_term = line.strip()[3:].strip()
            print(event_term.encode('utf-8'))
        else:
            # collect tweets by date
            tweets = line.strip().split('----------')
            #print('\n'.join(tweets).encode('utf-8'))
            timedict = defaultdict(int)
            ids = []
            for tweet in tweets:
                tokens = tweet.split('\t')
                try:
                    date = time_functions.return_datetime(tokens[2], setting = 'vs')
                    timedict[tokens[2]] += 1
                    ids.append(tokens[1])
                    id_date[tokens[1]] = date
                except:
                    continue
            timelist = dict2list(timedict)
            combi_timelist[event_term] = timelist
            event_term_ids[event_term] = ids
 #           print(event_term, event_terms[-1])
            if event_term == event_terms[-1]:
                # append event to list
                if len(event_terms) > 1: # there exist combis
                    combis = [event_terms]
                    if len(event_terms) > 2:
                        for i in range(2, len(event_terms)):
                            for combi in (list(itertools.combinations(event_terms, i))):
                                combis.append(list(combi))
                    for combi in combis: # combine
                        combi_sets = []
                        for et in combi:
                            combi_sets.append(set(event_term_ids[et]))
                        overlap = set.intersection(*combi_sets)
                        print(','.join(combi).encode('utf-8'), overlap)
                        overlap_timedict = defaultdict(int)
                        for tid in list(overlap):
                            overlap_timedict[str(id_date[tid].date())] += 1
                        #print(overlap_timedict)
                        timelist = dict2list(overlap_timedict)
                        # print(timelist)
                        combi_timelist[', '.join(list(combi))] = timelist
                # calculate burstiness
                position = (event_date.date() - datetime.date(2014, 8, 1)).days
                combi_burst = []
                for combi in combi_timelist.keys():
                    burstiscore = score_burstiness(combi_timelist[combi], position)
                    if combi_timelist[combi][position] > 9:
                        combi_burst.append([combi, burstiscore, position])
                combi_burst_sorted = sorted(combi_burst, key = lambda k : k[1], reverse = True)
                for combi in combi_burst_sorted:
                    event_bursti_scores[event].append(combi[0] + ' - ' + str(combi[1]) + ' - ' + \
                        str(combi_timelist[combi[0]][position]) + ' - ' + \
                        ','.join([str(x) for x in combi_timelist[combi[0]]]))
            
with open(outfile, 'w', encoding = 'utf-8') as out:
    for event in event_bursti_scores.keys():
        out.write('***' + event + '\n')
        for combi in event_bursti_scores[event]:
            out.write(combi + '\n')

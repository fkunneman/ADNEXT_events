

import sys
import os
from collections import defaultdict
import numpy
import matplotlib.pyplot as plt

import time_functions
import emotion_utils
import calculations

classifications_dir = sys.argv[1]
unique_events_file = sys.argv[2]
outdir = sys.argv[3]

range_begin = -120
range_end = 121
timebins = defaultdict(list)
step = 6
i = -120
while i < 0:
    for j in range(i, i+step):
        timebins[j] = i
    i += step

i = 0
while i < 121:
    for j in range(i, i+step):
        timebins[j] = i+step
    i += step

def fill_timebins(tweets, event_date):
    timebin_classifications = defaultdict(list)
    for tweet in tweets:
        tokens = tweet.split('\t')
        classification = tokens[1]
        dt = time_functions.return_datetime(tokens[4], tokens[5], setting = 'vs')
        d = dt - event_date
        tfe = (d.days * 24) + (d.seconds / 3600)
        if tfe >= range_begin and tfe < range_end:
            timebin_classifications[timebins[tfe]].append(classification)
    return timebin_classifications

def return_counts(bs, d, target):
    counts = []
    ks = d.keys()
    for timebin in bs:
        if timebin in ks:
            freq = len(d[timebin])
            c = d[timebin].count(target)
            counts.append([freq, c])
        else:
            counts.append([None, None])
    return counts

with open(unique_events_file) as ue:
    unique_events = ue.read().split('\n')

timebin_zin = defaultdict(list)
timebin_teleurgesteld = defaultdict(list)
timebin_tevreden = defaultdict(list)
for event in unique_events[:100]:
    with open(classifications_dir + event + '_zin.txt', 'r', encoding = 'utf-8') as eo:
        lines = eo.readlines()
        event_data = lines[0].strip()
        tweets_zin = lines[1:]
    try:
        with open(classifications_dir + event + '_teleurgesteld.txt', 'r', encoding = 'utf-8') as eo:
            tweets_teleurgesteld = eo.readlines()[1:]
        with open(classifications_dir + event + '_tevreden.txt', 'r', encoding = 'utf-8') as eo:
            tweets_tevreden = eo.readlines()[1:]
    except:
        continue
    if len(tweets_zin) > 50 and len(tweets_teleurgesteld) > 50:  
        print(event)
        event_date = time_functions.return_datetime(event_data.split('\t')[1], setting = 'vs')
        zin = fill_timebins(tweets_zin, event_date)
        for k in zin.keys():
            timebin_zin[k].extend(zin[k])
        teleurgesteld = fill_timebins(tweets_teleurgesteld, event_date)
        for k in teleurgesteld.keys():
            timebin_teleurgesteld[k].extend(teleurgesteld[k])
        tevreden = fill_timebins(tweets_tevreden, event_date)
        for k in tevreden.keys():
            timebin_tevreden[k].extend(tevreden[k])

keys = sorted(list(set(timebins.values())))
counts_zin = return_counts(timebin_zin)
counts_teleurgesteld = return_counts(timebin_teleurgesteld)
counts_tevreden = return_counts(timebin_tevreden)

t1 = [x[0] for x in counts_zin if x[0] != None] 
t2 = [x[0] for x in counts_teleurgesteld if x[0] != None]
t3 = [x[0] for x in counts_tevreden if x[0] != None]
t = t1 + [None] + t2
print('T1*********\n', t1)
print('T2*********\n', t2)
print('T3*********\n', t3)
print('T*********\n', t)

plot_zin = [x[1] for x in counts_zin]
plot_tevreden = [x[1] for x in counts_tevreden]
plot_teleurgesteld = [x[1] for x in counts_teleurgesteld]

plt.plot(x, prcs_zin, linestyle = '-', linewidth = 2)
plt.plot(x, prcs_teleurgesteld, linestyle = '--', linewidth = 2)
plt.plot(x, prcs_tevreden, linestyle = ':', linewidth = 2)
plt.xlabel('Hours in relation to event date')
plt.ylabel('Number of tweets')
legend = ['Total tweets', 'Tweets expressing positive expectation', 'Tweets expressing disappointment', 'Tweets expressing satisfaction']
plt.legend(legend,  loc = "upper left")
plt.savefig(outdir + 'timeplot_total_freqs.png', bbox_inches = "tight")
plt.clf()



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
timebins = {}
step = 6
i = -120
while i < -5:
    for j in range(i, i+step):
        timebins[j] = i
    i += step

i = 1
while i < 116:
    for j in range(i, i+step):
        timebins[j] = i+(step-1)
    i += step

def fill_timebins(tweets, event_date):
    timebin_classifications = defaultdict(list)
    for tweet in tweets:
        tokens = tweet.split('\t')
        classification = tokens[1]
        dt = time_functions.return_datetime(tokens[4], tokens[5], setting = 'vs')
        d = dt - event_date
        tfe = int((d.days * 24) + (d.seconds / 3600))
        if tfe > 23:
            tfe = tfe - 24
        if tfe >= range_begin and tfe < range_end and tfe != 0:
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
for event in unique_events:
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
        tel = False
        for k in teleurgesteld.keys():
            timebin_teleurgesteld[k].extend(teleurgesteld[k])
        tevreden = fill_timebins(tweets_tevreden, event_date)
        for k in tevreden.keys():
            timebin_tevreden[k].extend(tevreden[k])

keys = sorted(list(set(timebins.values())) + [0])
counts_zin = return_counts(keys, timebin_zin, 'zin')
counts_teleurgesteld = return_counts(keys, timebin_teleurgesteld, 'teleurgesteld')
counts_tevreden = return_counts(keys, timebin_tevreden, 'tevreden')

t1 = [x[0] for x in counts_zin[:21]] 
t2 = [x[0] for x in counts_teleurgesteld[21:]]
t = t1 + t2

plot_zin = [x[1] for x in counts_zin]
plot_tevreden = [x[1] for x in counts_tevreden]
plot_teleurgesteld = [x[1] for x in counts_teleurgesteld]

plt.plot(keys, t, linestyle = '-', linewidth = 2)
plt.plot(keys, plot_zin, linestyle = '-.', linewidth = 2)
plt.plot(keys, plot_teleurgesteld, linestyle = '--', linewidth = 2)
plt.plot(keys, plot_tevreden, linestyle = ':', linewidth = 2)
plt.xlabel('Hours in relation to event date')
plt.ylabel('Number of tweets')
legend = ['Total tweets', 'Positive expectation', 'Disappointment', 'Satisfaction']
plt.legend(legend,  loc = "upper left")
plt.savefig(outdir + 'timeplot_total_freqs.png', bbox_inches = "tight")
plt.clf()

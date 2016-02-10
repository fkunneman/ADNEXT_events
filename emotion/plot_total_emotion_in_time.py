

import sys
import os
from collections import defaultdict
import numpy
import matplotlib.pyplot

import time_functions
import calculations

classifications_dir = sys.argv[1]
unique_events_file = sys.argv[2]
outdir = sys.argv[3]
range_begin = int(sys.argv[4])
range_end = int(sys.argv[5])

def fill_timebins(tweets, event_date):
    timebin_scores = defaultdict(list)
    for tweet in tweets:
        tokens = tweet.split('\t')
        score = float(tokens[0])
        date = time_functions.return_datetime(tokens[3], setting = 'vs')
        tfe = (date - event_date).days
        if tfe >= range_begin and tfe < range_end:
            timebin_scores[tfe].append(score)
    return timebin_scores

def return_prcs(d):
    prcs = [] 
    for timebin in range(range_begin, range_end):
        if timebin in d:
            prcs.append(calculations.return_percentile(timebin_scores[timebin], 0.9))
        else:
            prcs.append(0)
    return prcs

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
    with open(classifications_dir + event_id + '_teleurgesteld.txt', 'r', encoding = 'utf-8') as eo:
        tweets_teleurgesteld = eo.readlines()[1:]
    with open(classifications_dir + event_id + '_tevreden.txt', 'r', encoding = 'utf-8') as eo:
        tweets_tevreden = eo.readlines()[1:]
    if len(tweets_zin) > 50 and len(tweets_teleurgesteld) > 50:  
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

prcs_zin = return_prcs(timebin_zin)
prcs_teleurgesteld = return_prcs(timebin_teleurgesteld)
prcs_tevreden = return_prcs(timebin_tevreden)

x = range(range_begin, range_end)
plt.plot(x, prcs_zin, linestyle = '-', linewidth = 2)
plt.plot(x, prcs_teleurgesteld, linestyle = '--', linewidth = 2)
plt.plot(x, prcs_tevreden, linestyle = ':', linewidth = 2)
plt.xlabel('Days in relation to event date')
plt.ylabel('0.90 percentile classifier score for emotion')
legend = ['Positive expectation', 'Disappointment', 'Satisfaction']
plt.legend(legend,  loc = "upper right")
plt.savefig(outdir + 'timeplot_' + event + '.png', bbox_inches = "tight")
plt.clf()

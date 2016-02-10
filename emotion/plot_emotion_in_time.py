

import sys
import os
from collections import defaultdict
import numpy
import matplotlib.pyplot

import time_functions

classifications_dir = sys.argv[1]
outdir = sys.argv[2]
range_begin = int(sys.argv[3])
range_end = int(sys.argv[4])
events = sys.argv[5:]

linestyles = ["-","--","-.",":"]

def fill_timebins(tweets, event_date):
    timebin_scores = defaultdict(list)
    for tweet in tweets:
        tokens = tweet.split('\t')
        score = float(tokens[0])
        date = time_functions.return_datetime(tokens[3], setting = 'vs')
        tfe = (date - event_date).days
        timebin_scores[tfe].append(score)
    tbs = list(timebin_scores.keys())   
    avgs = [] 
    for timebin in range(range_begin, range_end):
        if timebin in tbs:
            avgs.append(numpy.mean(timebin_scores[timebin]))
        else:
            avgs.append(0)
    return avgs

for event in events:
    with open(classifications_dir + event + '_zin.txt', 'r', encoding = 'utf-8') as eo:
        lines = eo.readlines()
        event_data = lines[0].strip()
        tweets_zin = lines[1:]
    with open(classifications_dir + event_id + '_teleurgesteld.txt', 'r', encoding = 'utf-8') as eo:
        tweets_teleurgesteld = eo.readlines()[1:]
    with open(classifications_dir + event_id + '_tevreden.txt', 'r', encoding = 'utf-8') as eo:
        tweets_tevreden = eo.readlines()[1:]
    event_date = time_functions.return_datetime(event_data.split('\t')[1], setting = 'vs')
    avgs_zin = fill_timebins(tweets_zin, event_date)
    avgs_teleurgesteld = fill_timebins(tweets_teleurgesteld, event_date)
    avgs_tevreden = fill_timebins(tweets_tevreden, event_date)
    x = range(range_begin, range_end)
    plt.plot(x, avg_zin, linestyle = '-', linewidth = 2)
    plt.plot(x, avg_teleurgesteld, linestyle = '--', linewidth = 2)
    plt.plot(x, avg_tevreden, linestyle = ':', linewidth = 2)
    plt.xlabel('Days in relation to event date')
    plt.ylabel('Avg classifier score for emotion')
    legend = ['Positive expectation', 'Disappointment', 'Satisfaction']
    plt.legend(legend,  loc = "upper right")
    plt.savefig(outdir + 'timeplot_' + event + '.png', bbox_inches = "tight")
    plt.clf()



import sys
import os
from collections import defaultdict
import numpy
import matplotlib.pyplot as plt

import time_functions

classifications_dir = sys.argv[1]
outdir = sys.argv[2]
range_begin = int(sys.argv[3])
range_end = int(sys.argv[4])
events = sys.argv[5:]

timebins = {}
step = 6
i = range_begin
while i < -5:
    for j in range(i, i+step):
        timebins[j] = i
    i += step

i = 1
while i < (range_end - 4):
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

def fill_timebins_doublec(tweets_c1, tweets_c2, event_date):
    timebin_classifications = defaultdict(list)
    tid_classifications = defaultdict(list) 
    tid_tokens = {}
    for tweet in tweets_c1:
        tokens = tweet.split('\t')
        tid = tokens[2]
        tid_tokens[tid] = tokens
        classification = tokens[1]
        tid_classifications[tid].append(classification)
    for tweet in tweets_c2:
        tokens = tweet.split('\t')
        tid = tokens[2]
        tid_tokens[tid] = tokens
        classification = tokens[1]
        tid_classifications[tid].append(classification)
    for tid in tid_classifications.keys():
        classifications = tid_classifications[tid]
        if classifications.count('other') == 2:
            cc = 'other'
        elif classifications.count('other') == 0:
            cc = 'mixed'
        elif classifications.count('teleurgesteld') == 1:
            cc = 'teleurgesteld'
        elif classifications.count('tevreden') == 1:
            cc = 'tevreden'
        tokens = tid_tokens[tid]
        dt = time_functions.return_datetime(tokens[4], tokens[5], setting = 'vs')
        d = dt - event_date
        tfe = int((d.days * 24) + (d.seconds / 3600))
        if tfe > 23:
            tfe = tfe - 24
        if tfe >= range_begin and tfe < range_end and tfe != 0:
            try:
                timebin_classifications[timebins[tfe]].append(cc)
            except:
                print(classifications)
    return timebin_classifications

def return_counts(bs, d, targets):
    counts = []
    ks = d.keys()
    for timebin in bs:
        if timebin in ks:
            bincounts = []
            for target in targets:
                c = d[timebin].count(target)
                bincounts.append(c)
            counts.append(bincounts)
        else:
            bincounts = [0] * len(targets)
            counts.append(bincounts)
    return counts

keys = sorted(list(set(timebins.values())) + [0])
half = int((len(keys) + 1) / 2)
for event in events:
    print(event)
    with open(classifications_dir + event + '_zin.txt', 'r', encoding = 'utf-8') as eo:
        lines = eo.readlines()
        event_data = lines[0].strip()
        tweets_zin = lines[1:]
    with open(classifications_dir + event + '_teleurgesteld.txt', 'r', encoding = 'utf-8') as eo:
        tweets_teleurgesteld = eo.readlines()[1:]
    with open(classifications_dir + event + '_tevreden.txt', 'r', encoding = 'utf-8') as eo:
        tweets_tevreden = eo.readlines()[1:]
    event_date = time_functions.return_datetime(event_data.split('\t')[1], setting = 'vs')
    timebins_zin = fill_timebins(tweets_zin, event_date)
    timebins_teleurgesteld_tevreden = fill_timebins_doublec(tweets_teleurgesteld, tweets_tevreden, event_date)
    counts_before = return_counts(keys, timebins_zin, ['zin', 'other'])
    counts_after = return_counts(keys, timebins_teleurgesteld_tevreden, ['teleurgesteld', 'tevreden', 'mixed', 'other'])
    vals_other = [x[1] for x in counts_before[:21]] + [x[3] for x in counts_after[21:]]
    vals_zin = [x[0] for x in counts_before]
    vals_teleurgesteld = [x[0] for x in counts_after]
    vals_mixed = [x[2] for x in counts_after]
    vals_tevreden = [x[1] for x in counts_after]
    
    plt.bar(keys, vals_zin, 5, color = 'g')
    plt.bar(keys, vals_teleurgesteld, 5, color = 'r', bottom = list(map(sum, zip(vals_zin))))
    plt.bar(keys, vals_mixed, 5, color = 'purple', bottom = list(map(sum, zip(vals_zin, vals_teleurgesteld))))
    plt.bar(keys, vals_tevreden, 5, color = 'lightskyblue', bottom = list(map(sum, zip(vals_zin, vals_teleurgesteld, vals_mixed))))
    plt.bar(keys, vals_other, 5, color = 'white', bottom = list(map(sum, zip(vals_zin, vals_teleurgesteld, vals_mixed, vals_tevreden))))
    #plt.plot(keys, list(map(sum, zip(vals_zin, vals_teleurgesteld, vals_mixed, vals_tevreden, vals_other))))
    plt.xlabel('Hours in relation to event date')
    plt.ylabel('Number of tweets')
    legend = ['PE', 'D', 'D + S', 'S', 'Other']
    plt.legend(legend,  loc = "upper left")
    plt.savefig(outdir + 'timeplot_' + event + '.png', bbox_inches = "tight")
    plt.clf()

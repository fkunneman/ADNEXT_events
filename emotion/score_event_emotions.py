
import os
import sys
import numpy
import math

import emotion_utils
import calculations
import linewriter

classificationdir_zinin = sys.argv[1]
classificationdir_teleurgesteld = sys.argv[2]
classificationdir_tevreden = sys.argv[3]
outfile = sys.argv[4]
outfile_complete = sys.argv[5]

events_zinin = os.listdir(classificationdir_zinin)
events_teleurgesteld = os.listdir(classificationdir_teleurgesteld)
events_tevreden = os.listdir(classificationdir_tevreden)

event_scores = []
event_scores_half = []

print('Parsing events')
for event in events_zinin:
    event_id = event[:-4]
#    print(event_id)
    with open(classificationdir_zinin + event, 'r', encoding = 'utf-8') as zin_in:
        scores_zinin = list(emotion_utils.parse_lcs_classifications(zin_in.readlines(), 'zin').values())
    if len(scores_zinin) > 0:
        stats_zinin = list(emotion_utils.calculate_event_emotion_stats(scores_zinin).values())
    else:
        continue
    try:
        with open(classificationdir_teleurgesteld + event, 'r', encoding = 'utf-8') as teleurgesteld_in:
            scores_teleurgesteld = list(emotion_utils.parse_lcs_classifications(teleurgesteld_in.readlines(), 'teleurgesteld').values())
        with open(classificationdir_tevreden + event, 'r', encoding = 'utf-8') as tevreden_in:
            scores_tevreden = list(emotion_utils.parse_lcs_classifications(tevreden_in.readlines(), 'tevreden').values())
        if len(scores_teleurgesteld) > 0:
            stats_teleurgesteld = list(emotion_utils.calculate_event_emotion_stats(scores_teleurgesteld).values())
            stats_tevreden = list(emotion_utils.calculate_event_emotion_stats(scores_tevreden).values())
            event_scores.append([event_id] + stats_zinin + stats_teleurgesteld + stats_tevreden)
        else:
            event_scores_half.append([event_id] + stats_zinin + ['-', '-', '-', '-', '-', '-', '-', '-'])
            
    except:
        print('No after event data')
        event_scores_half.append([event_id] + stats_zinin + ['-', '-', '-', '-', '-', '-', '-', '-'])

#lost_events = list(set(events_teleurgesteld) - set(events_zinin))
#for event in lost_events:
#    event_id = event[:-4]
#    print('rest', event_id)
#    with open(classificationdir_teleurgesteld + event, 'r', encoding = 'utf-8') as teleurgesteld_in:
#        scores_teleurgesteld = emotion_utils.parse_lcs_classifications(teleurgesteld_in.readlines(), 'teleurgesteld')
#    with open(classificationdir_tevreden + event, 'r', encoding = 'utf-8') as tevreden_in:
#        scores_tevreden = emotion_utils.parse_lcs_classifications(tevreden_in.readlines(), 'tevreden')
#    stats_teleurgesteld = emotion_utils.calculate_event_emotion_stats(scores_teleurgesteld)
#    stats_tevreden = emotion_utils.calculate_event_emotion_stats(scores_tevreden)
#    event_scores_half.append([event_id] + ['-', '-', '-', '-'] + stats_teleurgesteld + stats_tevreden)

#event_scores_all = event_scores + event_scores_half
#lw = linewriter.Linewriter(event_scores_all)
#lw.write_txt(outfile)

print('making calculations')
event_scores_zin_mean = [x[2] for x in event_scores]
ranks_zin_mean = calculations.rank_scores(event_scores_zin_mean)
event_scores_zin_median = [x[3] for x in event_scores]
ranks_zin_median = calculations.rank_scores(event_scores_zin_median)
event_scores_zin_percentile = [x[4] for x in event_scores]
ranks_zin_percentile = calculations.rank_scores(event_scores_zin_percentile)

event_scores_teleurgesteld_mean = [x[6] for x in event_scores]
ranks_teleurgesteld_mean = calculations.rank_scores(event_scores_teleurgesteld_mean)
event_scores_teleurgesteld_median = [x[7] for x in event_scores]
ranks_teleurgesteld_median = calculations.rank_scores(event_scores_teleurgesteld_median)
event_scores_teleurgesteld_percentile = [x[8] for x in event_scores]
ranks_teleurgesteld_percentile = calculations.rank_scores(event_scores_zin_percentile)

event_scores_tevreden_mean = [x[10] for x in event_scores]
ranks_tevreden_mean = calculations.rank_scores(event_scores_tevreden_mean)
event_scores_tevreden_median = [x[11] for x in event_scores]
ranks_tevreden_median = calculations.rank_scores(event_scores_tevreden_median)
event_scores_tevreden_percentile = [x[12] for x in event_scores]
ranks_tevreden_percentile = calculations.rank_scores(event_scores_tevreden_percentile)

event_scores_complete_ranks = []
for i, event in enumerate(event_scores):
#    print(event[0])
#    print('before', event)
    if event[1] > 50 and event[5] > 50: 
        event.insert(3, ranks_zin_mean[i])
        event.insert(5, ranks_zin_median[i])
        event.insert(7, ranks_zin_percentile[i])
        event.insert(10, ranks_teleurgesteld_mean[i])
        event.insert(12, ranks_teleurgesteld_median[i])
        event.insert(14, ranks_teleurgesteld_percentile[i])

        event.insert(17, ranks_tevreden_mean[i])
        event.insert(19, ranks_tevreden_median[i])
        event.insert(21, ranks_tevreden_percentile[i])
#    print('middle', event)
        anticipointment_mean = calculations.calculate_mean_reciprocal_rank([ranks_zin_mean[i], ranks_teleurgesteld_mean[i]])
        anticipointment_median = calculations.calculate_mean_reciprocal_rank([ranks_zin_median[i], ranks_teleurgesteld_median[i]])
        anticifaction_mean = calculations.calculate_mean_reciprocal_rank([ranks_zin_mean[i], ranks_tevreden_mean[i]])
        anticifaction_median = calculations.calculate_mean_reciprocal_rank([ranks_zin_median[i], ranks_tevreden_median[i]])
        event.extend([anticipointment_mean, anticipointment_median, anticifaction_mean, anticifaction_median])
#    print('after', event)
        event_scores_complete_ranks.append(event)

print('writing to file')
#event_scores_complete_ranks_clean = []
#for l in event_scores_complete_ranks:
#    nl = []
#    for x in l:
#        if type(x) is float:
#            if math.isnan(x):
#                nl.append(0.0)
#            else:
#                nl.append(x)
#        else:
#            nl.append(x)
#    event_scores_complete_ranks_clean.append(nl)
headers = ['event', '#zin', 'mean zin', 'rank mean zin', 'median zin', 'rank median zin', '0.9 percentile zin', 'rank 0.9 percentile zin', '#teleurgesteld', 'mean teleurgesteld', 
    'rank mean teleurgesteld', 'median teleurgesteld', 'rank median teleurgesteld', '0.9 percentile teleurgesteld', 'rank 0.9 percentile teleurgesteld', '#tevreden', 'mean tevreden', 
    'rank mean tevreden', 'median tevreden', 'rank median tevreden', '0.9 percentile tevreden', 'rank 0.9 percentile tevreden', 'anticipointment mean', 'anticipointment median', 
    'anticifaction mean', 'anticifaction median']
header_style = {'event' : 'general', '#zin' : '0', 'mean zin' : '0.00', 'rank mean zin' : '0', 'median zin' : '0.00', 
    'rank median zin' : '0', '0.9 percentile zin' : '0.00', 'rank 0.9 percentile zin' : '0', '#teleurgesteld' : '0', 'mean teleurgesteld' : '0.00', 'rank mean teleurgesteld' : '0', 
    'median teleurgesteld' : '0.00', 'rank median teleurgesteld' : '0', '0.9 percentile teleurgesteld' : '0.00', 'rank 0.9 percentile teleurgesteld' : '0', '#tevreden' : '0', 'mean tevreden' : '0.00', 
    'rank mean tevreden' : '0', 'median tevreden' : '0.00', 'rank median tevreden' : '0', '0.9 percentile tevreden' : '0.00', 'rank 0.9 percentile tevreden' : '0', 'anticipointment mean' : '0.00', 
    'anticipointment median' : '0.00', 'anticifaction mean' : '0.00', 'anticifaction median' : '0.00'}

lw = linewriter.Linewriter(event_scores_complete_ranks)
lw.write_xls(headers, header_style, outfile_complete)

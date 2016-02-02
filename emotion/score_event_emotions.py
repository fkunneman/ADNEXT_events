
import os
import sys
import numpy

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
for event in events_zinin[:10]:
    event_id = event[:-4]
    print(event_id)
    with open(classificationdir_zinin + event, 'r', encoding = 'utf-8') as zin_in:
        scores_zinin = emotion_utils.parse_lcs_classifications(zin_in.readlines(), 'zin')
    stats_zinin = calculations.calculate_event_emotion_stats(scores_zinin)
    try:
        with open(classificationdir_teleurgesteld + event, 'r', encoding = 'utf-8') as teleurgesteld_in:
            scores_teleurgesteld = emotion_utils.parse_lcs_classifications(teleurgesteld_in.readlines(), 'teleurgesteld')
        with open(classificationdir_tevreden + event, 'r', encoding = 'utf-8') as tevreden_in:
            scores_tevreden = emotion_utils.parse_lcs_classifications(tevreden_in.readlines(), 'tevreden')
        stats_teleurgesteld = calculations.calculate_event_emotion_stats(scores_teleurgesteld)
        stats_tevreden = calculations.calculate_event_emotion_stats(scores_tevreden)
        event_scores.append([event_id] + stats_zinin + stats_teleurgesteld + stats_tevreden)
    except:
        print('No after event data')
        event_scores_half.append([event_id] + stats_zinin + ['-', '-', '-', '-', '-', '-'])

lost_events = list(set(events_teleurgesteld) - set(events_zinin))
for event in lost_events[:2]:
    event_id = event[:-4]
    print(event_id)
    with open(classificationdir_teleurgesteld + event, 'r', encoding = 'utf-8') as teleurgesteld_in:
        scores_teleurgesteld = emotion_utils.parse_lcs_classifications(teleurgesteld_in.readlines(), 'teleurgesteld')
    with open(classificationdir_tevreden + event, 'r', encoding = 'utf-8') as tevreden_in:
        scores_tevreden = emotion_utils.parse_lcs_classifications(tevreden_in.readlines(), 'tevreden')
    stats_teleurgesteld = calculations.calculate_event_emotion_stats(scores_teleurgesteld)
    stats_tevreden = calculations.calculate_event_emotion_stats(scores_tevreden)
    event_scores_half.append([event_id] + ['-', '-', '-'] + stats_teleurgesteld + stats_tevreden)

event_scores_all = event_scores + event_scores_half
lw = linewriter.Linewriter(event_scores_all)
lw.write_txt(outfile)

print('making calculations')
event_scores_zin_mean = [x[2] for x in event_scores]
ranks_zin_mean = calculations.rank_scores(event_scores_zin_mean)
event_scores_zin_median = [x[3] for x in event_scores]
ranks_zin_median = calculations.rank_scores(event_scores_zin_median)

event_scores_teleurgesteld_mean = [x[5] for x in event_scores]
ranks_teleurgesteld_mean = calculations.rank_scores(event_scores_teleurgesteld_mean)
event_scores_teleurgesteld_median = [x[6] for x in event_scores]
ranks_teleurgesteld_median = calculations.rank_scores(event_scores_teleurgesteld_median)

event_scores_tevreden_mean = [x[8] for x in event_scores]
ranks_tevreden_mean = calculations.rank_scores(event_scores_tevreden_mean)
event_scores_tevreden_median = [x[9] for x in event_scores]
ranks_tevreden_median = calculations.rank_scores(event_scores_tevreden_median)

event_scores_complete_ranks = []
for i, event in event_scores:
    event.insert(2, ranks_zin_mean[i])
    event.insert(3, ranks_zin_median[i])
    event.insert(5, ranks_teleurgesteld_mean[i])
    event.insert(6, ranks_teleurgesteld_median[i])
    event.insert(8, ranks_tevreden_mean[i])
    event.insert(9, ranks_tevreden_median[i])
    anticipointment_mean = calculations.calculate_mean_reciprocal_rank([ranks_zin_mean[i], ranks_teleurgesteld_mean[i]])
    anticipointment_median = calculations.calculate_mean_reciprocal_rank([ranks_zin_mean[i], ranks_teleurgesteld_median[i]])
    anticifaction_mean = calculations.calculate_mean_reciprocal_rank([ranks_zin_mean[i], ranks_tevreden_mean[i]])
    anticifaction_median = calculations.calculate_mean_reciprocal_rank([ranks_zin_mean[i], ranks_tevreden_median[i]])
    event.extend([anticipointment_mean, anticipointment_median, anticifaction_mean, anticifaction_median])
    event_scores_complete_ranks.append(event)

print('writing to file')
headers = ['event', '#zin', 'mean zin', 'rank mean zin', 'median zin', 'rank median zin', '#teleurgesteld', 'mean teleurgesteld', 
    'rank mean teleurgesteld', 'median teleurgesteld', 'rank median teleurgesteld', '#tevreden', 'mean tevreden', 
    'rank mean tevreden', 'median tevreden', 'rank median tevreden', 'anticipointment mean', 'anticipointment median', 
    'anticifaction mean', 'anticifaction median']
header_style = {'event' : 'general', '#zin' : '0', 'mean zin' : '0.00', 'rank mean zin' : '0', 'median zin' : '0.00', 
    'rank median zin' : '0', '#teleurgesteld' : '0', 'mean teleurgesteld' : '0.00', 'rank mean teleurgesteld' : '0', 
    'median teleurgesteld' : '0.00', 'rank median teleurgesteld' : '0', '#tevreden' : '0', 'mean tevreden' : '0.00', 
    'rank mean tevreden' : '0', 'median tevreden' : '0.00', 'rank median tevreden' : '0', 'anticipointment mean' : '0.00', 
    'anticipointment median' : '0.00', 'anticifaction mean' : '0.00', 'anticifaction median' : '0.00'}

lw = linewriter.Linewriter(event_scores_complete_ranks)
lw.write_xls(headers, header_style, outfile_complete)


import os
import sys
import numpy

classificationdir_zinin = sys.argv[1]
classificationdir_teleurgesteld = sys.argv[2]
classificationdir_tevreden = sys.argv[3]
outfile = sys.argv[4]
outfile_complete = sys.argv[5]

events_zinin = os.listdir(classificationdir_zinin)
events_teleurgesteld = os.listdir(classificationdir_teleurgesteld)
events_tevreden = os.listdir(classificationdir_tevreden)

event_scores = []

for event in events_zinin:
    event_id = event[:-4]
    print(event_id)
    scores_zinin = []
    scores_teleurgesteld = []
    scores_tevreden = []
    with open(classificationdir_zinin + event, 'r', encoding = 'utf-8') as zin_in:
        for line in zin_in.readlines():
            try:
                tokens = line.strip().split()
                classifications = tokens[1:]
                classification_zinin = [x for x in classifications if x.split(":")[0] == 'zin' or x.split(":")[0] == '?zin'][0]
                score = float(classification_zinin.split(':')[1])
                scores_zinin.append(score)
            except:
                print('wrong input', line.encode('utf-8'))
    try:
        with open(classificationdir_teleurgesteld + event, 'r', encoding = 'utf-8') as teleurgesteld_in:
            for line in teleurgesteld_in.readlines():
                try:
                    tokens = line.strip().split()
                    classifications = tokens[1:]
                    classifications_teleurgesteld = [x for x in classifications if x.split(":")[0] == 'teleurgesteld' \
                    or x.split(":")[0] == '?teleurgesteld'][0]
                    score = float(classifications_teleurgesteld.split(':')[1])
                    scores_teleurgesteld.append(score)
                except:
                    print('wrong input', line.encode('utf-8'))
        with open(classificationdir_tevreden + event, 'r', encoding = 'utf-8') as tevreden_in:
            for line in tevreden_in.readlines():
                try:
                    tokens = line.strip().split()
                    classifications = tokens[1:]
                    classifications_tevreden = [x for x in classifications if x.split(":")[0] == 'tevreden' \
                        or x.split(":")[0] == '?tevreden'][0]
                    score = float(classifications_teleurgesteld.split(':')[1])
                    scores_tevreden.append(score)
                except:
                    print('wrong input', line.encode('utf-8'))
    except:
        print('No after event data')
    num_zinin = len(scores_zinin)
    mean_zinin = round(numpy.mean(scores_zinin), 2)
    median_zinin = round(numpy.median(scores_zinin), 2)
    num_teleurgesteld = len(scores_teleurgesteld)
    num_tevreden = len(scores_tevreden)
    if num_teleurgesteld > 0:
        mean_teleurgesteld = round(numpy.mean(scores_teleurgesteld), 2)
        median_teleurgesteld = round(numpy.median(scores_teleurgesteld), 2)
        mean_tevreden = round(numpy.mean(scores_tevreden), 2)
        median_tevreden = round(numpy.mean(scores_tevreden), 2)
        anticipointment_gap_mean = mean_zinin + mean_teleurgesteld
        anticipointment_gap_median = median_zinin + median_teleurgesteld
        anticifaction_gap_mean = mean_zinin + mean_tevreden
        anticifaction_gap_median = median_zinin + median_tevreden
    else:
        mean_teleurgesteld = '-'
        median_teleurgesteld = '-'
        mean_tevreden = '-'
        median_tevreden = '-'
        anticipointment_gap_mean = '-'
        anticipointment_gap_median = '-'
        anticifaction_gap_mean = '-'
        anticifaction_gap_median = '-'
    event_scores.append([event_id, num_zinin, mean_zinin, median_zinin, num_teleurgesteld, mean_teleurgesteld, median_teleurgesteld, 
        num_tevreden, mean_tevreden, median_tevreden, anticipointment_gap_mean, anticipointment_gap_median, anticifaction_gap_mean,
        anticifaction_gap_median])

lost_events = list(set(events_teleurgesteld) - set(events_zinin))
for event in lost_events:
    event_id = event[:-4]
    print(event_id)
    scores_teleurgesteld = []
    scores_tevreden = []
    with open(classificationdir_teleurgesteld + event, 'r', encoding = 'utf-8') as teleurgesteld_in:
        for line in teleurgesteld_in.readlines():
            try:
                tokens = line.strip().split()
                classifications = tokens[1:]
                classifications_teleurgesteld = [x for x in classifications if x.split(":")[0] == 'teleurgesteld' \
                    or x.split(":")[0] == '?teleurgesteld'][0]
                score = float(classifications_teleurgesteld.split(':')[1])
                scores_teleurgesteld.append(score)
            except:
                print('wrong input', line.encode('utf-8'))
    with open(classificationdir_tevreden + event, 'r', encoding = 'utf-8') as tevreden_in:
        for line in tevreden_in.readlines():
            try:
                tokens = line.strip().split()
                classifications = tokens[1:]
                classifications_tevreden = [x for x in classifications if x.split(":")[0] == 'tevreden' \
                    or x.split(":")[0] == '?tevreden'][0]
                score = float(classifications_teleurgesteld.split(':')[1])
                scores_tevreden.append(score)
            except:
                print('wrong input', line.encode('utf-8'))
    num_zinin = '-'
    mean_zinin = '-'
    median_zinin = '-'
    num_teleurgesteld = len(scores_teleurgesteld)
    num_tevreden = len(scores_tevreden)
    mean_teleurgesteld = round(numpy.mean(scores_teleurgesteld), 2)
    median_teleurgesteld = round(numpy.median(scores_teleurgesteld), 2)
    mean_tevreden = round(numpy.mean(scores_tevreden), 2)
    median_tevreden = round(numpy.mean(scores_tevreden), 2)
    anticipointment_gap_mean = '-'
    anticipointment_gap_median = '-'
    anticifaction_gap_mean = '-'
    anticifaction_gap_median = '-'
    event_scores.append([event_id, num_zinin, mean_zinin, median_zinin, num_teleurgesteld, mean_teleurgesteld, median_teleurgesteld, 
        num_tevreden, mean_tevreden, median_tevreden, anticipointment_gap_mean, anticipointment_gap_median, anticifaction_gap_mean,
        anticifaction_gap_median])

event_scores_complete_only = [x for x in event_scores if x[-1] != '-']
event_scores_complete_only_sorted = sorted(event_scores_complete_only, key = lambda k : k[10], reverse = True)
header = ['event', '#zin', 'mean zin', 'median zin', '#teleurgesteld', 'mean teleurgesteld', 'median teleurgesteld',
    '#tevreden', 'mean tevreden', 'median tevreden', 'anticipointment_gap_mean', 'anticipointment_gap_median', 
    'anticifaction_gap_mean', 'anticifaction_gap_median']

with open(outfile, 'w') as f_out:
    f_out.write('\t'.join(header) + '\n')
    for es in event_scores:
        try:
            f_out.write('\t'.join(["%.2f" % x for x in es]) + '\n')
        except:
            f_out.write('\t'.join([str(x) for x in es]) + '\n')
        
with open(outfile_complete, 'w') as f_out:
    f_out.write('\t'.join(header) + '\n')
    for es in event_scores_complete_only_sorted:
        try:
            f_out.write('\t'.join(["%.2f" % x for x in es]) + '\n')
        except:
            f_out.write('\t'.join([str(x) for x in es]) + '\n')


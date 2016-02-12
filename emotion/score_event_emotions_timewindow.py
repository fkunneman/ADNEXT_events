
import os
import sys

import docreader
import linewriter
import time_functions
import emotion_utils

classificationdir = sys.argv[1]
timewindow = int(sys.argv[2]) # in days
new_classifications = sys.argv[3]
scores_out = sys.argv[4]

classifications = os.listdir(classificationdir)
events = list(set([x.split('_')[0] for x in classifications]))

new_scores = []
for event in events:
    print(event)
    # zin
    try:
        dr_zin = docreader.Docreader()
        dr_zin.parse_doc(classificationdir + event + '_zin.txt')
    except:
        continue
    event_date = time_functions.return_datetime(dr_zin.lines[0][-1], setting = 'vs')
    zin_tweets = [dr_zin.lines[0]]
    for tweet in dr_zin.lines[1:]:
        tweet_date = time_functions.return_datetime(tweet[4], setting = 'vs')
        if (event_date - tweet_date).days <= timewindow:
            zin_tweets.append(tweet)
    zin_scores = [[float(tweet[0]), tweet[1]] for tweet in zin_tweets]
    if len(zin_scores) > 0:
        stats_zin = emotion_utils.calculate_event_emotion_stats(zin_scores)
        lw = linewriter.Linewriter(zin_tweets)
        lw.write_txt(new_classifications + event + '_zin.txt')
    else:
        continue
    # teleurgesteld
    try:
        dr_teleurgesteld = docreader.Docreader()
        dr_teleurgesteld.parse_doc(classificationdir + event + '_teleurgesteld.txt')
    except:
        continue
    event_date = time_functions.return_datetime(dr_teleurgesteld.lines[0][-1], setting = 'vs')
    teleurgesteld_tweets = [dr_teleurgesteld.lines[0]]
    for tweet in dr_teleurgesteld.lines[1:]:
        tweet_date = time_functions.return_datetime(tweet[3], setting = 'vs')
        if (tweet_date - event_date).days <= timewindow:
            teleurgesteld_tweets.append(tweet)
    teleurgesteld_scores = [float(tweet[0]) for tweet in teleurgesteld_tweets]
    if len(teleurgesteld_scores) > 0:
        stats_teleurgesteld = emotion_utils.calculate_event_emotion_stats(teleurgesteld_scores)
        lw = linewriter.Linewriter(teleurgesteld_tweets)
        lw.write_txt(new_classifications + event + '_teleurgesteld.txt')
    else:
        continue
    # tevreden
    try:
        dr_tevreden = docreader.Docreader()
        dr_tevreden.parse_doc(classificationdir + event + '_tevreden.txt')
    except:
        continue
    event_date = time_functions.return_datetime(dr_tevreden.lines[0][-1], setting = 'vs')
    tevreden_tweets = [dr_tevreden.lines[0]]
    for tweet in dr_tevreden.lines[1:]:
        tweet_date = time_functions.return_datetime(tweet[3], setting = 'vs')
        if (tweet_date - event_date).days <= timewindow:
            tevreden_tweets.append(tweet)
    tevreden_scores = [float(tweet[0]) for tweet in tevreden_tweets]
    if len(tevreden_scores) > 0:
        stats_tevreden = emotion_utils.calculate_event_emotion_stats(tevreden_scores)
        lw = linewriter.Linewriter(tevreden_tweets)
        lw.write_txt(new_classifications + event + '_tevreden.txt')
    else:
        continue
    # append data
    new_score = [event] + stats_zin + stats_teleurgesteld + stats_tevreden
    new_scores.append(new_score)

event_scores_complete = []
for i, event in enumerate(new_scores):
    anticipointment1 = event[2] + event[7]
    anticipointment2 = event[3] + event[8]
    anticipointment3 = event[4] + event[9]
    anticipointment4 = event[5] + event[10]
    anticifaction1 = event[2] + event[11]
    anticifaction2 = event[3] + event[12]
    anticifaction3 = event[4] + event[13]
    anticifaction4 = event[5] + event[14]
    event_scores_complete.append(event + [anticipointment1, anticipointment2, anticipointment3, anticipointment4,
        anticifaction1, anticifaction2, anticifaction3, anticifaction4])

headers = ['event', '#zin', '0.5 percentile zin', '0.7 percentile zin', '0.8 percentile zin', '0.9 percentile zin', '#teleurgesteld', 
    '0.5 percentile teleurgesteld', '0.7 percentile teleurgesteld', '0.8 percentile teleurgesteld', '0.9 percentile teleurgesteld', 
    '#tevreden', '0.5 percentile tevreden', '0.7 percentile tevreden', '0.8 percentile tevreden', '0.9 percentile tevreden', 
    'anticipointment 0.5', 'anticipointment 0.7', 'anticipointment 0.8', 'anticipointment 0.9', 
    'anticifaction 0.5', 'anticifaction 0.7', 'anticifaction 0.8', 'anticifaction 0.9']
header_style = {'event' : 'general', '#zin' : '0', '0.5 percentile zin' : '0.00', '0.7 percentile zin' : '0.00', 
    '0.8 percentile zin' : '0.00', '0.9 percentile zin' : '0.00', '#teleurgesteld' : '0', '0.5 percentile teleurgesteld' : '0.00', 
    '0.7 percentile teleurgesteld' : '0.00', '0.8 percentile teleurgesteld' : '0.00', '0.9 percentile teleurgesteld' : '0.00', 
    '#tevreden' : '0', '0.5 percentile tevreden' : '0.00', '0.7 percentile tevreden' : '0.00', 
    '0.8 percentile tevreden' : '0.00', '0.9 percentile tevreden' : '0.00', 
    'anticipointment 0.5': '0.00', 'anticipointment 0.7': '0.00', 'anticipointment 0.8' : '0.00', 'anticipointment 0.9' : '0.00',
    'anticifaction 0.5': '0.00', 'anticifaction 0.7' : '0.00', 'anticifaction 0.8' : '0.00', 'anticifaction 0.9' : '0.00'}

lw = linewriter.Linewriter(event_scores_complete)
lw.write_xls(headers, header_style, scores_out)

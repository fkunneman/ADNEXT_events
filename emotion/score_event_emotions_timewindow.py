
import os
import sys

import docreader
import linewriter
import time_functions
import emotion_utils

classificationdir = sys.argv[1]
unique_events_file = sys.argv[2]
timewindow = int(sys.argv[3]) # in days
new_classifications = sys.argv[4]
scores_out = sys.argv[5]

classifications = os.listdir(classificationdir)
events = list(set([x.split('_')[0] for x in classifications]))
with open(unique_events_file) as ue:
    unique_events = ue.read().split('\n')

new_scores = []
for event in events:
    if event in unique_events:
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
        zin_scores = [[float(tweet[0]), tweet[1]] for tweet in zin_tweets[1:]]
        if len(zin_scores) < 50:
            continue
        # teleurgesteld
        try:
            dr_teleurgesteld = docreader.Docreader()
            dr_teleurgesteld.parse_doc(classificationdir + event + '_teleurgesteld.txt')
        except:
            continue
        teleurgesteld_tweets = [dr_teleurgesteld.lines[0]]
        for tweet in dr_teleurgesteld.lines[1:]:
            tweet_date = time_functions.return_datetime(tweet[4], setting = 'vs')
            if (tweet_date - event_date).days <= timewindow:
                teleurgesteld_tweets.append(tweet)
        teleurgesteld_scores = [[float(tweet[0]), tweet[1]] for tweet in teleurgesteld_tweets[1:]]
        if len(teleurgesteld_scores) < 50:
            continue
        # tevreden
        try:
            dr_tevreden = docreader.Docreader()
            dr_tevreden.parse_doc(classificationdir + event + '_tevreden.txt')
        except:
            continue
        tevreden_tweets = [dr_tevreden.lines[0]]
        for tweet in dr_tevreden.lines[1:]:
            tweet_date = time_functions.return_datetime(tweet[4], setting = 'vs')
            if (tweet_date - event_date).days <= timewindow:
                tevreden_tweets.append(tweet)
        tevreden_scores = [[float(tweet[0]), tweet[1]] for tweet in tevreden_tweets[1:]]
        # append data
        stats_zin = emotion_utils.calculate_event_emotion_stats(zin_scores, 'zin')
        lw = linewriter.Linewriter(zin_tweets)
        lw.write_txt(new_classifications + event + '_zin.txt')
        stats_teleurgesteld = emotion_utils.calculate_event_emotion_stats(teleurgesteld_scores, 'teleurgesteld')
        lw = linewriter.Linewriter(teleurgesteld_tweets)
        lw.write_txt(new_classifications + event + '_teleurgesteld.txt')
        stats_tevreden = emotion_utils.calculate_event_emotion_stats(tevreden_scores, 'tevreden')
        lw = linewriter.Linewriter(tevreden_tweets)
        lw.write_txt(new_classifications + event + '_tevreden.txt')
        new_score = [event] + stats_zin + stats_teleurgesteld + stats_tevreden[1:]
        new_scores.append(new_score)

headers = ['event', '#before', 'Percent zin', 'Average zin', '0.5 percentile zin', '0.7 percentile zin', 
    '0.8 percentile zin', '0.9 percentile zin', '#after', 'Percent teleurgesteld', 'Average teleurgesteld', 
    '0.5 percentile teleurgesteld', '0.7 percentile teleurgesteld', '0.8 percentile teleurgesteld', 
    '0.9 percentile teleurgesteld', 'Percent tevreden', 'Average tevreden', '0.5 percentile tevreden', 
    '0.7 percentile tevreden', '0.8 percentile tevreden', '0.9 percentile tevreden']
header_style = {'event' : 'general', '#before' : '0', 'Percent zin' : '0.00', 'Average zin' : '0.00', 
    '0.5 percentile zin' : '0.00', '0.7 percentile zin' : '0.00', '0.8 percentile zin' : '0.00', 
    '0.9 percentile zin' : '0.00', '#after' : '0', 'Percent teleurgesteld' : '0.00', 
    'Average teleurgesteld' : '0.00','0.5 percentile teleurgesteld' : '0.00', 
    '0.7 percentile teleurgesteld' : '0.00', '0.8 percentile teleurgesteld' : '0.00', 
    '0.9 percentile teleurgesteld' : '0.00', 'Percent tevreden' : '0.00', 'Average tevreden' : '0.00', 
    '0.5 percentile tevreden' : '0.00', '0.7 percentile tevreden' : '0.00', '0.8 percentile tevreden' : '0.00', 
    '0.9 percentile tevreden' : '0.00'}

lw = linewriter.Linewriter(new_scores)
lw.write_xls(headers, header_style, scores_out)

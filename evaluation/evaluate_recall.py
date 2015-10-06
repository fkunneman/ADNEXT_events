
import sys
import os
import datetime
import re
import os
from collections import defaultdict

import time_functions
import coco

fgs = sys.argv[1] # gold standard
fee = sys.argv[2] # extracted events
of = sys.argv[3] # outfile
tmpdir = sys.argv[4]
twma = int(sys.argv[5])
tfs = sys.argv[6:] # stream of tweets

# 1: read in gold standard --> sorted event term - time
print('Reading gold standard file')
gold_standard_events = []
gold_standard_events_hashtag = []
gold_standard = []
with open(fgs, encoding = 'utf-8') as gs:
    for line in gs.readlines():
        event_date = line.strip().split('\t')
        try:
            event_date[1] = time_functions.return_datetime(event_date[1])
            event_date[0] = event_date[0].lower()
        except:
            d = event_date[0]
            e = event_date[1]
            event_date[1] = time_functions.return_datetime(d)
            event_date[0] = e.lower()
        if event_date[0] not in gold_standard_events:
            gold_standard.append(event_date)
            gold_standard_events.append(event_date[0])
            event_hashtag = '#' + ''.join(event_date[0].split())
            gold_standard_events_hashtag.append(event_hashtag)
gold_standard = sorted(gold_standard, key = lambda k : k[1])
#for event in gold_standard_events:
#    sys.stdout.buffer.write(event.encode('utf8'))
#    print(' ', event[1])

with open(of[:-4] + '_counts.txt', 'w', encoding = 'utf-8') as outfile:
    for month in ['08', '09', '10', '11', '12']:
        print(gold_standard[1][1], str(gold_standard[1][1])[5:7])
        count = len([x for x in gold_standard if str(x[1])[5:7] == month])
        outfile.write(month + '\t' + str(count) + '\n')
    total = len(gold_standard)
    outfile.write('total\t' + str(total) + '\n')

# 2: read in extracted events --> sorted event terms, time
print('Reading extracted events file')
extracted_events = []
with open(fee, encoding = 'utf-8') as ee:
    for line in ee.readlines():
        date_event = line.strip().split('\t')
        event_date = [date_event[1].split(', '), time_functions.return_datetime(date_event[0], setting = 'vs')]
        extracted_events.append(event_date)
extracted_events = sorted(extracted_events, key = lambda k : k[1])

print('Finding matches for extracted events file')
# match extracted events with gold standard
matches = []
non_matches = []
for event_date in extracted_events:
    event_terms = event_date[0]
    match = False
    event_terms_str = ', '.join(event_date[0])
    for event_term in event_terms:
        if event_term[0] == '#':
            if event_term in gold_standard_events_hashtag:
                matches.append(event_terms_str)
                match = True
                break
        else:
            parts = event_term.split(' ')
#            print(event_term, parts)
            et = [event_term]
            for l in range(2, len(parts)):
                if l == 2:
                    et.extend([' '.join(x) for x in zip(parts, parts[1:])])
                elif l == 3:
                    et.extend([' '.join(x) for x in zip(parts, parts[1:], parts[2:])])
                elif l == 4:
                    et.extend([' '.join(x) for x in zip(parts, parts[1:], parts[2:], parts[3:])])
                elif l == 5:
                    et.extend([' '.join(x) for x in zip(parts, parts[1:], parts[2:], parts[3:], parts[4:])])
            for part in et:
                for ev in gold_standard:
#                    print(part, ev, ev[0].split())
                    if re.match(part, ev[0]) or part in ev[0].split():
                        print("MATCH")
                        matches.append((event_terms_str, ev[0], str(ev[1].date())))
                        match = True
                        #break
                #if match:
                #    break
            #if match:
            #    break
    if not match:
        #print(event_terms_str)
        non_matches.append(event_terms_str)

with open(of[:-4] + '_matches.txt', 'w', encoding = 'utf-8') as outfile:
    outfile.write('\n'.join(['\t-\t'.join(x) for x in matches]))

with open(of[:-4] + '_non-matches.txt', 'w', encoding = 'utf-8') as outfile:
    outfile.write('\n'.join(['\t'.join(x) for x in non_matches]))


if twma:
    # 3: read in tweets

    current_tmpfiles = os.listdir(tmpdir)
    cc = coco.Coco(tmpdir)
    if 'ngrams.txt' in current_tmpfiles:
        cc.load_file(tmpdir + 'ngrams.txt')
    else:
        print('Reading tweet files')
        tweets = []
        for tweetfile in tfs:
            with open(tweetfile, encoding = 'utf-8') as tf:
                for tweet in tf.readlines()[1:]:
                    columns = tweet.strip().split('\t')
                    tweets.append(columns[-1])
        cc.set_lines(tweets)
        cc.simple_tokenize()
        cc.set_file()

    if 'ngrams.IndexedPatternModel_constrained' in current_tmpfiles:
        cc.load_model(tmpdir + 'ngrams.IndexedPatternModel')
    else:
        # clsfile = tmpdir + 'ngrams.colibri.cls' if 'ngrams.colibri.cls' in current_tmpfiles else False
        # datfile = tmpdir + 'ngrams.colibri.dat' if 'ngrams.colibri.cat' in current_tmpfiles else False
        cc.model_ngramperline(gold_standard_events)

    matches = cc.match(gold_standard_events)

    print('Writing to file')
    with open(of[:-4] + '_tweetmatches.txt', 'w', encoding = 'utf-8') as outfile:
        for event in gold_standard:
            if matches[event[0]][0] > 0:
                found_tweets = [tweets[i] for i in matches[event[0]][1]]
            else:
                found_tweets = []
            outfile.write(event[0] + '\t' + str(event[1].date()) + '\t' + str(matches[event[0]][0]) + '\t' + '-----'.join(found_tweets) + '\n')


import sys
import datetime
import re

import time_functions

fgs = sys.argv[1] # gold standard
fee = sys.argv[2] # extracted events
of = sys.argv[3] # outfile
#tfs = sys.argv[4:] # stream of tweets

# 1: read in gold standard --> sorted event term - time
print('Reading gold standard file')
gold_standard_events = []
gold_standard_events_hashtag = []
gold_standard = []
with open(fgs, encoding = 'utf-8') as gs:
    for line in gs.readlines():
        event_date = line.strip().split('\t')
        #print(event_date)
        event_date[1] = time_functions.return_datetime(event_date[1])
        if event_date[0] not in gold_standard_events:
            gold_standard.append(event_date)
            gold_standard_events.append(event_date[0])
            event_hashtag = '#' + ''.join(event_date[0].split())
            gold_standard_events_hashtag.append(event_hashtag)
gold_standard = sorted(gold_standard, key = lambda k : k[1])
#for event in gold_standard_events:
#    sys.stdout.buffer.write(event.encode('utf8'))
#    print(' ', event[1])
    
# 2: read in extracted events --> sorted event terms, time
print('Reading extracted events file')
extracted_events = []
with open(fee, encoding = 'utf-8') as ee:
    for line in ee.readlines():
        date_event = line.strip().split('\t')
        event_date = [date_event[1].split(', '), time_functions.return_datetime(date_event[0], setting = 'vs')]
        extracted_events.append(event_date)
extracted_events = sorted(extracted_events, key = lambda k : k[1])

# 3: read in tweets
#print('Reading tweet files')
#tweets = []
#for tweetfile in tfs:
#    with open(tweetfile, encoding = 'utf-8') as tf:
#        for tweet in tf.readlines()[1:]:
#            columns = tweet.strip().split('\t')
#            tweets.append(columns[-1])

# match extracted events with gold standard
matches = []
non_matches = []
for event_date in extracted_events:
    event_terms = event_date[0]
    match = False
    event_terms_str = ', '.join(event_date[0])
#    print(et)
    for event_term in event_terms:
  #          print(event_terms)
  #      except:
  #          continue
        if event_term[0] == '#':
 #           try:
 #               print('match', event_term)
 #           except:
 #               continue
            if event_term in gold_standard_events_hashtag:
                matches.append(event_terms_str)
                match = True
                break
        else:
            parts = event_term.split(' ')
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
  #      try:
            for part in et:
#                try:
#                    print('match', part)
#                except:
#                    continue
                for ev in gold_standard:
                    if re.match(part, ev[0]) or part in ev[0].split():
                        matches.append((event_terms_str, ev[0], str(ev[1].date())))
                        match = True
                        break
                if match:
                    break
            if match:
                break
    if not match:
        non_matches.append(event_terms_str)

with open(of[:-4] + '_matches.txt', 'w', encoding = 'utf-8') as outfile:
    outfile.write('\n'.join(['\t-\t'.join(x) for x in matches]))

with open(of[:-4] + '_non-matches.txt', 'w', encoding = 'utf-8') as outfile:
    outfile.write('\n'.join(['\t'.join(x) for x in non_matches]))

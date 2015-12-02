
import sys
import os
import datetime

import time_functions # from ADNEXT_utils

tweetsdir = sys.argv[1] # directory with event tweets
sequencedir = sys.argv[2] # directory with event sequence information
beforedir = sys.argv[3] # directory to write before tweets to
duringdir = sys.argv[4] # directory to write during tweets to
afterdir = sys.argv[5] # directory to write after tweets to

tweets_files = [tf for tf in os.listdir(tweetsdir) if tf[:6] == 'tweets' and tf[-4:] == '.txt']
sequence_files = [sf for sf in os.listdir(sequencedir) if sf[:9] == 'sequence_']
before_files = os.listdir(beforedir)
during_files = os.listdir(duringdir)
after_files = os.listdir(afterdir)

id_sequence_file = {}
for sf in sequence_files:
    event_id = sf[9:-4]
    id_sequence_file[event_id] = sf

#TODO parrallel

for i, tweets_file in enumerate(tweets_files):
    print(tweets_file)
    # check for existense in dirs
    if tweets_file in before_files or tweets_file in during_files or tweets_file in after_files:
        print('Already processed')
        continue
    event_id = tweets_file[7:-4]
    # extract eventdate
    sequence_file = id_sequence_file[event_id]
    with open(sequencedir + sequence_file, 'r', encoding = 'utf-8') as sf_open:
        infoline = sf_open.readlines()[0]
        event_date = time_functions.return_datetime(infoline.split('\t')[1], setting = 'vs')
    event_date_begin = datetime.datetime.combine(event_date, datetime.time(0,0))
    event_date_end = datetime.datetime.combine(event_date, datetime.time(23,59))
    # collect tweets
    with open(tweetsdir + tweets_file, 'r', encoding = 'utf-8') as tweets_in:
        tweets = [tweet.split('\t') for tweet in tweets_in.readlines()]
    # distinguish before during after
    before, during, after = time_functions.select_tweets_bda(tweets, date_index = 3, 
        time_index = 4, during_begin = event_date_begin, during_end = event_date_end, setting = 'vs')
    # write to files
    with open(beforedir + tweets_file, 'w', encoding = 'utf-8') as before_out:
        before_out.write(''.join(['\t'.join(tweet) for tweet in before]))
    with open(duringdir + tweets_file, 'w', encoding = 'utf-8') as during_out:
        during_out.write(''.join(['\t'.join(tweet) for tweet in during]))
    with open(afterdir + tweets_file, 'w', encoding = 'utf-8') as after_out:
        after_out.write(''.join(['\t'.join(tweet) for tweet in after]))
    if i == 100:
        quit()

        


import sys
import os
import datetime
import multiprocessing

import time_functions
import calculations

tweetdir = sys.argv[1]
eventdir = sys.argv[2]
eventfiles = sys.argv[3:]

statfiles = os.listdir(tweetdir)
writtenfiles = [x for x in os.listdir(eventdir) if x[-4:] == '.txt']
written_ids = [x[7:-4] for x in writtenfiles]

def collect_tweets(ets, stat_cds, q, r):
    for statfile, cursor_date in stat_cds:
        if set([statfile]) & set(statfiles):
            with open(tweetdir + statfile, 'r', encoding = 'utf-8') as stat_in:
                stats = [line.split('\t') for line in stat_in.read().split('\n')]
                terms = [line[0] for line in stats]
            tweetsfile = tweetdir + str(cursor_date.year) + month + day + '_tweets_cleaned_good.txt'
            with open(tweetsfile, 'r', encoding = 'utf-8') as tweets_in:
                tweets = tweets_in.read().split('\n')
            tweets_out = []
            for event_term in ets:
                try:
                    term_index = terms.index(event_term)
                    term_stats = stats[term_index]
                    tweet_segment = tweets[int(term_stats[2]):int(term_stats[3])]
                    for tweet in tweet_segment:
                        q.put(event_term + '\t' + tweet + '\n')
                except ValueError:
                    print(event_term.encode('utf-8'), 'not in list for event', event_id,'on date',str(cursor_date.date())) 
                    continue
        else:
            print('no existing file', statfile)
        r.put(statfile)

for eventfile in eventfiles:
    if eventfile[9:-4] in written_ids:
        print(eventfile, 'already processed')
        continue
    else:
        q = multiprocessing.Queue()
        r = multiprocessing.Queue()
        print(eventfile)
        event_tweets = []
        event_id = eventfile.split('_')[1][:-4]
        with open(datadir + eventfile, 'r', encoding = 'utf-8') as sequence_in:
            lines = sequence_in.read().strip().split('\n')
        event = lines[0]
        tokens = event.split('\t')
        event_terms = tokens[0].split(', ')
        event_date = time_functions.return_datetime(tokens[1], setting = 'vs')
        date_begin = time_functions.return_datetime(tokens[2][:10], setting = 'vs')
        date_end = time_functions.return_datetime(tokens[2][11:], setting = 'vs')
        # collect_tweets
        outtweets = eventdir + 'tweets_' + event_id + '.txt'
        cursor_date = date_begin
        stat_date = []
        while cursor_date <= date_end:
            month = '0' + str(cursor_date.month) if len(str(cursor_date.month)) == 1 else str(cursor_date.month) 
            day = '0' + str(cursor_date.day) if len(str(cursor_date.day)) == 1 else str(cursor_date.day) 
            statfile = str(cursor_date.year) + month + day + '_eventstats.txt'
            cursor_date = cursor_date + datetime.timedelta(days = 1)
            stat_date.append([statfile, cursordate])
        step = int(len(stat_date) / 12)
        for i in range(12):
            if i == 11:
                sds = stat_date[i:]
            else:
                sds = stat_date[i:i+step]
            p = multiprocessing.Process(target = collect_tweets, args = [event_terms, sds, q, r])
            p.start()
        t_out = open(outtweets, 'w', encoding = 'utf-8') 
        sfco = []
        while True:
            tweet = q.get()
            t_out.write(tweet)
            stat = r.get()
            sfco.append(stat)
            print(len(sfco), 'statfiles of', len(stat_date), 'collected')
            if len(sfco) == len(stat_date):
                break

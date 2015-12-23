
import sys
import os
import datetime

import time_functions
import calculations

datadir = sys.argv[1]
tweetdir = sys.argv[2]
eventdir = sys.argv[3]

def collect_tweets_statfiles(event_term, date):
    pass

all_eventfiles = [x for x in os.listdir(datadir) if x[:8] == 'sequence']
all_events = [x[9:-4] for x in all_eventfiles]

statfiles = os.listdir(tweetdir)
writtenfiles = [x for x in os.listdir(eventdir) if x[-4:] == '.txt']

all_written = [x[7:-4] for x in writtenfiles]
non_written = sorted(list(set(all_events) - set(all_written)))
print(len(all_events), len(all_written), len(non_written))

for event in non_written:
    print(event)
    terms_burstiness = []
    event_tweets = []
    event_id = eventfile.split('_')[1][:-4]
    with open(datadir + eventfile, 'r', encoding = 'utf-8') as sequence_in:
        lines = sequence_in.read().strip().split('\n')
    event = lines[0]
    tokens = event.split('\t')
    event_terms = tokens[0].split(', ')
    if len(event_terms) > 1:
        event_date = time_functions.return_datetime(tokens[1], setting = 'vs')
        date_begin = time_functions.return_datetime(tokens[2][:10], setting = 'vs')
        date_end = time_functions.return_datetime(tokens[2][11:], setting = 'vs')
        position = (event_date - date_begin).days
        
        for event_term in event_terms:

        print('calculating burstiness')
        combis = [event_terms]
        if len(event_terms) > 2:
            for i in range(2, len(event_terms)):
                for combi in (list(itertools.combinations(event_terms, i))):
                    combis.append(list(combi))
        for combi in combis: # combine
            combi_sets = []
            for et in combi:
                combi_sets.append(set(event_term_ids[et]))
            overlap = set.intersection(*combi_sets)
            print(','.join(combi).encode('utf-8'), overlap)
            overlap_timedict = defaultdict(int)
            for tid in list(overlap):
                overlap_timedict[str(id_date[tid].date())] += 1
            timelist = dict2list(overlap_timedict)
            combi_timelist[', '.join(list(combi))] = timelist
            # calculate burstiness
            combi_burst = []
            for combi in combi_timelist.keys():
                burstiscore = score_burstiness(combi_timelist[combi], position)
                if combi_timelist[combi][position] > 9:
                    combi_burst.append([combi, burstiscore, position])
            combi_burst_sorted = sorted(combi_burst, key = lambda k : k[1], reverse = True)
            for combi in combi_burst_sorted:
                event_bursti_scores[event].append(combi[0] + ' - ' + str(combi[1]) + ' - ' + \
                    str(combi_timelist[combi[0]][position]) + ' - ' + \
                    ','.join([str(x) for x in combi_timelist[combi[0]]]))





        for termsequence in lines[1:]:
            tokens = termsequence.split('\t')
            event_term = tokens[0]
            sequence = [int(x) for x in tokens[1].split()]
            burstiness = calculations.score_burstiness_sequence(sequence, position)
            term_burstiness.append([event_term] + burstiness + [position, sequence])
        ranked_burstiness = sorted(term_burstiness, key = lambda k : k[1], reverse = True)
        selected_terms = []
        for event_term in ranked_burstiness:
            if event_term[1] >= 10 and event_term[2] >= 20:
                selected_terms.append(event_term[0])
            else:
                break
        if len(selected_terms) > 0:
            print('collecting tweets')
            with open(selected_events_file, 'a', encoding = 'utf-8') as selected_out:
                selected_out.write(event_id + '\n')
            # collect_tweets
            outtweets = eventdir + 'tweets_' + event_id + '.txt'
            cursor_date = date_begin
            while cursor_date <= date_end:
                month = '0' + str(cursor_date.month) if len(str(cursor_date.month)) == 1 else str(cursor_date.month) 
                day = '0' + str(cursor_date.day) if len(str(cursor_date.day)) == 1 else str(cursor_date.day) 
                statfile = str(cursor_date.year) + month + day + '_eventstats.txt'
                if statfile in statfiles:
                    with open(tweetdir + statfile, 'r', encoding = 'utf-8') as stat_in:
                        stats = [line.split('\t') for line in stat_in.read().split('\n')]
                        terms = [line[0] for line in stats]
                    tweetsfile = tweetdir + str(cursor_date.year) + month + day + '_tweets_cleaned_good.txt'
                    with open(tweetsfile, 'r', encoding = 'utf-8') as tweets_in:
                        tweets = tweets_in.read().split('\n')
                    with open(outtweets, 'a', encoding = 'utf-8') as tweets_out:
                        printed_ids = set()
                        for event_term in selected_terms:
                            try:
                                term_index = terms.index(event_term)
                                term_stats = stats[term_index]
                                tweet_segment = tweets[int(term_stats[2]):int(term_stats[3])]
                                for tweet in tweet_segment:
                                    tid = tweet.split('\t')[0]
                                    if tid in printed_ids:
                                        continue
                                    else:
                                        printed_ids.add(tid)
                                        tweets_out.write(tweet + '\n')
                            except ValueError:
                                print(event_term.encode('utf-8'), 'not in list for event', event_id,'on date',str(cursor_date.date())) 
                                continue
                else:
                    print('no existing file', statfile)
                cursor_date = cursor_date + datetime.timedelta(days = 1) 

    else:
        with open(discarded_events_file, 'a', encoding = 'utf-8') as discarded_out:
            discarded_out.write(event_id + '\n')


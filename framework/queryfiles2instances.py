
import sys
import datetime

events = sys.argv[1]
periodicities = sys.argv[2]
stats = sys.argv[3:] # first half stats, second half tweets

event_date = {}
event_terms = defaultdict(list)
term_date_tweets = defaultdict(lambda : defaultdict(list))
term_date_freq = defaultdict(lambda : {})

with open(events, 'r', encoding = 'utf-8') as events_open:
    for line in events_open.readlines():
        tokens = line.strip().split('\t')
        date = datetime.date(int(tokens[0][:4]), int(tokens[0][5:7]), int(tokens[0][8:]))
        event = tokens[1]
        term = tokens[2]
        event_date[event] = date
        event_terms[event].append(term)

# half = len(stats_tweets) / 2
# statfiles = stats_tweets[:half]
# tweetfiles = stats_tweets[half:]

for statfile in enumerate(stats):
    # with open(tweetfiles[i], 'r', encoding = 'utf-8') as tweet_in:
    #     tweets = tweet_in.readlines()
    with open(statfile, 'r', encoding = 'utf-8') as stat_in:
        for line in stat_in.readlines():
            tokens = line.strip().split('\t')
            event_term = tokens[0]
            count = tokens[1]
            begin = tokens[2]
            end = tokens[3]
            statdate = datetime.date(int(statfile[:4]), int(statfile[4:6]), int(statfile[6:8]))
            # add event-date frequency
            term_date_freq[event_term][statdate] = int(count)
            # add event-date tweets
            #term_tweets = [x.strip() for x in tweets[begin:end]]
            term_date_tweets[event_term][statdate] = [begin, end]

lines = []
for event in event_terms.keys():
    terms = event_terms[event]
    # identify date window
    date = event_date[event]
    range_end = date + datetime.timedelta(days = 30)
    range_begin = date - datetime.timedelta(days = 30)
    for term in terms:
        line = [event, term]
        cursor_date = range_begin
        while cursor_date <= range_end:
            try:
                stats = term_date_freq[term][cursor_date]
                entry = [str(cursor_date), str(stats)]
                entry.extend(term_date_tweets[term][cursor_date])
                line.append(entry)
            except KeyError:
                print('No input for', term, cursor_date)
        print(line)
        lines.append(line)

print(len(lines))

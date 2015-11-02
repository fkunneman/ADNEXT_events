
import sys
import os
from collections import defaultdict

import query_tweets_json

queryfile = sys.argv[1]
outdir = sys.argv[2]
filedir = sys.argv[3]
tmpdir = sys.argv[4]

def date2twiqsfiles(d):
    files = []
    for hour in range(24):
       h = '0' + str(hour) if hour < 10 else str(hour)
       files.append(outdir + d + '-' + h + '.out')
    return files

with open(queryfile, 'r', encoding = 'utf-8') as infile:
    querylines = infile.readlines()

for line in querylines:
    tokens = line.strip().split('\t')
    if tokens[0] == '20150423':
        datefiles = date2twiqsfiles(tokens[0])
        print(tokens[0])
        terms = tokens[1].split(', ')
        tweetmatches = defaultdict(list)
        for df in datefiles:
            print(df)
            if os.path.isfile(df):            
                matches = query_tweets_json.query_event_terms_json(df, terms, tmpdir)
                for m in matches.keys():
                    tweetmatches[m].extend(matches[m])
        tweetout = outdir + tokens[0] + '_tweets.txt'
        eventstats = []
        with open(tweetout, 'w', encoding = 'utf-8') as tout:
            c = 0
            for eventterm in tweetmatches.keys():
                tweets = tweetmatches[eventterm]
                tout.write('\n'.join(tweets) + '\n')
                l = len(tweets)
                eventstats.append([eventterm, str(l), str(c), str(c + l)])
                c += l
        eventout = outdir + tokens[0] + '_eventstats.txt'
        with open(eventout, 'w', encoding = 'utf-8') as eout:
            for stat in eventstats:
                eout.write('\t'.join(stat) + '\n')

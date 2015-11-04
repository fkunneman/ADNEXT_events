
import sys
import os
from collections import defaultdict

import query_tweets_json
import json_tweets_parser
import linewriter

queryfile = sys.argv[1]
outdir = sys.argv[2]
tmpdir = sys.argv[3]

def date2twiqsfiles(d): 
    files = []
    year = d[:4]
    month = d[4:6]
    day = d[6:]
    path = 'twitter/' + year + '/' + month + '/' + day + '/' + d + '-'
    for hour in range(24):
       h = '0' + str(hour) if hour < 10 else str(hour)
       files.append(path + h + '.out.gz')
    return files

with open(queryfile, 'r', encoding = 'utf-8') as infile:
    querylines = infile.readlines()

for line in querylines:
    tokens = line.strip().split('\t')
    datefiles = date2twiqsfiles(tokens[0])
    print(tokens[0])
    terms = tokens[1].split(', ')
    tweetmatches = defaultdict(list)
    #path = False
    for df in datefiles:
        dfuz = df[:-3]
        os.system('hadoop fs -cat ' + df + ' | gunzip -c > ' + dfuz)
        #path = True
        matches = query_tweets_json.query_event_terms_json(dfuz, terms, tmpdir)
        for m in matches.keys():
            tweetmatches[m].extend(matches[m])
        os.system('rm ' + dfuz)
        # else:
        #     print('file not found:', df)
    # if path:
    tweetout_json = outdir + tokens[0] + '_tweets.json'
    tweetout_txt = outdir + tokens[0] + '_tweets.txt'
    eventstats = []
    with open(tweetout_json, 'w', encoding = 'utf-8') as tout:
        c = 0
        non_terms = list(set(terms) - set(tweetmatches.keys()))
        for term in non_terms:
            eventstats.append([term, '0', '0', '0'])
        for eventterm in tweetmatches.keys():
            tweets = tweetmatches[eventterm]
            tout.write('\n'.join(tweets) + '\n')
            l = len(tweets)
            eventstats.append([eventterm, str(l), str(c), str(c + l)])
            c += l
    # convert json to txt 
    jtp = json_tweets_parser.json_tweets_parser(tweetout_json)
    jtp.parse()
    jtp.convert()
    lw = linewriter.Linewriter(jtp.lines)
    lw.write_txt(tweetout_txt)
    os.system('rm ' + tweetout_json)
    os.system('gzip ' + tweetout_txt)
    eventout = outdir + tokens[0] + '_eventstats.txt'
    with open(eventout, 'w', encoding = 'utf-8') as eout:
        for stat in eventstats:
            eout.write('\t'.join(stat) + '\n')

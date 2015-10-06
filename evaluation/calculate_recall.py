
import sys

gsf = sys.argv[1]
eem = sys.argv[2]
tm = sys.argv[3]
#out = sys.argv[4]
#months = int(sys.argv[5])

# 1: collect num gold standard
with open(gsf, encoding = 'utf-8') as gsfo:
    gold_standard = gsfo.read().split('\n')    
num_gold_standard = len(gold_standard)

# 2: collect num event extraction
with open(eem, encoding = 'utf-8') as eemo:
    extracted_events = eemo.read().split('\n')

# 3: collect num tweet matching
with open(tm, encoding = 'utf-8') as tmo:
    tweet_all = tmo.read().split('\n')
tweet_matches = []
for x in tweet_all:
    if len(x.split('\t')) >= 3:
        if x.split('\t')[2] != '0':
            tweet_matches.append(x)

# 4: make calculations and output result- and plotfile 
matched = len(extracted_events) / num_gold_standard
matched_tweets = len(tweet_matches) / num_gold_standard
matched_tweets_threshold = [x for x in tweet_matches if int(x.split('\t')[2]) >= 5]
matched_tweets_threshold_score = len(matched_tweets_threshold) / num_gold_standard
percentage_tweets = len(extracted_events) / len(tweet_matches)
percentage_tweets_threshold = len(extracted_events) / len(matched_tweets_threshold)

print(num_gold_standard, len(tweet_matches), matched_tweets, len(matched_tweets_threshold),
    matched_tweets_threshold_score, len(extracted_events), matched, matched_tweets, 
    percentage_tweets, percentage_tweets_threshold)


import sys

import time_functions
import dutch_timex_extractor

test_tweets = sys.argv[1]

with open(test_tweets, 'r', encoding = 'utf-8') as test_in:
    tweets = test_in.readlines()

for tweet in tweets:
    tokens = tweet.strip().split('\t')
    try:
        date = time_functions.return_datetime(tokens[0], setting = 'vs')
    except:
        print('except:', tokens[0])
        continue
    text = tokens[1]
    dte = dutch_timex_extractor.Dutch_timex_extractor(text, date)
    #dte.extract_date()
    dte.extract_timeunit()    
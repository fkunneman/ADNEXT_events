
import sys

import time_functions
import dutch_timex_extractor
import commonness
import entity_extractor

test_tweets = sys.argv[1]
commonness_txt = sys.argv[2]
commonness_cls = sys.argv[3]
commonness_corpus = sys.argv[4]
ngrams_score = sys.argv[5]

with open(test_tweets, 'r', encoding = 'utf-8') as test_in:
    tweets = test_in.readlines()

cs = commonness.Commonness()
cs.set_classencoder(commonness_txt, commonness_cls, commonness_corpus)
cs.set_dmodel(ngrams_score)

for tweet in tweets:
    tokens = tweet.strip().split('\t')
    try:
        date = time_functions.return_datetime(tokens[0], setting = 'vs')
    except:
        print('except:', tokens[0])
        continue
    text = tokens[1].lower()
    dte = dutch_timex_extractor.Dutch_timex_extractor(text, date)
    dte.extract_refdates()
    if len(dte.refdates) > 0:
        ee = entity_extractor.EntityExtractor(cs)
         


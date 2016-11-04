
import sys

import time_functions
import dutch_timex_extractor
import commonness
import helpers
import entity_extractor
import ucto

test_tweets = sys.argv[1]
commonness_txt = sys.argv[2]
commonness_cls = sys.argv[3]
commonness_corpus = sys.argv[4]
ngrams_score = sys.argv[5]

with open(test_tweets, 'r', encoding = 'utf-8') as test_in:
    tweets = test_in.readlines()

tokenizer = ucto.Tokenizer('/vol/customopt/lamachine/etc/ucto/tokconfig-nl-twitter')

print('setting commonness object')
cs = commonness.Commonness()
cs.set_classencoder(commonness_txt, commonness_cls, commonness_corpus)
cs.set_dmodel(ngrams_score)

for tweet in tweets[1:]:
    tokens = tweet.strip().split('\t')
    try:
        date = time_functions.return_datetime(tokens[2], setting = 'vs')
    except:
        print('except:', tokens[0])
        continue
    tokenizer.process(tokens[7])
    text = ' '.join([token.text for token in tokenizer if not token.tokentype == 'PUNCTUATION'])
    text_lower = text.lower()
    dte = dutch_timex_extractor.Dutch_timex_extractor(text_lower, date)
    dte.extract_refdates()
    if len(dte.refdates) > 0:
        dte.filter_future_refdates()
        if len(dte.refdates) > 0:
            print(dte.refdates)
            datestrings = [obj[0] for obj in dte.refdates]
            tweet_chunks = helpers.remove_pattern_from_string(text_lower,datestrings)
            print(text_lower.encode('utf-8'),'\t'.join(tweet_chunks).encode('utf-8'))
            ee = entity_extractor.EntityExtractor(cs)
            ee.extract_entities_strings(tweet_chunks)
            ee.filter_entities_threshold()
            print(', '.join([x[0] for x in ee.entities]).encode('utf-8'))

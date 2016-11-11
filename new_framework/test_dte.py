
import sys
import json

import ucto

import time_functions
import dutch_timex_extractor
import commonness
import helpers
import entity_extractor
from tweet import Tweet
from event_ranker import EventRanker


commonness_txt = sys.argv[1]
commonness_cls = sys.argv[2]
commonness_corpus = sys.argv[3]
ngrams_score = sys.argv[4]
test_tweets = sys.argv[5:]

tweets = []
for ttf in test_tweets:
    print('reading',ttf)
    with open(ttf, 'r', encoding = 'utf-8') as test_in:
        tweets.extend(test_in.readlines()[1:])
print('Imported', len(tweets), 'tweets')

tokenizer = ucto.Tokenizer('/vol/customopt/lamachine/etc/ucto/tokconfig-nl-twitter')

#print('setting commonness object')
#cs = commonness.Commonness()
#cs.set_classencoder(commonness_txt, commonness_cls, commonness_corpus)
#cs.set_dmodel(ngrams_score)

tweetobjs = []
for tweet in tweets:
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
    tdict = {'id':tokens[1], 'user':tokens[6], 'datetime':date, 'text':text_lower}
    tweetobj = Tweet(tdict)
    if len(dte.refdates) > 0:
        dte.filter_future_refdates()
    tweetobj.set_refdates(dte.refdates)
    # if len(tweetobj.refdates) > 0:
    print(dte.refdates)
    datestrings = [obj[0] for obj in dte.refdates]
    tweet_chunks = helpers.remove_pattern_from_string(text_lower,datestrings)
    print(text_lower.encode('utf-8'),'\t'.join(tweet_chunks).encode('utf-8'))
    ee = entity_extractor.EntityExtractor()
    for chunk in tweet_chunks:
        tokens = chunk.split()
        #ee.extract_entities(tokens)
        ee.extract_entities_hashtag(tokens)
#    ee.filter_entities_threshold()
    tweetobj.set_entities(ee.entities)
#    print(', '.join([x[0] for x in ee.entities]).encode('utf-8'))
    tweetobjs.append(tweetobj)

er = EventRanker(tweetobjs)
events = er.extract_events()
for i,event in events[:100]:
    print(i, '\n', event.return_dict().encode('utf-8'))

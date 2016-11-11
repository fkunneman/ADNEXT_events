
import sys
import json

import ucto

import time_functions
from functions import dutch_timex_extractor
from classes import commonness
from functions import helpers
from functions import entity_extractor
from classes.tweet import Tweet
from functions.event_ranker import EventRanker


outfile = sys.argv[1]
commonness_txt = sys.argv[2]
commonness_cls = sys.argv[3]
commonness_corpus = sys.argv[4]
ngrams_score = sys.argv[5]
test_tweets = sys.argv[6:]

tweets = []
for ttf in test_tweets:
    print('reading',ttf)
    with open(ttf, 'r', encoding = 'utf-8') as test_in:
        tweets.extend(test_in.readlines()[1:])
print('Imported', len(tweets), 'tweets')

tokenizer = ucto.Tokenizer('/vol/customopt/lamachine/etc/ucto/tokconfig-nl-twitter')

print('setting commonness object', commonness_txt, commonness_cls, commonness_corpus, ngrams_score)
cs = commonness.Commonness()
cs.set_classencoder(commonness_txt, commonness_cls, commonness_corpus)
cs.set_dmodel(ngrams_score)

tweetobjs = []
check = range(0,len(tweets),10000)
for i,tweet in enumerate(tweets):
    if i in check:
        print('processed',i,'tweets')
    tokens = tweet.strip().split('\t')
#    try:
#    date = time_functions.return_datetime(tokens[2], setting = 'vs')
#    except:
#        print('except:', tokens[0])
#        continue
    tokenizer.process(tokens[7])
    text = ' '.join([token.text for token in tokenizer if not token.tokentype == 'PUNCTUATION'])
    text_lower = text.lower()
    #tdict = {'id':tokens[1], 'user':tokens[6], 'datetime':' '.join([tokens[2],tokens[3]]), 'text':text_lower}
    tweetobj = Tweet()
    tweetobj.set_id(tokens[1])
    tweetobj.set_user(tokens[6])
    tweetobj.set_datetime(tweetobj.import_datetime(tokens[2] + ' ' + tokens[3]))
    tweetobj.set_tweettext(text_lower)
    dte = dutch_timex_extractor.Dutch_timex_extractor(tweetobj.text, tweetobj.datetime)
    dte.extract_refdates()
    if len(dte.refdates) > 0:
        dte.filter_future_refdates()
    tweetobj.set_refdates(dte.refdates)
    # if len(tweetobj.refdates) > 0:
#    print(dte.refdates)
    datestrings = [obj[0] for obj in dte.refdates]
    tweet_chunks = helpers.remove_pattern_from_string(tweetobj.text,datestrings)
#    print(text_lower.encode('utf-8'),'\t'.join(tweet_chunks).encode('utf-8'))
    ee = entity_extractor.EntityExtractor()
    ee.set_commonness(cs)
    for chunk in tweet_chunks:
        tokens = chunk.split()
        ee.extract_entities(tokens)
    #    ee.extract_entities_hashtag(tokens)
    ee.filter_entities_threshold()
    tweetobj.set_entities(ee.entities)
#    print(', '.join([x[0] for x in ee.entities]).encode('utf-8'))
    tweetobjs.append(tweetobj)
print('generated',len(tweetobjs),'tweet objects, starting event ranking')

er = EventRanker(tweetobjs)
events = er.extract_events()
events_json = [event.return_dict() for event in events]
with open(outfile,'w',encoding='utf-8') as outw:
    json.dump(events_json,outw)

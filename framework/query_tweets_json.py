
import sys
import re
import json
from collections import defaultdict

import coco

def query_event_terms(event_terms, tweets, tmpdir = False):
    if tmpdir:
        cc = coco.Coco(tmpdir)
        cc.set_lines(tweets)
        cc.simple_tokenize()
        cc.set_file()
        cc.model_ngramperline(event_terms)
        matches = cc.match(event_terms)
        return matches

def query_event_terms_json(infile, qs, tmpdir):
    # open tweet file
    with open(infile, encoding = 'utf-8') as infile:
        tweets = infile.readlines()
        # check if last tweet is incomplete, if so: throw away
        erikt = re.compile('}$')
        if not erikt.match(tweets[len(tweets)-1]):
            tweets.pop()

    # extract text of tweets from json file
    tweets_text = []
    json_text = []
    for tweet in tweets:
        if not re.match(r'^{', tweet):
            tweet = '{' + '{'.join(tweet.split('{')[1:])
        try:
            decoded = json.loads(tweet)
            if len(decoded.keys()) > 2:
                text = decoded['text'].replace('\n','')
                if ('twinl_lang' in decoded and decoded['twinl_lang'] != 'dutch') or re.search(r'\bRT\b', text):
                    continue
                else:
                    tweets_text.append(text.lower())
                    json_text.append(tweet)
        except:
            print(infile, 'error occurred at line \n', tweet, 'skipping file...')
            continue

    # query event terms from tweets
    matches = query_event_terms(qs, tweets_text, tmpdir)
    matches_tweets = defaultdict(list)
    for k in matches.keys():
        matches_tweets[k] = [json_text[i].strip() for i in matches[k]]

    return matches_tweets

def query_event_terms_txt(infile, qs, tmpdir):
    # open tweet file
    with open(sys.argv[1], encoding = 'utf-8') as infile:
        tweets = infile.readlines()

    # extract text of tweets
    tweets_text = []
    for tweet in tweets[1:]:
        tokens = tweet.strip().split('\t')
        if not re.search(r'\bRT\b', tokens[-1]):
            tokenizer.process(tokens[-1])
            text = " ".join([x.text.lower() for x in tokenizer])
    for tweet in tweets_text:
        if not re.match(r'^{', tweet):
            tweet = '{' + '{'.join(tweet.split('{')[1:])
        try:
            decoded = json.loads(tweet)
            if len(decoded.keys()) > 2:
                text = decoded['text'].replace('\n','')
                if ('twinl_lang' in decoded and decoded['twinl_lang'] != 'dutch') or re.search(r'\bRT\b', text):
                    continue
                else:
                    tweets_text.append(text)
        except:
            print(infile, 'error occurred at line \n', tweet, 'skipping file...')
            quit()

    # query event terms from tweets
    matches = query_event_terms(qs, tweets_text, tmpdir)

    return matches

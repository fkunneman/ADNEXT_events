
import itertools
from collections import defaultdict

def return_combis(event_terms):
    combis = [event_terms]
    if len(event_terms) > 2:
        for i in range(2, len(event_terms)):
            for combi in (list(itertools.combinations(event_terms, i))):
                 combis.append(list(combi))
    return combis

def extract_andpatterns(tweetdict, combis):
    id_tweet = {}
    event_term_ids = defaultdict(list)
    for event_term in tweetdict.keys():
        ids = [x.split('\t')[0] for x in tweetdict[event_term]]
        for tweet in tweetdict[event_term]:
            tid = tweet.split('\t')[0]
            id_tweet[tid] = tweet
            event_term_ids[event_term].append(tid)
    combi_tweets = {}
    for combi in combis: # combine
        combi_sets = []
        for event_term in combi:
            combi_sets.append(set(event_term_ids[event_term]))
        overlap = list(set.intersection(*combi_sets))
        tweets = [id_tweet[x] for x in overlap]
        if len(tweets) > 0:
            combi_tweets['_'.join(combi)] = tweets
    return combi_tweets


from collections import Counter
from itertools import product
import math

from classes.event import Event

class EventRanker:

    def __init__(self, tweets):
        self.tweets = tweets
        self.events = []
        self.date_entity_event = {}
        self.date_counts = Counter()
        self.entity_counts = Counter()

    def list2unidict(self,l,uniform_value):
        return dict(zip(l,[uniform_value]*len(l)))

    def pair_lists(self,l1,l2):
        return list(product(l1,l2))

    def calculate_expected(self,total_count,count_v1,count_v2):
        return (count_v1 * count_v2) / total_count

    def calculate_observed(self,combi,total_count,count_v1,count_v2,observed_v1_v2):
        observed = observed_v1_v2 if combi.count('+') == 2 else total_count if combi.count('-') == 2 else count_v1 if combi[1] == '-' else count_v2
        observed_subtract = 0 if combi.count('+') == 2 else (observed_v1_v2 + self.calculate_observed(['-','+'],total_count,count_v1,count_v2,observed_v1_v2) + self.calculate_observed(['+','-'],total_count,count_v1,count_v2,observed_v1_v2)) if combi.count('-') == 2 else observed_v1_v2
        observed -= observed_subtract
        return observed

    def calculate_fit(self,observed,expected):
        try:
            return observed * (math.log(observed/expected)/math.log(2))
        except: # outcome is 0
            return 0

    def calculate_g2(self,total_count,count_v1,count_v2,observed_v1_v2):
        g2 = 0
        combis = self.pair_lists(['+','-'],['+','-'])
        for combi in combis:
            observed = self.calculate_observed(combi,total_count,count_v1,count_v2,observed_v1_v2)
            c1 = count_v1 if combi[0] == '+' else total_count-count_v1
            c2 = count_v2 if combi[0] == '+' else total_count-count_v2
            expected = self.calculate_expected(total_count,c1,c2)
            fit = self.calculate_fit(observed,expected)
            g2 += fit
        return g2

    def count_refdates(self,tweet):
        dates = tweet.refdates
        date_counts = self.list2unidict(dates,1)
        self.date_counts.update(date_counts)

    def count_entities(self,tweet):
        entities = tweet.entities
        entity_counts = self.list2unidict(entities,1)
        self.entity_counts.update(entity_counts)
        
    def make_counts(self):
        for tweet in self.tweets:
            self.count_refdates(tweet)
            self.count_entities(tweet)

    def generate_candidate_events(self):
        # Find out all possible pairs of dates and entities
        all_date_entity_pairs = self.pair_lists(self.date_counts.keys(),self.entity_counts.keys())
        date_entity_event = self.list2unidict(all_date_entity_pairs,False)
        for tweet in self.tweets:
            date_entity_pairs = self.pair_lists(tweet.refdates,tweet.entities)
            for pair in date_entity_pairs:
                if date_entity_event[pair]: # event already exists, add tweets and counts
                    event = date_entity_event[pair]
                    event.add_mention()
                    event.add_tweet(tweet)
                else: # new event should be made
                    event = Event()
                    event.set_datetime(pair[0])
                    event.add_entities([pair[1]])
                    event.add_tweet(tweet)
                    date_entity_event[pair] = event
                    self.events.append(event)

    def prune_events(self,minimum_event_mentions):
        self.events = [event for event in self.events if event.mentions >= minimum_event_mentions]

    def assess_hashtag_consistency(self,event):
        all_hashtags = sum([[x for x in tweet.entities if x[0] == '#'] for tweet in event.tweets],[])
        all_unique_hashtags = list(set(all_hashtags))
        hashtag_count = dict([(hashtag,all_hashtags.count(hashtag)) for hashtag in all_unique_hashtags])
        consistent_hashtags = [hashtag for hashtag in hashtag_count.keys() if hashtag_count[hashtag] == event.mentions]
        return consistent_hashtags

    def filter_events(self,consistent_hashtag_threshold=2):
        filtered_events = []
        for event in self.events:
            if not len(self.assess_hashtag_consistency(event)) >= consistent_hashtag_threshold:
                filtered_events.append(event)
        self.events = filtered_events

    def score_event(self,event,tweet_count):
        date = event.datetime
        entity = event.entities[0]
        event_score = self.calculate_g2(tweet_count,self.date_counts[date],self.entity_counts[entity],event.mentions)
        event.set_score(event_score)

    def score_events(self):
        tweet_count = len(self.tweets)
        for event in self.events:
            self.score_event(event,tweet_count)

    def rank_events(self,cut_off):
        ranked_events = sorted(self.events,key = lambda k: k.score,reverse=True)[:cut_off]
        self.events = ranked_events

    def extract_events(self,minimum_event_mentions=5,cut_off=2500):
        self.make_counts()
        self.generate_candidate_events()
        self.prune_events(minimum_event_mentions)
        self.filter_events()
        self.score_events()
        self.rank_events(cut_off)
        return self.events

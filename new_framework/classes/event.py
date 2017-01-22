
import json
from classes.tweet import Tweet
from collections import defaultdict

class Event:
    """
    Container for event class
    """
    def __init__(self):
        self.mentions = 1
        self.datetime = False
        self.entities = []
        self.score = False
        self.tweets = []
        self.date_tweets = defaultdict(list)

    def import_eventdict(self,eventdict):
        self.datetime = self.import_datetime(eventdict['datetime']) if 'datetime' in eventdict.keys() else False 
        self.entities = eventdict['entities'] if 'entities' in eventdict.keys() else False
        self.score = float(eventdict['score']) if 'score' in eventdict.keys() else False
        self.tweets = self.import_tweets(eventdict['tweets']) if 'tweets' in eventdict.keys() else []

    def return_dict(self):
        eventdict = {
            'datetime':str(self.datetime),
            'entities':self.entities,
            'score':self.score,
            'tweets':[tweet.return_dict() for tweet in self.tweets],
            'mentions':self.mentions
        }
        return eventdict

    def import_datetime(self,datetime):
        date,time = datetime.split()
        dt = time_functions.return_datetime(date,time,minute=True,setting='vs')
        return dt

    def set_datetime(self,datetime):
        self.datetime = datetime

    def add_entities(self,entities):
        self.entities.extend(entities)

    def set_score(self,score):
        self.score = score

    def import_tweets(self,tweets):
        imported_tweets = [Tweet(tweetdict) for tweetdict in tweets]
        return imported_tweets

    def add_tweet(self,tweet):
        self.tweets.append(tweet)
        self.date_tweets[tweet.datetime.date()].append(tweet)

    def add_mention(self,n=1):
        self.mentions += 1

    # def add_tids(self,tids):
    #     self.tids = tids

    # def set_periodics(self,events):
    #     self.periodics = events

    # def merge(self,clust):
    #     self.ids.extend(clust.ids)
    #     self.entities.extend(clust.entities) 
    #     self.entities = list(set(self.entities))
    #     self.score = max([self.score,clust.score])
    #     self.tweets = list(set(self.tweets + clust.tweets))

    # def resolve_overlap_entities(self):
    #     self.entities = calculations.resolve_overlap_entities(sorted(self.entities,key = lambda x : x[1],reverse=True))
    #     new_entities = []
    #     i = 0
    #     while i < len(entities):
    #         one = False
    #         if i+1 >= len(entities):
    #             one = True 
    #         elif entities[i][1] > entities[i+1][1]:
    #             one = True
    #         if one:
    #             overlap = False
    #             for e in new_entities:
    #                 if has_overlap_entity(re.sub('#','',entities[i][0]),re.sub('#','',e[0])):
    #                     overlap = True    
    #             if not overlap:
    #                 new_entities.append(entities[i])
    #             i+=1
    #         else: #entities have the same score
    #             #make list of entities with similar score
    #             sim_entities = [entities[i],entities[i+1]]
    #             j = i+2
    #             while j < len(entities):
    #                 if entities[j][1] == entities[i][1]: 
    #                     sim_entities.append(entities[j])
    #                     j+=1
    #                 else:
    #                     break
    #             i=j
    #             #rank entities by length
    #             sim_entities = sorted(sim_entities,key = lambda x : len(x[0].split(" ")), reverse=True)
    #             for se in sim_entities:
    #                 overlap = False
    #                 for e in new_entities:
    #                     if has_overlap_entity(se[0].replace("_"," ").replace("#",""),e[0].replace("_"," ").replace("#","")):
    #                         overlap = True
    #                 if not overlap:
    #                     new_entities.append(se)
    #     return new_entities


    # def order_entities(self):
    #     new_entities = calculations.order_entities([x[0] for x in self.entities],[x.text for x in self.tweets])
    #     new_entities_score = []
    #     for x in new_entities:
    #         entity_score = [y for y in self.entities if y[0] == x][0]
    #         new_entities_score.append(entity_score)
    #     self.entities = new_entities_score

    # def add_ttratio(self):
    #     tokens = []
    #     for tweet in self.tweets:
    #         tokens.extend(tweet.text.split(" ")) 
    #     self.tt_ratio = len(list(set(tokens))) / len(tokens)

    # def add_tfidf(self,sorted_tfidf,w_indexes):
    #     self.word_tfidf = {}
    #     sorted_word_tfidf = [(w_indexes[x[0]],x[1]) for x in sorted_tfidf if x[1] > 0]
    #     for word_score in sorted_word_tfidf:
    #         self.word_tfidf[word_score[0]] = word_score[1]

    # def rank_tweets(self,rep = False):
    #     tweet_score = []
    #     exclude = set(string.punctuation)
    #     for tweet in self.tweets:
    #         scores = []
    #         for chunk in tweet.chunks:
    #             chunk = chunk.replace('#','').replace('-',' ')
    #             chunk = ''.join(ch for ch in chunk if ch not in exclude)
    #             for word in chunk.split():
    #                 try:
    #                     wordscore = self.word_tfidf[word]
    #                     scores.append(wordscore)
    #                 except KeyError:
    #                     continue
    #         score = numpy.mean(scores)
    #         tweet_score.append((tweet.text,score))
    #     if rep:
    #         self.reptweets = []
    #         noadds = []
    #         ht = re.compile(r"^#")
    #         usr = re.compile(r"^@")
    #         url = re.compile(r"^http")
    #         for x in sorted(tweet_score,key = lambda x : x[1],reverse=True):
    #             add = True
    #             content = [x for x in x[0].split() if not ht.search(x) and not usr.search(x) and not url.search(x)]
    #             try:
    #                 for rt in self.reptweets:

    #                     overlap = len(set(content) & set(rt[1])) / max(len(set(content)),len(set(rt[1])))
    #                     if overlap > 0.8:              
    #                         add = False
    #                         noadds.append(x[0])
    #                         break
    #                 if add:
    #                     self.reptweets.append((x[0],content))
    #                 if len(self.reptweets) == 5:
    #                     break
    #             except:
    #                 break
    #         self.reptweets = [x[0] for x in self.reptweets]
    #         if len(self.reptweets) < 5:
    #             for rt in noadds:
    #                 self.reptweets.append(rt)
    #                 if len(self.reptweets) == 5:
    #                     break
    #         nreptweets = []
    #         for x in self.reptweets:
    #             tweetwords = []
    #             for word in x.split():
    #                 if url.search(word):
    #                     word = "URL"
    #                 tweetwords.append(word)
    #             nreptweets.append(" ".join(tweetwords))
    #         self.reptweets = nreptweets

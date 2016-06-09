
class Event:
    """
    Container for event class
    """
    def __init__(self,index,info):
        self.ids = [index]
        self.date = info[0]
        self.entities = info[1] #list
        self.score = info[2]
        self.tweets = info[3]
        self.periodics = []

    def add_tids(self,tids):
        self.tids = tids

    def set_periodics(self,events):
        self.periodics = events

    def merge(self,clust):
        self.ids.extend(clust.ids)
        self.entities.extend(clust.entities) 
        self.entities = list(set(self.entities))
        self.score = max([self.score,clust.score])
        self.tweets = list(set(self.tweets + clust.tweets))

    def resolve_overlap_entities(self):
        self.entities = calculations.resolve_overlap_entities(sorted(self.entities,key = lambda x : x[1],reverse=True))

    def order_entities(self):
        new_entities = calculations.order_entities([x[0] for x in self.entities],[x.text for x in self.tweets])
        new_entities_score = []
        for x in new_entities:
            entity_score = [y for y in self.entities if y[0] == x][0]
            new_entities_score.append(entity_score)
        self.entities = new_entities_score

    def add_ttratio(self):
        tokens = []
        for tweet in self.tweets:
            tokens.extend(tweet.text.split(" ")) 
        self.tt_ratio = len(list(set(tokens))) / len(tokens)

    def add_tfidf(self,sorted_tfidf,w_indexes):
        self.word_tfidf = {}
        sorted_word_tfidf = [(w_indexes[x[0]],x[1]) for x in sorted_tfidf if x[1] > 0]
        for word_score in sorted_word_tfidf:
            self.word_tfidf[word_score[0]] = word_score[1]

    def rank_tweets(self,rep = False):
        tweet_score = []
        exclude = set(string.punctuation)
        for tweet in self.tweets:
            scores = []
            for chunk in tweet.chunks:
                chunk = chunk.replace('#','').replace('-',' ')
                chunk = ''.join(ch for ch in chunk if ch not in exclude)
                for word in chunk.split():
                    try:
                        wordscore = self.word_tfidf[word]
                        scores.append(wordscore)
                    except KeyError:
                        continue
            score = numpy.mean(scores)
            tweet_score.append((tweet.text,score))
        if rep:
            self.reptweets = []
            noadds = []
            ht = re.compile(r"^#")
            usr = re.compile(r"^@")
            url = re.compile(r"^http")
            for x in sorted(tweet_score,key = lambda x : x[1],reverse=True):
                add = True
                content = [x for x in x[0].split() if not ht.search(x) and not usr.search(x) and not url.search(x)]
                try:
                    for rt in self.reptweets:

                        overlap = len(set(content) & set(rt[1])) / max(len(set(content)),len(set(rt[1])))
                        if overlap > 0.8:              
                            add = False
                            noadds.append(x[0])
                            break
                    if add:
                        self.reptweets.append((x[0],content))
                    if len(self.reptweets) == 5:
                        break
                except:
                    break
            self.reptweets = [x[0] for x in self.reptweets]
            if len(self.reptweets) < 5:
                for rt in noadds:
                    self.reptweets.append(rt)
                    if len(self.reptweets) == 5:
                        break
            nreptweets = []
            for x in self.reptweets:
                tweetwords = []
                for word in x.split():
                    if url.search(word):
                        word = "URL"
                    tweetwords.append(word)
                nreptweets.append(" ".join(tweetwords))
            self.reptweets = nreptweets
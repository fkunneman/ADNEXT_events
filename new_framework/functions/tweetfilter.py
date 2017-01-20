
class Tweetfilter:

    def __init__(self, jsontweets):
        self.tweets = jsontweets

    def is_retweet(self, tweettext):
        if tweettext[:2] == 'RT':
            return True
        else:
            return False

    def discard_retweets(self):
        new_tweets = []
        for tweet in self.tweets:
            if 'text' in tweet:
                if not self.is_retweet(tweet['text']):
                    new_tweets.append(tweet)
        self.tweets = new_tweets

    def discard_nondutch(self):
        new_tweets = []
        for tweet in self.tweets:
            if 'twinl_lang' in tweet.keys():
                if tweet['twinl_lang'] == 'dutch':
                    new_tweets.append(tweet)
            else:
                new_tweets.append(tweet)
        self.tweets = new_tweets

    def return_tweets(self):
        return self.tweets

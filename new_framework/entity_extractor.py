

class EntityExtractor:

    def __init__(self, commonness):
        self.commonness = commonness
        self.entities = []

    def extract_ngrams(self,tokens,n):
        ngrams = list(zip(*[tokens[i:] for i in range(n)]))
        ngrams_string = [' '.join(ngram) for ngram in ngrams]
        return ngrams_string

    def score_commonness_pattern(self,pattern):
        commonness_score = self.commonness.dmodel[pattern]
        return commonness_score

    def match_entities_ngram(self,ngram):
        pattern = self.commonness.classencoder.buildpattern(ngram)
        if pattern.unknown():        
            return False
        else:
            commonness_score = self.score_commonness_pattern(pattern)
            return (ngram,commonness_score)

    def match_entities_ngrams(self,ngrams):
        patterns = [self.match_entities_ngram(ngram) for ngram in ngrams]
        matches = [pattern for pattern in patterns if pattern]
        return matches

    def extract_entities_commonness(self,tokens,maximum_token_length_entity=5):
        ngrams = sum([self.extract_ngrams(tokens,token_length) for token_length in range(maximum_token_length_entity)],[]) 
        matches = self.match_entities_ngrams(ngrams)
        return matches

    def extract_entities_hashtag(self,tokens):
        hashtags = [token for token in tokens if token[0] == '#']
        hashtags_score = [(hashtag,1) for hashtag in hashtags]
        return hashtags_score

    def extract_entities_string(self,string,maximum_token_length_entity=5,pattern_threshold=0.05):
        string_tokens = string.split()
        self.entities.extend(self.extract_entities_commonness(string_tokens,maximum_token_length_entity))
        self.entities.extend(self.extract_entities_hashtag(string_tokens))

    def extract_entities_tweetchunks(self,tweetchunks,maximum_token_length_entity=5):
        for chunk in tweetchunks:
            self.extract_entities_string(chunk,maximum_token_length_entity)

    def filter_entities_threshold(self, pattern_threshold=0.05):
        self.entities = [entity for entity in self.entities if entity[1] > pattern_threshold]

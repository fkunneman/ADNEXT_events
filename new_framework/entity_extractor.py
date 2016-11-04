

class EntityExtrator:

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
        patterns = [(ngram,self.match_entities_ngram(ngram)) for ngram in ngrams]
        matches = [pattern for pattern in patterns if pattern[1]]        

    def extract_entities(self,tweettokens,maximum_token_length_entity=5,pattern_threshold = 0.05):
        ngrams = sum([self.extract_ngrams(tweettokens,token_length) for token_length in range(maximum_token_length_entity)],[]) 
        matches = self.match_entities_ngrams(ngrams)
        self.entities = [match for match in matches if match[1] > pattern_threshold]
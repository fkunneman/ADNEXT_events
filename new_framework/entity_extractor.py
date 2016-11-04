

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

    def extract_entities(self,tokens,maximum_token_length_entity=5):
        ngrams = sum([self.extract_ngrams(tokens,token_length) for token_length in range(maximum_token_length_entity)],[]) 
        matches = self.match_entities_ngrams(ngrams)
        self.entities.extend(matches)

    def extract_entities_string(self,string,maximum_token_length_entity=5,pattern_threshold=0.05):
        string_tokens = string.split()
        self.extract_entities(string_tokens,maximum_token_length_entity)

    def extract_entities_strings(self,strings,maximum_token_length_entity=5):
        for string in strings:
            self.extract_entities_string(string,maximum_token_length_entity)

    def filter_entities_threshold(self, pattern_threshold=0.05):
        self.entities = [entity for entity in self.entities if entity[1] > pattern_threshold]

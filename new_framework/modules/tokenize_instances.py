


from luiginlp.engine import Task, StandardWorkflowComponent, InputFormat, InputComponent, registercomponent, InputSlot, Parameter, BoolParameter

import ucto
import json

from modules.filter_tweets import FilterTweets

class Tokenize_instances(Task):
    """"Tokenizes a file one document per line"""

    in_filtered = InputSlot()

    config = Parameter()
    strip_punctuation = BoolParameter()
    lowercase = BoolParameter()

    def out_tokenized(self):
        return self.outputfrominput(inputformat='filtered', stripextension='.filtered.json', addextension='.tok.json')

    def run(self):

        print('Running Tokenizer...')
        
        with open(self.in_filtered().path, 'r', encoding = 'utf-8') as file_in:
            tweets = json.load(file_in)

        toktweets = []
        tokenizer = ucto.Tokenizer(self.config)
        for tweet in tweets:
            text = tweet['text']
            tokenizer.process(text)
            tokens = []
            for token in tokenizer:
                if not (self.strip_punctuation and token.tokentype == 'PUNCTUATION'):
                    tokens.append(token.text)
            tokenized = ' '.join(tokens)
            if self.lowercase:
                tokenized = tokenized.lower()
            tweet['text'] = tokenized 
            toktweets.append(tweet)

        # write to file
        with open(self.out_tokenized().path,'w',encoding='utf-8') as file_out:
            json.dump(toktweets,file_out)

@registercomponent
class Tokenize(StandardWorkflowComponent):
    
    config = Parameter()
    strip_punctuation = BoolParameter()
    lowercase = BoolParameter()

    def accepts(self):
        return (
            InputFormat(self, format_id='filtered', extension='.filtered.json'),
            InputComponent(self, FilterTweets)
        )

    def autosetup(self):
        return Tokenize_instances

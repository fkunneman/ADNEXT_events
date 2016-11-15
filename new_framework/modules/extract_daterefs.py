

from luiginlp.engine import Task, StandardWorkflowComponent, InputFormat, InputComponent, registercomponent, InputSlot, Parameter, BoolParameter

import json

from functions import dutch_timex_extractor
from classes import tweet

class DateExtractorTask(Task):

    in_tokenized = InputSlot()

    skip_date = BoolParameter()
    skip_month = BoolParameter()
    skip_timeunit = BoolParameter()
    skip_day = BoolParameter()

    def out_dateref(self):
        return self.outputfrominput(inputformat='tokenized', stripextension='.tok.json', addextension='.dateref.json')

    def run(self):
        
        # read in tweets
        with open(self.in_tokenized().path, 'r', encoding = 'utf-8') as file_in:
            tweetdicts = json.loads(file_in)

        # format as tweet objects
        tweets = [tweet.Tweet(tweetdict) for tweetdict in tweetdicts]

        for tweet in tweets:
            dte = dutch_timex_extractor.Dutch_timex_extractor(tweet.text, tweet.date)

        if self.lowercase:
            documents = [doc.lower() for doc in documents]

        ft = featurizer.Featurizer(documents, features)
        ft.fit_transform()
        instances, vocabulary = ft.return_instances(['token_ngrams'], )

        numpy.savez(self.out_features().path, data=instances.data, indices=instances.indices, indptr=instances.indptr, shape=instances.shape)

        vocabulary = list(vocabulary)
        with open(self.out_vocabulary().path,'w',encoding='utf-8') as vocab_out:
            vocab_out.write('\n'.join(vocabulary))
        
@registercomponent
class Featurize(StandardWorkflowComponent):
    token_ngrams = Parameter(default='1 2 3')
    blackfeats = Parameter(default=False)
    lowercase = BoolParameter(default=True)    

    tokconfig = Parameter(default=False)
    strip_punctuation = BoolParameter(default=True)

    def accepts(self):
        return InputFormat(self, format_id='tokenized', extension='tok.txt'), InputComponent(self, Tokenize, config=self.tokconfig, strip_punctuation=self.strip_punctuation)
                    
    def autosetup(self):
        return Featurize_tokens

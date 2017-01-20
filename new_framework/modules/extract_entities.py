

from luiginlp.engine import Task, StandardWorkflowComponent, InputFormat, InputComponent, registercomponent, InputSlot, Parameter, BoolParameter

import json

from functions import entity_extractor, helpers
from classes import tweet, commonness
from modules.extract_cityref import ExtractCityref

class ExtractEntitiesTask(Task):

    in_cityref = InputSlot()

    commonness_txt = Parameter()
    commonness_cls = Parameter()
    commonness_corpus = Parameter()
    ngrams_score = Parameter()

    def out_entity(self):
        return self.outputfrominput(inputformat='cityref', stripextension='.json', addextension='.entity.json')

    def run(self):

        # set commonness object
        cs = commonness.Commonness()
        cs.set_classencoder(self.commonness_txt, self.commonness_cls, self.commonness_corpus)
        cs.set_dmodel(self.ngrams_score)
        
        # read in tweets
        with open(self.in_cityref().path, 'r', encoding = 'utf-8') as file_in:
            tweetdicts = json.loads(file_in.read())

        # format as tweet objects
        tweets = []
        for td in tweetdicts:
            tweetobj = tweet.Tweet()
            tweetobj.import_tweetdict(td)
            tweets.append(tweetobj)

        # extract entities
        for tweetobj in tweets:
            # remove already extracted time and locations from the tweet, forming it into chunks
            datestrings = [sr[0] for sr in tweetobj.string_refdates]
            cities = tweetobj.cityrefs
            tweet_chunks = helpers.remove_pattern_from_string(tweetobj.text,datestrings+cities)
            # find entities in every chunk
            ee = entity_extractor.EntityExtractor()
            ee.set_commonness(cs)
            for chunk in tweet_chunks:
                tokens = chunk.split()
                ee.extract_entities(tokens)
                ee.filter_entities_threshold()
            tweetobj.set_entities(ee.entities)

        # write to file
        outtweets = [tweet.return_dict() for tweet in tweets]
        with open(self.out_entity().path,'w',encoding='utf-8') as file_out:
            json.dump(outtweets,file_out)
        
@registercomponent
class ExtractEntities(StandardWorkflowComponent):

    commonness_txt = Parameter()
    commonness_cls = Parameter()
    commonness_corpus = Parameter()
    ngrams_score = Parameter()    

    config = Parameter()
    strip_punctuation = BoolParameter()
    to_lowercase = BoolParameter()
    skip_date = BoolParameter()
    skip_month = BoolParameter()
    skip_timeunit = BoolParameter()
    skip_day = BoolParameter()
    citylist = Parameter()

    def accepts(self):
        return (
            InputFormat(self, format_id='cityref', extension='.json'),
            InputComponent(self, ExtractCityref, config=self.config, strip_punctuation=self.strip_punctuation, to_lowercase=self.to_lowercase, citylist=self.citylist, skip_date=self.skip_date, skip_month=self.skip_month, skip_timeunit=self.skip_timeunit, skip_day=self.skip_day)
        )
                    
    def autosetup(self):
        return ExtractEntitiesTask

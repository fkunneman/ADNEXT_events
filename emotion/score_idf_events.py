
import sys
import os

import datahandler
import featurizer

eventdoc = sys.argv[1]
outfile = sys.argv[2]

dh = datahandler.Datahandler()
dh.set(eventdoc)
dh.filter_punctuation()
dh.to_lower()

f = {'token_ngrams' : {'n_list' : [1, 2, 3]}}
dir_eventdoc = '/'.join(eventdoc.split('/')[:-1])
featurizer = featurizer.Featurizer(dh.dataset['text'], dh.dataset['tagged'], dir_eventdoc, f)
featurizer.fit_transform()
instances, vocabulary = featurizer.return_instances(['token_ngrams'])

print(' | '.join(instances[1]).encode('utf-8'))

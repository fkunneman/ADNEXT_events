
import sys
import os

import datahandler
import featurizer
import vectorizer

eventdoc = sys.argv[1]
outfile = sys.argv[2]

dh = datahandler.Datahandler()
dh.set(eventdoc)
dh.filter_punctuation()
dh.to_lower()

f = {'token_ngrams' : {'n_list' : [1, 2, 3, 4, 5]}}
dir_eventdoc = '/'.join(eventdoc.split('/')[:-1])
featurizer = featurizer.Featurizer(dh.dataset['text'], dh.dataset['tagged'], dir_eventdoc, f)
featurizer.fit_transform()
instances, vocabulary = featurizer.return_instances(['token_ngrams'])

labels = dh.dataset['label']
vr = vectorizer.Vectorizer(instances, instances, labels, 'tfidf', len(vocabulary))
train_vectors, test_vectors, top_features, top_features_values =  vr.vectorize()
vocabulary_topfeatures = [[vocabulary[i], top_feature_values[i]] for i in top_features]

with open(outfile, 'w', encoding = 'utf-8') as file_out:
    for vt in sorted(vocabulary_topfeatures, key = lambda k : k[1]):
        outfile.write(' '.join(vt) + '\n')

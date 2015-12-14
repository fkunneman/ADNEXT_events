
import sys

import docreader
import reporter

experimentdir = sys.argv[1]
docsfile = sys.argv[2]
label = sys.argv[3]

print('reading in docs')
dr = docreader.Docreader()
lines = dr.parse_csv(docsfile)
docs = [x[-1] for x in lines]

print('reading in targets')
# parse test
with open(experimentdir + 'test', 'r', encoding = 'utf-8') as test_in:
    instances = test_in.readlines()
    test_tuples = [instance.strip().split() for instance in instances]
    targets = dict((filename, target) for filename, target in test_tuples)

print('reading in classifications')
classifications = []
# parse output
with open(experimentdir + 'test.rnk', 'r', encoding = 'utf-8') as output_in:
    for line in output_in.readlines():
        tokens = line.strip().split()
        filename = '/'.join(tokens[0].strip().split('/')[-2:])
        classification, score = tokens[1].split()[0].split(":")
        classification = classification.replace("?","")
        classifications.append([targets[filename], classification, float(score)])

print('performing evaluation')
output = (classifications, False, False)
ev = reporter.Eval([docs, output], [label, 'other'], experimentdir)
ev.report()

features_weight = []
with open(experimentdir + 'data/' + label + '_6.mitp', 'r', encoding = 'utf-8') as features_in:
    featurelines = features_in.readlines()[6:]
    for line in featurelines:
        tokens = line.split('\t')
        feature = tokens[0]
        weight = round(float(tokens[1]), 2)
        features_weight.append([feature, weight])

features_weight_sorted = sorted(features_weight, key = lambda k : k[1], reverse = True)
with open(experimentdir + 'features_sorted.txt', 'w', encoding = 'utf-8') as features_out:
    features_out.write('\n'.join(['\t'.join([str(x) for x in line]) for line in features_weight_sorted]))

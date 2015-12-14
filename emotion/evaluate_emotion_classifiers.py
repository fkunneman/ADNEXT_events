
import sys

import reporter

experimentdir = sys.argv[1]
testfile = sys.argv[2]
label = sys.argv[3]

print('reading in targets')
# parse test
with open(testfile, 'r', encoding = 'utf-8') as test_in:
    instances = test_in.readlines()
    test_tuples = [instance.strip().split() for instance in instances]
    targets = dict((filename, target) for filename, target in test_tuples)

print('reading in classifications')
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
ev = reporter.Eval Reporter(output, [label, 'other'], experimentdir)
ev.report()

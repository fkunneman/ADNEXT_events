
import sys
import matplotlib.pyplot as plt

import docreader
import reporter

experimentdir = sys.argv[1]
docsfile = sys.argv[2]
label = sys.argv[3]
parts = sys.argv[4]
plot_out = sys.argv[5]
num_targets = int(sys.argv[6])
clfile = int(sys.argv[7]) # true or false

if clfile:
    print('quick parse')
    dr = docreader.Docreader()
    dr.parse_doc(experimentdir + 'classifications.txt')
    clfs = dr.lines[2:]
    classifications = []
    for clf in clfs:
        clf = clf[0].split()
        try:
            clf[2] = float(clf[2])
        except:
            print(clf)
            clf = clf[1:]
            clf[2] = float(clf[2])
        classifications.append(clf)
    selected_docs = ['p'] * len(classifications)

else:
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

    print('reading in parts')
    with open(parts, 'r', encoding = 'utf-8') as parts_in:
        instances = parts_in.readlines()
        indices = dict((instance.split()[0], i) for i, instance in enumerate(instances))

    print('reading in classifications')
    classifications = []
    selected_docs = []
    # parse output
    with open(experimentdir + 'test.rnk', 'r', encoding = 'utf-8') as output_in:
        for line in output_in.readlines():
            try:
                tokens = line.strip().split()
                filename = '/'.join(tokens[0].strip().split('/')[-3:])
                classification, score = tokens[1].split()[0].split(":")
                classification = classification.replace("?","")
                classifications.append([targets[filename], classification, float(score)])
                selected_docs.append(docs[indices[filename]])
            except:
                print('wrong input', line.encode('utf-8'))
            
    print('selected', len(selected_docs), 'docs')
    print('performing evaluation')


x, y = [], []
target_classifications = [c for c in classifications if c[1] == label]
sorted_classifications = sorted(target_classifications, key = lambda k : k[2], reverse = True)
targets = 0
classifications = 0
for cl in sorted_classifications:
    classifications += 1
    if cl[0] == label:
        targets += 1
    recall = round(targets / num_targets, 2)
    x.append(classifications)
    y.append(recall)

plt.plot(x, y, linestyle = '-', linewidth = 2)
plt.ylim((0,1))
plt.xlabel('Rank')
plt.ylabel('Recall-at-Rank')
plt.savefig(plot_out)

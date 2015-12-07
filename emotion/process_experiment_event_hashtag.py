
import sys
import os
import random
import re

import coco
import docreader
import reporter
import utils
import featurizer

hashtag = sys.argv[1]
label_positive = sys.argv[2]
label_negative = sys.argv[3]
tweets_hashtag = sys.argv[4]
tweets_random = sys.argv[5]
parts_hashtag = sys.argv[6]
parts_random = sys.argv[7]
tweets_train = sys.argv[8]
tweets_dev = sys.argv[9]
parts_train = sys.argv[10]
parts_dev = sys.argv[11]
files_dir = sys.argv[12]
experiment_dir = sys.argv[13]

def write_config():
    fileschunks = files_dir.split("/")
    files = "/".join(fileschunks[:-1]) + "/./" + fileschunks[-1]
    current = os.getcwd()
    current_chunks = current.split("/")
    data = "/".join(current_chunks) + "/./data"
    index = "/".join(current_chunks) + "/./index"
    config = "\n".join\
        ([
        "docprof.normalise=NONE",
        "general.analyser=nl.cs.ru.phasar.lcs3.analyzers.FreqAnalyzer",
        "general.autothreshold=true",
        "general.data=" + data,
        "general.files=" + files,
        "general.index=" + index,
        "general.numcpus=16",
        "general.termstrength=BOOL", # hier een parameter
        "gts.mindf=1",
        "gts.mintf=6",
        "lts.algorithm=INFOGAIN", # parameter
        "lts.maxterms=100000",
        "profile.memory=false",
        "research.fullconfusion=false",
        "research.writemit=true",
        "research.writemitalliters=true",
        "general.algorithm=WINNOW",
        "general.docext=",
        "general.fbeta=1.0",
        "general.fullranking=true",
        "general.maxranks=1",
        "general.minranks=1",
        "general.preprocessor=",
        "general.rankalliters=false",
        "general.saveclassprofiles=true",
        "general.threshold=1.0",
        "general.writetestrank=true",
        "gts.maxdf=1000000",
        "gts.maxtf=1000000",
        "lts.aggregated=true",
        "naivebayes.smoothing=1.0",
        "positivenaivebayes.classprobability=0.2",
        "regwinnow.complexity=0.1",
        "regwinnow.initialweight=0.1",
        "regwinnow.iterations=10",
        "regwinnow.learningrate=0.01",
        "regwinnow.ownthreshold=true",
        "research.conservememory=true",
        "research.mitsortorder=MASS",
        "rocchio.beta=1.0",
        "rocchio.gamma=1.0",
        "svmlight.params=",
        "winnow.alpha=1.05",
        "winnow.beta=0.95",
        "winnow.beta.twominusalpha=false",
        "winnow.decreasing.alpha=false",
        "winnow.decreasing.alpha.strategy=LOGARITMIC",
        "winnow.maxiters=6",
        "winnow.negativeweights=true",
        "winnow.seed=-1",
        "winnow.termselect=false",
        "winnow.termselect.epsilon=1.0E-4",
        "winnow.termselect.iterations=1,2,",
        "winnow.thetamin=0.5",
        "winnow.thetaplus=2.5"
        ])
    with open("lcs3.conf", "w", encoding = "utf-8") as config_out:
        config_out.write(config)

tmpdir = 'tmp/'
if not os.path.exists(tmpdir):
    os.mkdir(tmpdir)
if not os.path.exists(experiment_dir):
    os.mkdir(experiment_dir)
event_train_dir = experiment_dir + 'event_train/'
if not os.path.exists(event_train_dir):
    os.mkdir(event_train_dir)
emotion_train_dir = experiment_dir + 'emotion_train/'
if not os.path.exists(emotion_train_dir):
    os.mkdir(emotion_train_dir)

print('train events')

# identify dev indices with hashtag
#dr = docreader.Docreader()
# devlines = dr.parse_csv(tweets_dev)
# textlines_dev = [x[-1] for x in devlines]

# cc = coco.Coco(tmpdir)
# cc.set_lines(textlines_dev)
# cc.set_file()
# cc.model_ngramperline([hashtag])
# matches = cc.match([hashtag])[hashtag]

#matches = random.sample(range(len(textlines_dev)), 1000)

# ht_tweets_dev = [devlines[i] for i in matches]
# with open(parts_dev) as dev_open:
#     parts = dev_open.readlines()

# test = []
# for i, instance in enumerate(parts):
#     tokens = instance.split()
#     if i in matches:
#         test.append(tokens[0] + ' ' + label_positive)
#     else:
#         test.append(tokens[0] + ' ' + label_negative)
# test_tuples = [instance.split() for instance in test]
# targets = dict((filename, target) for filename, target in test_tuples)

# identify train indices with hashtag
dr = docreader.Docreader()
trainlines = dr.parse_csv(tweets_train)
textlines = [x[-1] for x in trainlines]

cc = coco.Coco(tmpdir)
cc.set_lines(textlines)
cc.set_file()
cc.model_ngramperline([hashtag])
matches = cc.match([hashtag])[hashtag]

#matches = random.sample(range(len(textlines)), 2000)

# make new files with matches
ht_tweets_train = [textlines[i] for i in matches]
ht_tweets_train_tagged = utils.tokenized_2_tagged(ht_tweets_train)
find_username = re.compile("^@\w+")
find_url = re.compile(r"^(http://|www|[^\.]+)\.([^\.]+\.)*[^\.]{2,}")
new_tweets_tagged = []
for tweet in ht_tweets_train_tagged:
    new_tweet = []
    for token in tweet:
        if find_username.match(token[0]):
            token[0] = '_USER_'
        elif find_url.match(token[0]):
            token[0] = '_URL_'
        else:
            token[0] = token[0].lower()
        new_tweet.append(token)
    new_tweets_tagged.append(new_tweet)

print('Extracting features')
partsdirectory = '/'.join(parts_hashtag.split('/')[:-1]) + '/'
featuredict = {'token_ngrams' : {'n_list': [1, 2, 3], 'blackfeats' : ['_USER_', '_URL_'] + [hashtag]}}
ft = featurizer.Featurizer(ht_tweets_train, new_tweets_tagged, partsdirectory, featuredict)
ft.fit_transform()
instances, vocabulary = ft.return_instances(['token_ngrams'])

train = []
# make chunks of 25000 from the data
chunks = [range(instances.shape[0])]
for i, chunk in enumerate(chunks):
    # make subdirectory
    subpart = 'event_' + label_positive + '/'
    subdir = files_dir + subpart
    if not os.path.isdir(subdir):
        os.mkdir(subdir)
    for j, index in enumerate(chunk):
        zeros = 5 - len(str(j))
        filename = subpart + ('0' * zeros) + str(j) + '.txt'
        features = [vocabulary[x] for x in instances[index].indices]
        with open(files_dir + filename, 'w', encoding = 'utf-8') as outfile: 
            outfile.write('\n'.join(features))
        train.append(filename + ' ' + label_positive)

with open(parts_train) as train_open:
    parts = train_open.readlines()

parts_indices = range(len(parts))
nht_train = list(set(parts_indices) - set(matches))
num_ht_train = len(matches)
random_train = random.sample(nht_train, num_ht_train)

for i, instance in enumerate(parts):
    if i in random_train:
        tokens = instance.split()
        train.append(tokens[0] + ' ' + label_negative)

# classify lcs
with open('train', 'w', encoding = 'utf-8') as train_out:
    train_out.write('\n'.join(train))
# with open('test', 'w', encoding = 'utf-8') as test_out:
#     test_out.write('\n'.join(test))
write_config()

os.system("lcs --verbose")

# evaluate
# classifications = []
# with open('test.rnk') as rnk:
#     for line in rnk.readlines():
#         tokens = line.strip().split()
#         filename = tokens[0].strip()
#         classification, score = tokens[1].split()[0].split(":")
#         classification = classification.replace("?","")
#         classifications.append([targets[filename], classification, float(score)])

os.system("mv * " + event_train_dir)
#output = (textlines_dev, [classifications, False, False]) 
#rp = reporter.Eval(output, [label_positive, label_negative], event_train_dir)
#rp.report()

#################################################

print('train emotion')

# select training tweets positive and negative
dr = docreader.Docreader()
train_tweets_general = dr.parse_csv(tweets_hashtag)
train_tweets_ids = [x[0] for x in train_tweets_general]
ids_dev = set([x[0] for x in devlines])
overlap = [] 
for i, tweet in enumerate(train_tweets_ids):
    if set([tweet]) & ids_dev:
        overlap.append(i)

with open(parts_hashtag) as ph_open:
    train_parts_general = ph_open.readlines()
print('train size before:', len(train_parts_general))
train_parts_general_clean = [x for i, x in enumerate(train_parts_general) if not i in overlap]
print('train size after:', len(train_parts_general_clean))

dr = docreader.Docreader()
random_tweets = dr.parse_csv(tweets_random)
random_tweets_ids = [x[0] for x in random_tweets]
overlap = [] 
for i, tweet in enumerate(random_tweets_ids):
    if set([tweet]) & ids_dev:
        overlap.append(i)   
with open(parts_random) as pr_open:
    random_parts = pr_open.readlines()
print('random size before:', len(random_parts))
random_parts_clean = [x for i, x in enumerate(random_parts) if not i in overlap]
print('random size after:', len(random_parts_clean))

random_sample = random.sample(random_parts_clean, len(train_parts_general_clean))
with open('train', 'w', encoding = 'utf-8') as train_out:
    train_out.write(''.join(train_parts_general_clean))
    for x in random_sample:
        tokens = x.strip().split()
        train_out.write('\n' + tokens[0] + ' ' + label_negative)

# with open('test', 'w', encoding = 'utf-8') as test_out:
#     test_out.write('\n'.join(test))
write_config()

# classify lcs
os.system("lcs --verbose")

# evaluate
# classifications = []
# with open('test.rnk') as rnk:
#     for line in rnk.readlines():
#         tokens = line.strip().split()
#         filename = tokens[0].strip()
#         classification, score = tokens[1].split()[0].split(":")
#         classification = classification.replace("?","")
#         classifications.append([targets[filename], classification, float(score)])

os.system("mv * " + emotion_train_dir)
# output = (textlines_dev, [classifications, False, False]) 
# rp = reporter.Eval(output, [label_positive, label_negative], emotion_train_dir)
# rp.report()

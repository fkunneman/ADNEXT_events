
import sys
import os
import random
import re
import itertools

import coco
import docreader
import reporter
import utils
import featurizer

label_positive = sys.argv[1]
label_negative = sys.argv[2]
tweets_random = sys.argv[3]
parts_random = sys.argv[4]
tweets_test = sys.argv[5]
tweets_train = sys.argv[6]
emotiondir = sys.argv[7]
files_dir = sys.argv[8]
experiment_dir = sys.argv[9]
partsdirectory = sys.argv[10]
hashtags = sys.argv[11:]

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

def train_combimodels(hts):

    expdir = experiment_dir + '_'.join([x[1:] for x in hts]) + '/' # without '#'

    if not os.path.exists(exp):
        os.mkdir(exp)
    event_train_dir = expdir + 'event_train/'
    if not os.path.exists(event_train_dir):
        os.mkdir(event_train_dir)
    emotion_train_dir = expdir + 'emotion_train/'
    if not os.path.exists(emotion_train_dir):
        os.mkdir(emotion_train_dir)

    print('Train events')

    # make new files with matches
    print('Making new train files')
    hts_tweets_train = []
    all_matches = []
    for ht in hts:
        all_matches.extend(hashtag_trainmatches[ht])
    all_matches = sorted(list(set(all_matches)))
    hts_tweets_train = [textlines_train[i] for i in all_matches]
    hts_tweets_train_tagged = utils.tokenized_2_tagged(hts_tweets_train)
    find_username = re.compile("^@\w+")
    find_url = re.compile(r"^(http://|www|[^\.]+)\.([^\.]+\.)*[^\.]{2,}")
    new_tweets_tagged = []
    for tweet in hts_tweets_train_tagged:
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
    featuredict = {'token_ngrams' : {'n_list': [1, 2, 3], 'blackfeats' : ['_USER_', '_URL_'] + hts}}
    ft = featurizer.Featurizer(hts_tweets_train, new_tweets_tagged, partsdirectory, featuredict)
    ft.fit_transform()
    instances, vocabulary = ft.return_instances(['token_ngrams'])

    train = []
    # make chunks of 25000 from the data
    chunks = [range(instances.shape[0])]
    for i, chunk in enumerate(chunks):
        # make subdirectory
        subpart = 'event_' + '_'.join([x[1:] for x in hts]) + '/'
        subdir = files_dir + subpart
        if not os.path.isdir(subdir):
            os.mkdir(subdir)
        for j, index in enumerate(chunk):
            zeros = 5 - len(str(j))
            filename = subpart + ('0' * zeros) + str(j) + '.txt'
            features = [vocabulary[x].replace(' ', '_') for x in instances[index].indices]
            with open(files_dir + filename, 'w', encoding = 'utf-8') as outfile: 
                outfile.write('\n'.join(features))
            train.append(filename + ' ' + label_positive)

    with open(parts_train) as train_open:
        parts = train_open.readlines()

    parts_indices = range(len(parts))
    nht_train = list(set(parts_indices) - set(all_matches))
    num_ht_train = len(all_matches)
    random_train = random.sample(nht_train, num_ht_train)
    random_train_set = set(random_train)

    for i, instance in enumerate(parts):
        if set([i]) & random_train_set:
            tokens = instance.split()
            train.append(tokens[0] + ' ' + label_negative)

    # classify lcs
    with open('train', 'w', encoding = 'utf-8') as train_out:
        train_out.write('\n'.join(train))

    write_config()
    os.system("lcs --verbose")
    os.system("mv * " + event_train_dir)

    #################################################

    print('Train emotion')
    # cleanup mixedtweetfile
    hts_emotiontweets_train = []
    for ht in hts:
        hts_emotiontweets_train.extend(hashtag_emotiontweets[ht][0])
    # rm overlap
    seen = {}
    for tid in list(set([x[1] for x in hts_emotiontweets_train])):
        seen[tid] = False
    hts_emotiontweets_train_clean = []
    for tweet in hts_emotiontweets_train:
        if not seen(tweet[1]):
            hts_emotiontweets_train_clean.append(tweet)
            seen[tweet[1]] = True
    # new featurizer: rm all involved hashtags
    print('Making new training files')
    hts_emotiontweets_train_clean_text = [line[8] for line in hts_emotiontweets_train]
    hts_emotiontweets_train_clean_tagged = utils.tokenized_2_tagged(hts_emotiontweets_train_clean_text)
    find_username = re.compile("^@\w+")
    find_url = re.compile(r"^(http://|www|[^\.]+)\.([^\.]+\.)*[^\.]{2,}")
    new_tweets_tagged = []
    for tweet in hts_emotiontweets_train_clean_tagged:
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
    featuredict = {'token_ngrams' : {'n_list': [1, 2, 3], 'blackfeats' : ['_USER_', '_URL_'] + hts}} # with '#'
    ft = featurizer.Featurizer(hts_emotiontweets_train_clean_tagged, new_tweets_tagged, partsdirectory, featuredict)
    ft.fit_transform()
    instances, vocabulary = ft.return_instances(['token_ngrams'])

    train = []
    # make chunks of 25000 from the data
    chunks = [range(instances.shape[0])]
    for i, chunk in enumerate(chunks):
        # make subdirectory
        subpart = '_'.join([x[1:] for x in hts]) + '/' # without '#'
        subdir = files_dir + subpart
        if not os.path.isdir(subdir):
            os.mkdir(subdir)
        for j, index in enumerate(chunk):
            zeros = 5 - len(str(j))
            filename = subpart + ('0' * zeros) + str(j) + '.txt'
            features = [vocabulary[x].replace(' ', '_') for x in instances[index].indices]
            with open(files_dir + filename, 'w', encoding = 'utf-8') as outfile: 
                outfile.write('\n'.join(features))
            train.append(filename + ' ' + label_positive)

    # classify lcs
    if len(random_parts_clean) < len(train):
        random_sample = random.sample(random_parts_clean, len(train))
    else:
        random_sample = random_parts_clean
    with open('train', 'w', encoding = 'utf-8') as train_out:
        train_out.write(''.join(train))
        for x in random_sample:
            tokens = x.strip().split()
            train_out.write('\n' + tokens[0] + ' ' + label_negative)

    write_config()
    os.system("lcs --verbose")
    os.system("mv * " + emotion_train_dir)

############################# MAIN ################################

tmpdir = 'tmp/'
if not os.path.exists(tmpdir):
    os.mkdir(tmpdir)

print('Reading in test tweets')
# identify test indices with hashtag
dr = docreader.Docreader()
testlines = dr.parse_csv(tweets_test)
textlines_test = [x[-1] for x in testlines]

print('Reading in train tweets')
# identify train indices with hashtag
dr = docreader.Docreader()
trainlines = dr.parse_csv(tweets_train)
textlines_train = [x[-1] for x in trainlines]

print('Identifying hashtag matches')
hashtag_trainmatches = {}

cc = coco.Coco(tmpdir)
cc.set_lines(textlines_train)
cc.set_file()
for hashtag in hashtags:    
    print(hashtag)
    cc.model_ngramperline([hashtag]) # with '#'
    hashtag_trainmatches[hashtag] = cc.match([hashtag])[hashtag]

# select emotion tweets positive and negative
print('Extracting emotion tweets')
hashtag_emotiontweets = {}

ids_test = set([x[0] for x in testlines])
dr = docreader.Docreader()
for hashtag in hashtags:
    print(hashtag)
    tweets_hashtag = emotiondir + hashtag + '.csv'
    parts_hashtag = partsdirectory + hashtag[1:] + '.txt'
    train_tweets_general = dr.parse_csv(tweets_hashtag)
    train_tweets_ids = [x[1] for x in train_tweets_general]
    overlap = [] 
    for i, tweet in enumerate(train_tweets_ids):
        if set([tweet]) & ids_test:
            overlap.append(i)
    train_tweets_general_clean = [x for i, x in enumerate(tran_tweets_general) if not i in overlap]
    hashtag_emotiontweets[hashtag] = train_tweets_general_clean

print('Extracting random tweets')
dr = docreader.Docreader()
random_tweets = dr.parse_csv(tweets_random)
random_tweets_ids = [x[0] for x in random_tweets]
overlap = [] 
for i, tweet in enumerate(random_tweets_ids):
    if set([tweet]) & ids_test:
        overlap.append(i)   
with open(parts_random) as pr_open:
    random_parts = pr_open.readlines()
print('random size before:', len(random_parts))
random_parts_clean = [x for i, x in enumerate(random_parts) if not i in overlap]
print('random size after:', len(random_parts_clean))

############ make combis and train classifiers ##################
combis = []
for i in range(2, len(hashtags)):
    for combi in itertools.combinations(hashtags, i):
        combis.append(list(combi))
combis.append(hashtags)

for combi in combis:
    print('Training classifiers for ', '_'.join(combi))
    train_combimodels(combi)

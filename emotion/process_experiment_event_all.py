
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
tweets_test = sys.argv[4]
emotiondir = sys.argv[5]
files_dir = sys.argv[6]
expdir = sys.argv[7]
partsdirectory = sys.argv[8]
combi = sys.argv[9:]

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

    if not os.path.exists(expdir):
        os.mkdir(expdir)

    print('Train emotion')
    # cleanup mixedtweetfile
    hts_emotiontweets_train = []
    for ht in hts:
        hts_emotiontweets_train.extend(hashtag_emotiontweets[ht])
    # rm overlap
    seen = {}
    for tid in list(set([x[1] for x in hts_emotiontweets_train])):
        seen[tid] = False
    hts_emotiontweets_train_clean = []
    for tweet in hts_emotiontweets_train:
        if not seen[tweet[1]]:
            hts_emotiontweets_train_clean.append(tweet)
            seen[tweet[1]] = True
    # new featurizer: rm all involved hashtags
    print('Making new training files')
    hts_emotiontweets_train_clean_text = [line[8] for line in hts_emotiontweets_train_clean]
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
        subpart = 'final_' + label_positive + '/'
        subdir = files_dir + subpart
        if not os.path.isdir(subdir):
            os.mkdir(subdir)
        for j, index in enumerate(chunk):
            zeros = 5 - len(str(j))
            filename = subpart + ('0' * zeros) + str(j) + '.txt'
            features = [vocabulary[x].replace(' ', '_') for x in instances[index].indices]
            with open(files_dir + filename, 'w', encoding = 'utf-8') as outfile: 
                outfile.write('\n'.join(features))
            train.append(filename + ' ' + label_positive + '\n')

    # take sample of random tweets
    random_sample = random.sample(random_tweets_clean, len(train))

    # new featurizer: rm all involved hashtags
    print('Making new training files')
    random_clean_text = [line[5] for line in random_sample]
    random_clean_text_tagged = utils.tokenized_2_tagged(random_clean_text)
    find_username = re.compile("^@\w+")
    find_url = re.compile(r"^(http://|www|[^\.]+)\.([^\.]+\.)*[^\.]{2,}")
    new_tweets_tagged = []
    for tweet in random_clean_text:
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

    # make chunks of 25000 from the data
    chunks = [range(instances.shape[0])]
    for i, chunk in enumerate(chunks):
        # make subdirectory
        subpart = 'final_other/'
        subdir = files_dir + subpart
        if not os.path.isdir(subdir):
            os.mkdir(subdir)
        for j, index in enumerate(chunk):
            zeros = 5 - len(str(j))
            filename = subpart + ('0' * zeros) + str(j) + '.txt'
            features = [vocabulary[x].replace(' ', '_') for x in instances[index].indices]
            with open(files_dir + filename, 'w', encoding = 'utf-8') as outfile: 
                outfile.write('\n'.join(features))
            train.append(filename + ' ' + label_negative + '\n')

    with open('train', 'w', encoding = 'utf-8') as train_out:
        train_out.write(''.join(train))

    write_config()
    os.system("lcs --verbose")
    os.system("mv * " + expdir)

############################# MAIN ################################

tmpdir = 'tmp/'
if not os.path.exists(tmpdir):
    os.mkdir(tmpdir)

print('Reading in test tweets')
# identify test indices with hashtag
dr = docreader.Docreader()
testlines = dr.parse_csv(tweets_test)
textlines_test = [x[-1] for x in testlines]

# select emotion tweets positive and negative
print('Extracting emotion tweets')
hashtag_emotiontweets = {}

ids_test = set([x[0] for x in testlines])
dr = docreader.Docreader()
for hashtag in combi:
    print(hashtag)
    tweets_hashtag = emotiondir + hashtag + '.csv'
    parts_hashtag = partsdirectory + hashtag[1:] + '.txt'
    train_tweets_general = dr.parse_csv(tweets_hashtag)
    train_tweets_ids = [x[1] for x in train_tweets_general]
    overlap = [] 
    for i, tweet in enumerate(train_tweets_ids):
        if set([tweet]) & ids_test:
            overlap.append(i)
    train_tweets_general_clean = [x for i, x in enumerate(train_tweets_general) if not i in overlap]
    hashtag_emotiontweets[hashtag] = train_tweets_general_clean

print('Extracting random tweets')
dr = docreader.Docreader()
random_tweets = dr.parse_csv(tweets_random)
random_tweets_ids = [x[0] for x in random_tweets]
overlap = [] 
for i, tweet in enumerate(random_tweets_ids):
    if set([tweet]) & ids_test:
        overlap.append(i)
random_tweets_clean = [x for i, x in enumerate(train_tweets) if not i in overlap]

############ train classifier ##################
print('Training classifiers for ', '_'.join(combi))
train_combimodels(combi)

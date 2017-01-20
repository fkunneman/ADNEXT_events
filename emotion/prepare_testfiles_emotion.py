
import sys
import os

import coco
import docreader

label_positive = sys.argv[1]
label_negative = sys.argv[2]
tweets_test = sys.argv[3]
parts_test = sys.argv[4]
experiment_dir = sys.argv[5]

words = experiment_dir.split('/')[-2].split('_')
hashtags = ['#' + x for x in words]
print(hashtags)

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

# identify test indices with hashtag
dr = docreader.Docreader()
testlines = dr.parse_csv(tweets_test)
textlines_test = [x[-1] for x in testlines]

matches = []
for hashtag in hashtags:
    cc = coco.Coco(tmpdir)
    cc.set_lines(textlines_test)
    cc.set_file()
    cc.model_ngramperline([hashtag])
    matches.extend(cc.match([hashtag])[hashtag])
matches = sorted(list(set(matches)))

ht_tweets_test = [testlines[i] for i in matches]
with open(parts_test) as test_open:
    parts = test_open.readlines()

test = []
for i, instance in enumerate(parts):
    tokens = instance.split()
    if i in matches:
        test.append(tokens[0] + ' ' + label_positive)
    else:
        test.append(tokens[0] + ' ' + label_negative)

with open(experiment_dir + 'event_train/test', 'w', encoding = 'utf-8') as test_out:
    test_out.write('\n'.join(test))

with open(experiment_dir + 'emotion_train/test', 'w', encoding = 'utf-8') as test_out:
    test_out.write('\n'.join(test))

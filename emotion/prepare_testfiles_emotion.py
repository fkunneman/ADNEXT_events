
import sys
import os

import coco
import docreader

hashtag = sys.argv[1]
label_positive = sys.argv[2]
label_negative = sys.argv[3]
tweets_dev = sys.argv[4]
parts_dev = sys.argv[5]
experiment_dir = sys.argv[6]

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

# identify dev indices with hashtag
dr = docreader.Docreader()
devlines = dr.parse_csv(tweets_dev)
textlines_dev = [x[-1] for x in devlines]

cc = coco.Coco(tmpdir)
cc.set_lines(textlines_dev)
cc.set_file()
cc.model_ngramperline([hashtag])
matches = cc.match([hashtag])[hashtag]

ht_tweets_dev = [devlines[i] for i in matches]
with open(parts_dev) as dev_open:
    parts = dev_open.readlines()

test = []
for i, instance in enumerate(parts):
    tokens = instance.split()
    if i in matches:
        test.append(tokens[0] + ' ' + label_positive)
    else:
        test.append(tokens[0] + ' ' + label_negative)

with open(experiment_dir + 'test', 'w', encoding = 'utf-8') as test_out:
    test_out.write('\n'.join(test))

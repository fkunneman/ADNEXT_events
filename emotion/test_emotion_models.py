
import sys
import os
import random
import re

import coco
import docreader
import reporter
import utils
import featurizer

testparts = sys.argv[1]
hashtags = sys.argv[2:]

with open(testparts) as tp_open:
    testlines = testparts.readlines()

for i in range(len(testlines), 1000):
    try:
        chunk = testlines[i : i+1000]
    except:
        chunk = testlines[i:]
    with open('test', 'w') as testout:
        testout.write(''.join(chunk))
    for hashtag in hashtags:
        os.system('/vol/customopt/machine-learning/lib/lcs3.8/production.jar ' + hashtag + '/emotion_train/ ' +
            'test >> ' + hashtag + '/emotion_train/test.rnk')
    print(i+1000, 'lines done.')

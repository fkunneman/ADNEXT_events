
import sys
import os
import random
import re

import docreader
import reporter
import utils

testparts = sys.argv[1]
event = int(sys.argv[2]) #bool
emotion = int(sys.argv[3]) #bool
hashtags = sys.argv[4:]

with open(testparts) as tp_open:
    testlines = tp_open.readlines()
print(len(testlines))

for i in range(0, len(testlines), 1000):
    try:
        chunk = testlines[i : i+1000]
    except:
        chunk = testlines[i:]
    with open('test', 'w') as testout:
        testout.write(''.join(chunk))
    for hashtag in hashtags:
        if emotion:
            os.system('/vol/customopt/machine-learning/lib/lcs3.8/production.jar ' + hashtag + '/emotion_train/ ' +
            'test >> ' + hashtag + '/emotion_train/test.rnk')
        if event:
            os.system('/vol/customopt/machine-learning/lib/lcs3.8/production.jar ' + hashtag + '/event_train/ ' +
            'test >> ' + hashtag + '/event_train/test.rnk')
    print(i+1000, 'lines done.')
    os.system('rm -r unseenidx/')

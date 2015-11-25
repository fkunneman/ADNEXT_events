
import sys
import os

import docreader
import utils

statdir = sys.argv[1]
taggeddir = sys.argv[2]
outfile = sys.argv[3]

taggedfiles = os.listdir(taggeddir)

# create bigdocs
header = ['label', 'tweet_id', 'author_id', 'date', 'time', 'authorname', 'text', 'tagged']
bigdocs = [header]
for taggedfile in taggedfiles:
    label = eventfile.split('_')[1][:-4]
    with open(statdir + 'tweet_' + label + '.txt') as stat_in:
        lines = stat_in.read().split('\n')
        event_info = line[0]
        date = event_info.split('\t')[1]
    reader = docreader.Docreader()
    lines = reader.parse_csv(eventdir + eventfile)
    tagged = '\n'.join([x[-1] for x in lines])
    text = ' '.join([x[-2] for x in lines])
    bigdoc = [label, '-', '-', 'date', '-', '-', text, tagged]
    bigdocs.append(bigdoc)

utils.write_csv(bigdocs, outfile)

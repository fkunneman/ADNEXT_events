
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
    label = taggedfile.split('_')[1][:-4]
    with open(statdir + 'sequence_' + label + '.txt') as stat_in:
        lines = stat_in.read().split('\n')
        event_info = lines[0]
        date = event_info.split('\t')[1]
    reader = docreader.Docreader()
    lines = reader.parse_csv(taggeddir + taggedfile)
    tagged = '\n'.join([x[-1] for x in lines[1:]])
    text = ' '.join([x[-2] for x in lines[1:]])
    bigdoc = [label, '-', '-', 'date', '-', '-', text, tagged]
    bigdocs.append(bigdoc)

utils.write_csv(bigdocs, outfile)

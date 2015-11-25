
import sys
import os

import docreader


eventdir = sys.argv[1]

eventfiles = os.listdir(eventdir)

# create bigdocs
bigdocs = []
for eventfile in eventfiles:
    label = eventfile.split('_')[1][:-4]
    reader = docreader.Docreader()
    lines = reader.parse_csv(eventdir + eventfile)
    print(lines[:3])
            
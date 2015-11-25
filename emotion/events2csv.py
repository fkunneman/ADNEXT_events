
import sys
import os

import docreader
import utils

eventdir = sys.argv[1]
eventfiles = sys.argv[2:]

fields = ['label', 'doc_id', 'author_id', 'date', 'time', 'authorname', 'text', 'tagged']
columndict = {'doc_id' : 0, 'author_id' : 1, 'authorname' : 2, 'date' : 3, 'time' : 4, 'text' : 5}

for eventfile in eventfiles:
    reader = docreader.Docreader()
    reader.parse_doc(eventfile, '\t', False, False, False)
    new_lines, other_lines = reader.set_lines(fields, columndict)
    csv_doc = eventfile[:-4] + '.csv'
    utils.write_csv(new_lines, csv_doc) 


import sys
import os

import docreader
import utils

eventdir = sys.argv[1]
eventfiles = sys.argv[2:]

fields = ['label', 'doc_id', 'author_id', 'date', 'time', 'authorname', 'text', 'tagged']
columndict = {0 : 'doc_id', 1 : 'author_id', 2 : 'authorname', 3 : 'date', 4 : 'time', 5 : 'text'}

for eventfile in eventfiles:
    reader = docreader.Docreader()
    reader.parse_doc(eventfile, '\t', False, False, False)
    new_lines, other_lines = reader.set_lines(fields, columndict)
    csv_doc = eventfile[:-4] + '.csv'
    utils.write_csv(new_lines, csv_doc) 

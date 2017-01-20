
import sys
import os

import docreader
import utils

eventdir = sys.argv[1]

all_files = os.listdir(eventdir)
txt_files = [x for x in all_files if x[-4:] == '.txt']
csv_files = [x for x in all_files if x[-4:] == '.csv']
txt_stripped = [x[:-4] for x in txt_files]
csv_stripped = [x[:-4] for x in csv_files]
txt_unique = list(set(txt_stripped) - set(csv_stripped))

fields = ['label', 'doc_id', 'author_id', 'date', 'time', 'authorname', 'text', 'tagged']
columndict = {0 : 'doc_id', 1 : 'author_id', 2 : 'authorname', 3 : 'date', 4 : 'time', 5 : 'text'}

while len(txt_unique) > 0:
    eventfile = txt_unique[0]
    print(eventfile)
    reader = docreader.Docreader()
    reader.parse_doc(eventdir + eventfile + '.txt', '\t', False, False, False)
    new_lines, other_lines = reader.set_lines(fields, columndict)
    csv_doc = eventdir + eventfile + '.csv'
    utils.write_csv(new_lines, csv_doc) 
    all_files = os.listdir(eventdir)
    txt_files = [x for x in all_files if x[-4:] == '.txt']
    csv_files = [x for x in all_files if x[-4:] == '.csv']
    txt_stripped = [x[:-4] for x in txt_files]
    csv_stripped = [x[:-4] for x in csv_files]
    txt_unique = list(set(txt_stripped) - set(csv_stripped))

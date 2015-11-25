
import sys
import os

import time_functions
import calculations

datadir = sys.argv[1]
tweetdir = sys.argv[2]

eventfiles = [x for x in os.listdir(datadir) if x[:8] == 'sequence']

for eventfile in eventfiles:
    with open(datadir + eventfile, 'r', encoding = 'utf-8') as sequence_in:
        lines = sequence_in.read().split('\n')
    event = lines[0]
    tokens = event.split('\t')
    event_terms = tokens[0].split(', ')
    event_date = time_functions.return_datetime(tokens[1], setting = 'vs')
    date_begin = time_functions.return_datetime(tokens[2][:10], setting = 'vs')
    date_end = time_functions.return_datetime(tokens[2][11:], setting = 'vs')
    position = (event_date - date_begin).days()
    for termsequence in lines[1:]:
        tokens = sequence[0]
        event_term = tokens[0]
        sequence = [int(x) for x in tokens[1].split()]
        burstiness = calculations.score_burstiness_sequence(sequence, position)
        print(event_term.encode('utf-8'), burstiness, position, event_date.date(), date_begin.date(), sequence) 

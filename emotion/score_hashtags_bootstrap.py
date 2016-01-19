
import sys
from collections import defaultdict

import docreader
from framework import calculations
import coco

positive = sys.argv[1]
negative = sys.argv[2]
outfile = sys.argv[3]

print('Reading in docs')
dr_pos = docreader.Docreader()
dr_pos.parse_doc(positive, delimiter = '\t', header = False)

dr_neg = docreader.Docreader()
dr_neg.parse_doc(negative, delimiter = '\t', header = False)

print('Counting hashtags')
fcs = calculations.count_tokens([line[0] for line in dr_pos.lines])
hts_pos = [str(fc[0]) for fc in calculations.count_tokens([line[0] for line in dr_pos.lines]) if fc[0][0] == '#' and int(fc[1]) >= 10]
print('Selected', len(hts_pos), 'candidate hashtags')

print('Identifying lines with hashtag')
all_lines = dr_pos.lines + dr_neg.lines
cc = coco.Coco('tmp/')
cc.set_lines([line[0] for line in all_lines])
cc.set_file()
cc.model_ngramperline(hts_pos)

print('Summing up hashtag score')
hashtag_average = {}
for hashtag in hts_pos:
    matches = cc.match([hashtag])[hashtag]
    score = 0
    for match in matches:
        line = all_lines[match]
        score += float(line[1])
    hashtag_average[hashtag] = score / len(matches) 
sorted_hashtags = sorted(hashtag_average, key = hashtag_average.get, reverse = True)
with open(outfile, 'w', encoding = 'utf-8') as out:
    for hashtag in sorted_hashtags:
        out.write(hashtag + '\t' + str(hashtag_average[hashtag]) + '\n')


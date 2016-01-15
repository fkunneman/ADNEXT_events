
import sys

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
hts_pos = [fc[0] for fc in calculations.count_tokens(dr_pos.lines) if fc[0][0] == '#' and fc[1] >= 10]
print('Selected', len(hts_pos), 'candidate hashtags')

print('Identifying lines with hashtag')
all_lines = dr_pos.lines + dr_neg.lines
cc = coco.Coco('tmp/')
cc.set_lines([line[0] for line in all_lines])
cc.set_file()
cc.model_ngramperline(hts_pos)

print('Summing up hashtag score')
hashtag_score = defaultdict(float)
for hashtag in hts_pos:
    print(hashtag.encode('utf-8'))
    matches = coco.match([hashtag])
    for match in matches:
        line = all_lines[match]
        print(line[0].encode('utf-8'))
        hashtag_score[hashtag] += float(line[1])
sorted_hashtags = sorted(hashtag_score, key = hashtag_score.get, reverse = True)
with open(outfile, 'w', encoding = 'utf-8'):
    for hashtag in sorted_hashtags:
        outfile.write(hashtag + '\t' + str(hashtag_score[hashtag]) + '\n')

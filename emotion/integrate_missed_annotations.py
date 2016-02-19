
import sys

import docreader
import linewriter

aligned_annotations = sys.argv[1]
new_annotations = sys.argv[2]
rank_file = sys.argv[3]
sheetname = sys.argv[4]
annotator_index = int(sys.argv[5])
outfile = sys.argv[6]

dr_aligned = docreader.Docreader()
dr_aligned.parse_doc(aligned_annotations)

dr_ranks = docreader.Docreader()
dr_ranks.parse_doc(rank_file)

dr_new = docreader.Docreader()
dr_new.parse_doc(new_annotations, sheet = sheetname)

new_annotations = [x[2] for x in dr_new.lines[1:]]
ranks = [x[0] for x in dr_ranks.lines[1:]]
ranks_annotations = zip(ranks, new_annotations)

aligned_annotations_completer = dr_aligned.lines

for ra in ranks_annotations:
    #print(ra[0] + 1, aligned_annotations_completer[int(ra[0]) + 1])
    aligned_annotations_completer[int(ra[0]) + 1][annotator_index] = ra[1]

lw = linewriter.Linewriter(aligned_annotations_completer[1:])
lw.write_xls(headers = ['tweet', 'classifier_score', 'AB', 'ES', 'FK'], 
    header_style = {'tweet' : 'general', 'classifier_score' : '0.00', 'AB' : 'general', 'ES' : 'general', 'FK' : 'general'},
    outfile = outfile)

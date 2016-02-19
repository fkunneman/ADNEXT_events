
import sys

import docreader
import annotation_calcs

annotation_file = sys.argv[1]
num_instances = int(sys.argv[2])
first_instance = int(sys.argv[3]) 
first_annotator = int(sys.argv[4]) # index in file
last_annotator = int(sys.argv[5]) # index in file
outfile = sys.argv[6]
plotout = sys.argv[7]

# parse annotationfile
dr = docreader.Docreader()
dr.parse_doc(annotation_file)
annotations = [l[first_annotator:last_annotator + 1] for l in dr.lines[first_instance:first_instance+num_instances]]

ac = annotation_calcs.Annotation_calculator(annotations)
ac.output_annotation_scores(outfile)
ac.plot_precision_at(plotout)

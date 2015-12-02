
import sys

import docreader
import coco

infile = sys.argv[1]
tmpdir = sys.argv[2]
outdir = sys.argv[3]
to_match = sys.argv[4:]

dr = docreader.Docreader()
lines = dr.parse_doc(infile)

textlines = [x[-1] for x in lines]
print(textlines[1].encode('utf-8'))

cc = coco.Coco(tmpdir)
cc.set_lines(textlines)
cc.set_file()
cc.model_ngramperline(to_match)
matches = cc.match(to_match)

print(matches)
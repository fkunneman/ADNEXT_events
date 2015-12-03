
import sys

import docreader # from ADNEXT_predict
import linewriter # from ADNEXT_collect
import coco # from ADNEXT_utils

infile = sys.argv[1]
tmpdir = sys.argv[2]
outdir = sys.argv[3]
to_match = sys.argv[4:]

dr = docreader.Docreader()
lines = dr.parse_csv(infile)

textlines = [x[-1] for x in lines]

cc = coco.Coco(tmpdir)
cc.set_lines(textlines)
cc.set_file()
cc.model_ngramperline(to_match)
matches = cc.match(to_match)

for key in matches.keys():
    outfile = outdir + key + '.txt'
    with open(outfile, 'w') as file_out:
        file_out.write('\n'.join([str(i) for i in matches[key]]))
    # selected = [lines[i] for i in matches[key]]
    # lw = linewriter.Linewriter(selected)
    # lw.write_csv(outfile)

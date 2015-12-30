
import sys

import docreader
import linewriter

fname = sys.argv[1]
#partsname = sys.argv[2]

drf = docreader.Docreader()
lines = drf.parse_csv(fname)
#drp = docreader.Docreader()
#drp.parse_txt(partsname, False, False)

lbefore = len(lines)
print('lines before', len(lines))
seen = []
keep = []
for i, l in enumerate(lines):
    tid = l[0]
    if not (set(tid) & set(seen)):
        keep.append(i)
        seen.append(tid)
#print(' '.join(seen).encode('utf-8'))
new_lines = [lines[i] for i in keep]
# new_lines_parts = [drp.lines[i] for i in keep]
print('lines after', len(new_lines))
if not len(new_lines) == lbefore:
    lwf = linewriter.Linewriter(new_lines)
    lwf.write_txt(fname)
#lwp = linewriter.Linewriter(new_lines_parts)
#lwp.write_txt(partsname)

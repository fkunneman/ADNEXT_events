
import sys

import docreader
import linewriter

fname = sys.argv[1]
partsname = sys.argv[2]

drf = docreader.Docreader()
drf.parse_csv(fname)
drp = docreader.Docreader()
drp.parse_txt(partsname, False, False)

print('lines before', len(drf.lines))
seen = []
keep = []
for i, l in enumerate(drf.lines):
    tid = l[0]
    if not (set(tid) & set(seen)):
        keep.append(i)
        seen.append(tid)
new_lines = [drf.lines[i] for i in keep]
new_lines_parts = [drp.lines[i] for i in keep]
print('lines after', len(new_lines))
lwf = linewriter.Linewriter(new_lines)
lwf.write_csv(fname)
lwp = linewriter.Linewriter(new_lines_parts)
lwp.write_txt(partsname)


import sys

import docreader
import linewriter
import calculations

datafile = sys.argv[1]
outfile = sys.argv[2]

dr = docreader.Docreader()
dr.parse_doc(datafile)

new_lines = []
for l in dr.lines[1:]:
    anticipation = float(l[5])
    disappointment = float(l[10])
    satisfaction = float(l[15])
    anticipointment = calculations.calculate_harmonic_mean([anticipation, disappointment])
    antisfaction = calculations.calculate_harmonic_mean([anticipation, satisfaction])
    l.extend([anticipointment, antisfaction])
    new_lines.append(l)

headers = ['event', '#zin', '0.5 percentile zin', '0.7 percentile zin', '0.8 percentile zin', '0.9 percentile zin', '#teleurgesteld', 
    '0.5 percentile teleurgesteld', '0.7 percentile teleurgesteld', '0.8 percentile teleurgesteld', '0.9 percentile teleurgesteld', '#tevreden',
    '0.5 percentile tevreden', '0.7 percentile tevreden', '0.8 percentile tevreden', '0.9 percentile tevreden', 'anticipointment 0.5', 'anticipointment 0.7', 'anticipointment 0.8', 
    'anticipointment 0.9', 'anticifaction 0.5', 'anticifaction 0.7', 'anticifaction 0.8', 'anticifaction 0.9', 'anticipointment', 'antisfaction']
header_style = {'event' : 'general', '#zin' : '0', '0.5 percentile zin' : '0.00', '0.7 percentile zin' : '0.00', 
    '0.8 percentile zin' : '0.00', '0.9 percentile zin' : '0.00', '#teleurgesteld' : '0', '0.5 percentile teleurgesteld' : '0.00',
    '0.7 percentile teleurgesteld' : '0.00', '0.8 percentile teleurgesteld' : '0.00', '0.9 percentile teleurgesteld' : '0.00', 
    '#tevreden' : '0', '0.5 percentile tevreden' : '0.00', '0.7 percentile tevreden' : '0.00', 
    '0.8 percentile tevreden' : '0.00', '0.9 percentile tevreden' : '0.00', 'anticipointment 0.5': '0.00', 
    'anticipointment 0.7': '0.00', 'anticipointment 0.8' : '0.00', 'anticipointment 0.9' : '0.00', 
    'anticifaction 0.5' : '0.00', 'anticifaction 0.7' : '0.00', 'anticifaction 0.8' : '0.00', 
    'anticifaction 0.9' : '0.00', 'anticipointment' : '0.00', 'antisfaction' : '0.00'}

lw = linewriter.Linewriter(new_lines)
lw.write_xls(headers, header_style, outfile)




import sys
import re

classifications_dir = sys.argv[1]
new_classifications_dir = sys.argv[2]
unique_events_file = sys.argv[3]
report_file = sys.argv[4]
keep_file = sys.argv[5]
emotion = sys.argv[6] #zin, teleurgesteld of tevreden

with open(unique_events_file) as ue:
    unique_events = ue.read().split('\n')

blacklist = []
keeps = []
for event in unique_events:
#    print(event)
    misplaced = []
    good = []
    try:
        with open(classifications_dir + event + '_' + emotion + '.txt', 'r', encoding = 'utf-8') as eo:
            lines = eo.readlines()
    except:
        continue
    event_terms = lines[0].split('\t')[0].split(', ')
    for i, tweet in enumerate(lines[1:]):
        match = False
        for et in event_terms:
            if not et == '*':
                if re.search('(^|\s)' + et + '($|\s)', tweet, re.IGNORECASE):
                    match = True
                    break
        if not match:
            misplaced.append(i)
        else:
            good.append(tweet)
#    if len(misplaced) > 0:
#        percent = len(misplaced) / len(lines[1:])
#        if percent > 0.8:
#            blacklist.append([event, percent])
#        else:
#            keeps.append(event)
#            with open(new_classifications_dir + event + '_' + emotion + '.txt', 'w', encoding = 'utf-8') as n_out:
#                n_out.write(''.join([lines[0]] + good)) 
#    else:
#        keeps.append(event)
    with open(new_classifications_dir + event + '_' + emotion + '.txt', 'w', encoding = 'utf-8') as n_out:
        n_out.write(''.join([lines[0]] + good)) 

with open(report_file, 'w') as ro:
    ro.write('\n'.join([' '.join([str(y) for y in x]) for x in blacklist]) + '\n')

with open(keep_file, 'w') as ko:
    ko.write('\n'.join(keeps))

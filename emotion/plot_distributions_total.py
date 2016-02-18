
import os
import sys
import matplotlib.pyplot as plt

import docreader

classificationdir = sys.argv[1]
plot_out = sys.argv[2]
event_threshold = int(sys.argv[3])

classifications = os.listdir(classificationdir)
events = list(set([x.split('_')[0] for x in classifications]))

zin_scores = []
tevreden_scores = []
teleurgesteld_scores = []
new_scores = []
for event in events:
    print(event)
    # zin
    try:
        dr_zin = docreader.Docreader()
        dr_zin.parse_doc(classificationdir + event + '_zin.txt')
    except:
        continue
    if len(dr_zin.lines) > event_threshold:
        zin_tweets = dr_zin.lines[1:]
        zin_scores.extend([float(tweet[0]) for tweet in zin_tweets])
        #plt.hist(zin_scores)
        #plt.savefig(plot_out + 'dist_zin_' + event + '.png')
        #plt.clf()
    # teleurgesteld
    try:
        dr_teleurgesteld = docreader.Docreader()
        dr_teleurgesteld.parse_doc(classificationdir + event + '_teleurgesteld.txt')
    except:
        continue
    if len(dr_teleurgesteld.lines) > event_threshold:
        teleurgesteld_tweets = dr_teleurgesteld.lines[1:]
        teleurgesteld_scores.extend([float(tweet[0]) for tweet in teleurgesteld_tweets])
        #plt.hist(teleurgesteld_scores)
        #plt.savefig(plot_out + 'dist_teleurgesteld_' + event + '.png')
        #plt.clf()
    # tevreden
    try:
        dr_tevreden = docreader.Docreader()
        dr_tevreden.parse_doc(classificationdir + event + '_tevreden.txt')
    except:
        continue
    if len(dr_tevreden.lines) > event_threshold:
        tevreden_tweets = dr_tevreden.lines[1:]
        tevreden_scores.extend([float(tweet[0]) for tweet in tevreden_tweets])
        #plt.hist(tevreden_scores)
        #plt.savefig(plot_out + 'dist_tevreden_' + event + '.png')
        #plt.clf()

plt.hist(zin_scores)
plt.savefig(plot_out + 'dist_tevreden.png')
plt.clf()

plt.hist(teleurgesteld_scores)
plt.savefig(plot_out + 'dist_tevreden.png')
plt.clf()

plt.hist(tevreden_scores)
plt.savefig(plot_out + 'dist_tevreden.png')
plt.clf()

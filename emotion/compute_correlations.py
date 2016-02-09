
import sys
from scipy.stats import linregress
from matplotlib import pyplot as plt

import docreader

event_scores = sys.argv[1]
freq_index_before = int(sys.argv[2])
freq_index_after = int(sys.argv[3])
x_index = int(sys.argv[4])
y_index = int(sys.argv[5])
z_index = int(sys.argv[6])
outdir = sys.argv[7]
lower_bound = int(sys.argv[8]) # 0 or real number
filtered_events = sys.argv[9]

with open(filtered_events) as fe_open:
    f_events = fe_open.read().split('\n')
    
steps = [1, 2, 5]
jumps = [1, 10, 100, 1000, 10000]

dr = docreader.Docreader()
dr.parse_doc(event_scores)

outputs = []
for jump in jumps:
    for step in steps:
        if lower_bound:
            if (step*jump) > lower_bound:
                threshold = step * jump
                print(threshold)
                lines = [l for l in dr.lines[1:] if l[freq_index_before] > lower_bound and l[freq_index_before] < upper_threshold and 
                    l[freq_index_after] > lower_bound and l[freq_index_after] < upper_threshold and (set(l[0]) & set(f_events))]
                output = [upper_threshold, len(lines)]
                x = [l[x_index] for l in lines]
                y = [l[y_index] for l in lines]
                z = [l[z_index] for l in lines]
            else:
                continue
        else:
            threshold = step * jump
            print(threshold)
            lines = [l for l in dr.lines[1:] if l[freq_index_before] > threshold and l[freq_index_after] > threshold and (set(l[0]) & set(f_events))]
            output = [threshold, len(lines)]
            x = [l[x_index] for l in lines]
            y = [l[y_index] for l in lines]
            z = [l[z_index] for l in lines]
        try:
            plt.scatter(x, y)
            plt.savefig(outdir + 'scatter_xy_' + str(threshold) + '.png')
            plt.clf()
            lr = linregress(x, y)
            output.append(lr[2])
            plt.scatter(x, z)
            plt.savefig(outdir + 'scatter_xz_' + str(threshold) + '.png')
            plt.clf()
            lr = linregress(x, z)
            output.append(lr[2])
            plt.scatter(y, z)
            plt.savefig(outdir + 'scatter_yz_' + str(threshold) + '.png')
            plt.clf()
            lr = linregress(y, z)
            output.append(lr[2])
            outputs.append(output)
        except ValueError:
            continue

with open(outdir + 'correlations.txt', 'w') as c_out:
    c_out.write('\n'.join(['\t'.join([str(k) for k in l]) for l in outputs]))

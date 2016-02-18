
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
                lines = [l for l in dr.lines[1:] if l[freq_index_before] > lower_bound and l[freq_index_before] < threshold and 
                    l[freq_index_after] > lower_bound and l[freq_index_after] < threshold]
                output = [threshold, len(lines)]
                ind = [[l[x_index], l[y_index], l[z_index]] for l in lines if l[x_index] != None and l[y_index] != None and l[z_index] != None]
                x = [l[0] for l in ind]
                y = [l[1] for l in ind]
                z = [l[2] for l in ind]
                sizes = [4 for l in ind]
            else:
                continue
        else:
            threshold = step * jump
            print(threshold)
            lines = [l for l in dr.lines[1:] if l[freq_index_before] > threshold and l[freq_index_after] > threshold]
            output = [threshold, len(lines)]
            ind = [[l[x_index], l[y_index], l[z_index]] for l in lines if l[x_index] != None and l[y_index] != None and l[z_index] != None]
            x = [l[0] for l in ind]
            y = [l[1] for l in ind]
            z = [l[2] for l in ind]
            sizes = [4 for l in ind]
        try:
            plt.scatter(x, y, s = sizes)
            plt.axis((0, 1, 0, 1))
            plt.savefig(outdir + 'scatter_xy_' + str(threshold) + '.png')
            plt.clf()
            lr = linregress(x, y)
            output.append(str(round(lr[2], 2)) + ' (' + str(round(lr[3], 2)) + ')')
            plt.scatter(x, z, s = sizes)
            plt.axis((0, 1, 0, 1))
            plt.savefig(outdir + 'scatter_xz_' + str(threshold) + '.png')
            plt.clf()
            lr = linregress(x, z)
            output.append(str(round(lr[2], 2)) + ' (' + str(round(lr[3], 2)) + ')')
            plt.scatter(y, z, s = sizes)
            plt.axis((0, 1, 0, 1))
            plt.savefig(outdir + 'scatter_yz_' + str(threshold) + '.png')
            plt.clf()
            lr = linregress(y, z)
            output.append(str(round(lr[2], 2)) + ' (' + str(round(lr[3], 2)) + ')')
            outputs.append(output)
        except ValueError:
            continue

with open(outdir + 'correlations.txt', 'w') as c_out:
    c_out.write('\n'.join(['\t'.join([str(k) for k in l]) for l in outputs]))


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

steps = [1, 2, 5]
jumps = [1, 10, 100, 1000, 10000]

dr = docreader.Docreader()
dr.parse_doc(event_scores)

outputs = []
for jump in jumps:
    for step in steps:
        threshold = step * jump
        print(threshold)
        lines = [l for l in dr.lines[1:] if l[freq_index_before] > threshold and l[freq_index_after] > threshold]
        output = [threshold, len(lines)]
        x = [l[x_index] for l in lines]
        y = [l[y_index] for l in lines]
        z = [l[z_index] for l in lines]
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
        print(output)
        outputs.append(output)
        quit()
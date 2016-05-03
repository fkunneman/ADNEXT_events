

import sys
import matplotlib.pyplot as plt

cfile_1 = sys.argv[1]
cfile_2 = sys.argv[2]
cfile_3 = sys.argv[3]
#cfile_4 = sys.argv[4]
#plotindex = int(sys.argv[5])
outname = sys.argv[4]
xlabel = sys.argv[5]
legend = sys.argv[6:]

def cfile_to_plotinput(cfile, plotindex):
    with open(cfile) as c_in:
        lines = c_in.read().split('\n')

    output = []
    for line in lines:
        tokens = line.split('\t')
        #if tokens[0] == '5000':
        #    break
        #else:
        output.append([tokens[0], tokens[1], tokens[plotindex].split()[0]])

    return output

plot1 = cfile_to_plotinput(cfile_1, 2)
plot2 = cfile_to_plotinput(cfile_2, 3)
plot3 = cfile_to_plotinput(cfile_3, 4)
#plot4 = cfile_to_plotinput(cfile_4)

x = [l[0] for l in plot1[:11]]
y1 = [l[2] for l in plot1[:11]]
y2 = [l[2] for l in plot2[:11]]
y3 = [l[2] for l in plot3[:11]]
#y4 = [l[2] for l in plot4]
x[0] = 0

#print(x, y1, y2, y3)
#quit()

plt.plot(x, y1, linestyle = '-', linewidth = 2)
plt.plot(x, y2, linestyle = '--', linewidth = 2)
plt.plot(x, y3, linestyle = ':', linewidth = 2)
#plt.plot(x, y4, linestyle = ':', linewidth = 2)
x1, x2, y1, y2 = plt.axis()
plt.gcf().subplots_adjust(bottom=0.15)
plt.axis((x1, x2, 0, 1))
plt.xscale('symlog')
plt.xlabel(xlabel, fontsize=16)
plt.ylabel('Correlation', fontsize=16)
plt.tick_params(axis = 'both', which = 'major', labelsize = 16)
plt.tick_params(axis = 'both', which = 'minor', labelsize = 16)
plt.legend(legend,  loc = "upper left")
plt.savefig(outname)

"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars
"""
import numpy as np
import matplotlib.pyplot as plt

N = 2
s1_means = (47.127, 11)
s1_std = (1.63550328645, 4)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, s1_means, width, color='r', yerr=s1_std)

s2_improve_means = (48, 48)
s2_improve_std = (1, 0)
rects2 = ax.bar(ind + width, s2_improve_means, width, color='y', yerr=s2_improve_std)

s2_worse_means = (1, 2)
s2_worse_std = (1, 0)
rects3 = ax.bar(ind + width+width, s2_worse_means, width, color='b', yerr=s2_worse_std)

# add some text for labels, title and axes ticks
ax.set_ylabel('Number of matches')
ax.set_title('Number of matches by distribution')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('Normal', 'Binomial'))

ax.legend((rects1[0], rects2[0], rects3[0]), ('Benefit +, No negative',
'Benefit +, Negative', 'Benefit -, Negative'))


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
plt.show()

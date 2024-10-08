import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

fig_params = {'axes.labelsize': 11.5,
              'font.family': 'serif',
              'font.size': 10,
              'lines.linewidth': 2.0,
              'legend.fontsize': 11,
              'xtick.labelsize': 10.5,
              'ytick.labelsize': 11,
              'figure.figsize': [9, 6],
              'figure.titlesize': 14.5,
              'savefig.format': 'png',
              'savefig.bbox': 'tight'}
plt.rcParams.update(fig_params)

palette = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE',  '#AA3377', '#BBBBBB'] #['#507fb5', '#b5507f', '#7fb550', '#b58650']
sns.set_palette(sns.color_palette(palette))

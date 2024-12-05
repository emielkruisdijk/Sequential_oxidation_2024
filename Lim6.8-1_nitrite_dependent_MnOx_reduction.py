# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:47:48 2024

@author: ekruisdijk
"""

import numpy as np
from matplotlib import pyplot as plt
import scipy
from pylab import *
import pandas as pd
import matplotlib as mpl
from matplotlib.offsetbox import AnchoredText
import datetime
import functools
import matplotlib.patches as patches
from matplotlib import cm
from numpy import linspace
import matplotlib.lines as mlines
from matplotlib.patches import Rectangle
import scipy.optimize as optimization
from matplotlib import ticker
from matplotlib.ticker import MaxNLocator
########################################################################
#STYLE

#Legend
mpl.rcParams['legend.numpoints']=1
mpl.rcParams['legend.handlelength']=1
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['legend.loc'] = 'best'
mpl.rcParams['legend.fontsize'] = 10
mpl.rcParams['axes.labelsize'] = 10
mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10
mpl.rcParams['font.size'] = 10

params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)
########################################################################
        
#Read data
df=pd.read_csv('WQ_data.csv', header= 0, skipinitialspace=True, sep=',')
oxy=pd.read_csv('O2_data.csv', header= 0, skipinitialspace=True, sep=';')
df_simc2=pd.read_csv('Lim6.8-1.txt', header= 0, skipinitialspace=True, sep='\t')
df_simc2_1=pd.read_csv('Lim6.8-2.txt', header= 0, skipinitialspace=True, sep='\t')

df=df.dropna()

df_simc2 = df_simc2[df_simc2['step'] == 195]
df_simc2_1 = df_simc2_1[df_simc2_1['step'] == 195]

df['Date'] =  pd.to_datetime(df['Date'], format='%d/%m/%Y')

Dates=[ pd.to_datetime('31-05-2023', format='%d-%m-%Y')] #pd.to_datetime('24-05-2023', format='%d-%m-%Y'),

locs=['Column 2', 'Column 3']

df10=df.loc[df['Name'].str.contains('Effluent VF21')]

f, (ax1, ax3)= plt.subplots(nrows=1, ncols=2, figsize=(8, 2.5))

for l in locs:
    if l == 'Column 2':
        df1=df.loc[df['Name'].str.contains(l)]
        
        custom_order = {'Column 2.3': 209, 'Column 2.5': 179, 'Column 2.6': 159, 'Column 2.7': 120, 'Column 2.8': 100, 'Column 2.9': 80, 'Column 2.10': 60, 'Column 2.11': 40, 'Column 2.12': 20, 'Effluent Column 2': 0}
        df1['Height'] = df1['Name'].map(custom_order)
        
        color=['k', 'm']
        
        for d,c in zip(Dates, color):
            df2=df1.loc[df['Date']==d] 
            ax1.plot(df2['mg NH4 / l']/18.039, df2['Height'], 'o', c=c, label=r"obs NH$_4^+$")#'obs NH$_4$$^+%$')
            ax1.plot(df2['mg NO3 / l']/62.004, df2['Height'], 'o', c='b', label=r"obs NO$_3^-$")#+'$^-%$')
            ax3.plot(df2['mg Mn/l']/54.938, df2['Height'], 'o', c=c, label=r"obs Mn$^{2+}$")
            
            ax1.plot(df_simc2['Amm'].head(-1)*1000, 195-df_simc2['dist_x'].head(-1), '--', c='k', label='sim NH$_4^+$')
            ax1.plot(df_simc2['NO3'].head(-1)*1000, 195-df_simc2['dist_x'].head(-1), '--', c='c', label='sim NO$_3^-$')
            ax1.plot(df_simc2['NO2'].head(-1)*1000, 195-df_simc2['dist_x'].head(-1), '--', c='g', label='sim NO$_2^-$')
            ax1.plot((df_simc2['NO3'].head(-1)*1000+df_simc2['NO2'].head(-1)*1000), 195-df_simc2['dist_x'].head(-1), '--', c='b', label='sim NO$_3^-$\n+NO$_2^-$')
            ax3.plot(df_simc2['Mn_di'].head(-1)*1000, 195-df_simc2['dist_x'].head(-1), '--', c='k', label=r"sim Mn$^{2+}$")
                      
            ax1.set_ylabel('Depth (cm)')
        
ax1.grid()
ax3.grid()


ax1.set_ylim(0, 209)
ax3.set_ylim(0, 209)

ax1.set_xlim(0, 0.2)
ax3.set_xlim(0, 0.010)

ax1.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax3.xaxis.set_major_locator(MaxNLocator(nbins=3))

ax1.tick_params('x', labelrotation=45)
ax3.tick_params('x', labelrotation=45)

# Define background rectangles
bg_colors = ['#27aae1', '#ffcf34']
for i, ax in enumerate([ax1, ax3]):
    middle_bg = patches.Rectangle((0, 209), width=100, height=-14, 
                                   facecolor=bg_colors[0],  # Alternate colors between yellow and blue
                                   edgecolor='none',
                                   zorder=0)
    bottom_bg = patches.Rectangle((0, 195), width=100, height=-195, 
                                   facecolor=bg_colors[1],  # Alternate colors between yellow and blue
                                   edgecolor='none',
                                   zorder=0)
    ax.add_patch(middle_bg)
    ax.add_patch(bottom_bg)
                  
plt.subplots_adjust(hspace=0.65,wspace=0.2)

ax1.legend(loc='best', fontsize=8)
ax3.legend(loc='best', fontsize=8)

plt.savefig('Lim6.8-1_nitrite_dependent_MnOx_reduction.png',bbox_inches='tight', dpi=300)
 
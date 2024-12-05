# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:47:48 2024

@author: ekruisdijk
"""

from matplotlib import pyplot as plt
import pandas as pd
import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib.ticker import MaxNLocator
########################################################################
#STYLE

#Legend
mpl.rcParams['legend.numpoints']=1
mpl.rcParams['legend.handlelength']=2
#mpl.legend(loc='best', frameon=True)
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
df_sim=pd.read_csv('AER8.txt', header= 0, skipinitialspace=True, sep='\t')

df=df.dropna()

df_sim = df_sim[df_sim['step'] == 195]

df['Date'] =  pd.to_datetime(df['Date'], format='%d/%m/%Y')

Dates=[pd.to_datetime('31-05-2023', format='%d-%m-%Y')]

locs=['Column 1']

df10=df.loc[df['Name'].str.contains('Effluent VF21')]

f, (ax1, ax2, ax3, ax4)= plt.subplots(nrows=1, ncols=4, figsize=(6, 1.2))

for l in locs:
    if l == 'Column 1':
        df1=df.loc[df['Name'].str.contains(l)]
        
        custom_order = {'Column 1.1': 220, 'Column 1.3': 209, 'Column 1.5': 179, 'Column 1.6': 159, 'Column 1.7': 120, 'Column 1.8': 100, 'Column 1.9': 80, 'Column 1.10': 60, 'Column 1.11': 40, 'Column 1.12': 20, 'Effluent Column 1': 0}
        df1['Height'] = df1['Name'].map(custom_order)
        
        color=['k', 'm', 'r']
        
        for d,c in zip(Dates, color):
            df2=df1.loc[df['Date']==d]               
            
            ax1.plot(df2['mg NH4 / l']/18.039, df2['Height'], 'o', c=c)
            ax1.plot(df2['mg NO3 / l']/62.004, df2['Height'], 'o', c='b')
            ax2.plot(df2['mg Mn/l']/54.938, df2['Height'], 'o', c=c, label='Mn')
            
            ax1.plot(df_sim['Amm'].head(-1)*1000, 195-df_sim['dist_x'].head(-1), '--', c='k', label='NH$_4$')
            #ax1.plot(df_sim['NO2'].head(-1)*1000, 195-df_sim['dist_x'].head(-1), '--', c='g', label='NO$_2$')
            ax1.plot(df_sim['NO3'].head(-1)*1000, 195-df_sim['dist_x'].head(-1), '--', c='b', label='NO$_3$')
            #ax1.plot((df_sim['NO3'].head(-1)+df_sim['NO2'].head(-1))*1000, 195-df_sim['dist_x'].head(-1), '--', c='r', label='NO$_3$')
            
            ax2.plot(df_sim['Mn_di'].head(-1)*1000, 195-df_sim['dist_x'].head(-1), '--', c='k')
            
            # Convert timestamp to string
            timestamp_str = d.strftime('%d')
            
            oxy2= oxy.columns[oxy.columns.str.contains(timestamp_str) & oxy.columns.str.contains(l[0] + l[-1])]
            
            print(oxy2)
            
            ax3.plot(oxy[oxy2]/32, oxy['Height'], 'o', c=c, label='Measured')
            #ax3.plot(df2['mg O2/l']/32, df2['Height'], 'o', c='k')
            ax4.plot(df2['pH'], df2['Height'], 'o', c=c, label='pH')
            
            ax3.plot(df_sim['O2'].head(-1)*1000, 195-df_sim['dist_x'].head(-1), '--', c='k', label='Simulated')
            ax4.plot(df_sim['_pH'].head(-1), 195-df_sim['dist_x'].head(-1), '--', c='k')
            
            ax1.set_title('NH$_4$ and NO$_3$ \n(mmol/L)')
            ax2.set_title('Mn\n(mmol/L)')
            ax3.set_title('O$_2$\n(mmol/L)')
            ax4.set_title('pH\n(-)')
            

            
            ax1.set_xlim(0, 0.2)
            ax2.set_xlim(0, 0.004)
            ax3.set_xlim(0, 0.4)
            ax4.set_xlim(6.5,8)
            
            ax2.tick_params(labelleft=False, left=False)
            ax3.tick_params(labelleft=False, left=False)
            ax4.tick_params(labelleft=False, left=False)
            
            ax1.set_ylabel('Depth (cm)')



ax1.set_ylim(0, 209)
ax2.set_ylim(0, 209)
ax3.set_ylim(0, 209)
ax4.set_ylim(0, 209)


ax1.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax2.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax3.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax4.xaxis.set_major_locator(MaxNLocator(nbins=3))

# Define background rectangles
bg_colors = ['#27aae1', '#ffcf34']
for i, ax in enumerate([ax1, ax2, ax3, ax4]):
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


ax1.text(-0.9, 0.5, 'AER8', fontsize=16, transform=ax1.transAxes, horizontalalignment='center', verticalalignment='center', rotation=90)

ax1.grid()
ax2.grid()
ax3.grid()
ax4.grid()

ax1.tick_params('x', labelrotation=45)
ax2.tick_params('x', labelrotation=45)
ax3.tick_params('x', labelrotation=45)
ax4.tick_params('x', labelrotation=45)
  
                  
plt.subplots_adjust(hspace=0.6,wspace=0.3)

ax1.legend(loc='best', fontsize=6)

ax3.legend(loc='upper center', bbox_to_anchor=(-0.5, -0.60), ncol=5, fontsize=10)    

plt.savefig('AER8.png',bbox_inches='tight', dpi=300)
 

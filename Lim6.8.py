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
mpl.rcParams['legend.handlelength']=1
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
#plt.style.use('ggplot')
########################################################################
        
#Read data
df=pd.read_csv('WQ_data.csv', header= 0, skipinitialspace=True, sep=',')
oxy=pd.read_csv('O2_data.csv', header= 0, skipinitialspace=True, sep=';')
df_simc2=pd.read_csv('Lim6.8-1.txt', header= 0, skipinitialspace=True, sep='\t')
#df_sim_opt=pd.read_csv(r'C:\Users\ekruisdijk\OneDrive - Delft University of Technology\Documents\Work\VIDI - Arsenic Removal\Work\Pilot Hammerflier\04_Models\Final models\C2\C2 v2_optimized.txt', header= 0, skipinitialspace=True, sep='\t')
df_simc3=pd.read_csv('Lim6.8-2.txt', header= 0, skipinitialspace=True, sep='\t')


df_simc2 = df_simc2[df_simc2['step'] == 195]
#df_sim_opt = df_sim_opt[df_sim_opt['step'] == 195]
df_simc3 = df_simc3[df_simc3['step'] == 195]

df=df.dropna()

df['Date'] =  pd.to_datetime(df['Date'], format='%d/%m/%Y')

Dates=[ pd.to_datetime('31-05-2023', format='%d-%m-%Y')] #pd.to_datetime('24-05-2023', format='%d-%m-%Y'),

locs=['Column 2', 'Column 3']

df10=df.loc[df['Name'].str.contains('Effluent VF21')]

f, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8))= plt.subplots(nrows=2, ncols=4, figsize=(6, 3))

for l in locs:
    if l == 'Column 2':
        df1=df.loc[df['Name'].str.contains(l)]
        
        custom_order = {'Column 2.3': 209, 'Column 2.5': 179, 'Column 2.6': 159, 'Column 2.7': 120, 'Column 2.8': 100, 'Column 2.9': 80, 'Column 2.10': 60, 'Column 2.11': 40, 'Column 2.12': 20, 'Effluent Column 2': 0}
        df1['Height'] = df1['Name'].map(custom_order)
        
        color=['k', 'm']
        
        for d,c in zip(Dates, color):
            df2=df1.loc[df['Date']==d] 
            ax1.plot(df2['mg NH4 / l']/18.039, df2['Height'], 'o', c=c)
            ax1.plot(df2['mg NO3 / l']/62.004, df2['Height'], 'o', c='b')
            ax2.plot(df2['mg Mn/l']/54.938, df2['Height'], 'o', c=c, label='Mn')
            
            ax1.plot(df_simc2['Amm'].head(-1)*1000, 195-df_simc2['dist_x'].head(-1), '--', c='k', label='NH$_4$')
            #ax1.plot(df_simc2['NO3'].head(-1)*1000, 195-df_simc2['dist_x'].head(-1), '--', c='c', label='NO$_3$')
            #ax1.plot(df_simc2['NO2'].head(-1)*1000, 195-df_simc2['dist_x'].head(-1), '--', c='g', label='NO$_2$')
            ax1.plot((df_simc2['NO3'].head(-1)*1000+df_simc2['NO2'].head(-1)*1000), 195-df_simc2['dist_x'].head(-1), '--', c='b', label='NO$_3$')
            ax2.plot(df_simc2['Mn_di'].head(-1)*1000, 195-df_simc2['dist_x'].head(-1), '--', c='k')
            
#            ax1.plot(df_sim_opt['Amm'].head(-1)*1000, 195-df_sim_opt['dist_x'].head(-1), ':', c='k')
#            ax1.plot(df_sim_opt['NO3'].head(-1)*1000, 195-df_sim_opt['dist_x'].head(-1), ':', c='b')
#            ax1.plot(df_sim_opt['NO2'].head(-1)*1000, 195-df_sim_opt['dist_x'].head(-1), ':', c='g')
#            ax2.plot(df_sim_opt['Mn_di'].head(-1)*1000, 195-df_sim_opt['dist_x'].head(-1), ':', c='k')
            
            
            # Convert timestamp to string
            timestamp_str = d.strftime('%d')
            
            oxy2= oxy.columns[oxy.columns.str.contains(timestamp_str) & oxy.columns.str.contains(l[0] + l[-1])]
                        
            ax3.plot(oxy[oxy2]/32, oxy['Height'], 'o', c=c, label='Observed') ### change O2 range to measured in field
            #ax3.plot(df2['mg O2/l']/32, df2['Height'], 'o', c='b', label='O2') ### change O2 range to measured in field
            ax4.plot(df2['pH'], df2['Height'], 'o', c=c, label='pH')
                        
            ax3.plot(df_simc2['O2'].head(-1)*1000, 195-df_simc2['dist_x'].head(-1), '--', c='k', label='Simulated')
            ax4.plot(df_simc2['_pH'].head(-1), 195-df_simc2['dist_x'].head(-1), '--', c='k')
            
#            ax3.plot(df_sim_opt['O2'].head(-1)*1000, 195-df_sim_opt['dist_x'].head(-1), ':', c='k', label='Optimized')
#            ax4.plot(df_sim_opt['_pH'].head(-1), 195-df_sim_opt['dist_x'].head(-1), ':', c='k')
            
            ax1.set_title('NH$_4$ and NO$_3$\n(mmol/L)')
            ax2.set_title('Mn\n(mmol/L)')
            ax3.set_title('O$_2$\n(mmol/L)')
            ax4.set_title('pH\n(-)')
                        
            ax1.set_xlim(0, 0.2)
            ax2.set_xlim(0, 0.010)
            ax3.set_xlim(0, 0.2)
            ax4.set_xlim(6.5,8)
            
            ax2.tick_params(labelleft=False, left=False)
            ax3.tick_params(labelleft=False, left=False)
            ax4.tick_params(labelleft=False, left=False)
            
            ax1.set_ylabel('Depth (cm)')
        
    elif l == 'Column 3':
    
        df1=df.loc[df['Name'].str.contains('Column 3')]  
        
        custom_order = {'Column 3.3': 209, 'Column 3.5': 179, 'Column 3.6': 159, 'Column 3.7': 120, 'Column 3.8': 100, 'Effluent Column 3': 0}
        
        df1['Height'] = df1['Name'].map(custom_order)
        
        color=['k', 'm']
        
        for d,c in zip(Dates, color):
            df2=df1.loc[df['Date']==d] 
            ax5.plot(df2['mg NH4 / l']/18.039, df2['Height'], 'o', c=c, label='NH4')
            ax5.plot(df2['mg NO3 / l']/62.004, df2['Height'], 'o', c='b', label='NO3')
            ax6.plot(df2['mg Mn/l']/54.938, df2['Height'], 'o', c=c, label='Mn')
            
            ax5.plot(df_simc3['Amm'].head(-1)*1000, 195-df_simc3['dist_x'].head(-1), '--', c='k')
            ax5.plot(df_simc3['NO3'].head(-1)*1000, 195-df_simc3['dist_x'].head(-1), '--', c='b')
            ax6.plot(df_simc3['Mn_di'].head(-1)*1000, 195-df_simc3['dist_x'].head(-1), '--', c='k')
            # Convert timestamp to string
            timestamp_str = d.strftime('%d')
            
            oxy2= oxy.columns[oxy.columns.str.contains(timestamp_str) & oxy.columns.str.contains(l[0] + l[-1])]            
            #oxy_nan = oxy[oxy[oxy2].notna()]
            oxy_nan=oxy.dropna(subset=oxy2)
            
            ax7.plot(oxy_nan[oxy2]/32, oxy_nan['Height'], 'o', c=c) ### change O2 range to measured in field
            #ax7.plot(df2['mg O2/l']/32, df2['Height'], 'o', c='b', label=str(d)[:10]) ### change O2 range to measured in field
            ax8.plot(df2['pH'], df2['Height'], 'o', c=c, label='pH')
            
            ax7.plot(df_simc3['O2'].head(-1)*1000, 195-df_simc3['dist_x'].head(-1), '--', c='k')
            ax8.plot(df_simc3['_pH'].head(-1), 195-df_simc3['dist_x'].head(-1), '--', c='k')
            
            ax5.set_xlim(0, 0.2)
            ax6.set_xlim(0, 0.010)
            ax7.set_xlim(0, 0.4)
            ax8.set_xlim(6.5,8)
            
            ax6.tick_params(labelleft=False, left=False)
            ax7.tick_params(labelleft=False, left=False)
            ax8.tick_params(labelleft=False, left=False)
            
            ax5.set_ylabel('Depth (cm)')

ax1.grid()
ax2.grid()
ax3.grid()
ax4.grid()
ax5.grid()
ax6.grid()
ax7.grid()
ax8.grid()

ax1.set_ylim(0, 209)
ax2.set_ylim(0, 209)
ax3.set_ylim(0, 209)
ax4.set_ylim(0, 209)
ax5.set_ylim(0, 209)
ax6.set_ylim(0, 209)
ax7.set_ylim(0, 209)
ax8.set_ylim(0, 209) 

ax1.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax2.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax3.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax4.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax5.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax6.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax7.xaxis.set_major_locator(MaxNLocator(nbins=3))
ax8.xaxis.set_major_locator(MaxNLocator(nbins=3))


ax1.tick_params('x', labelrotation=45)
ax2.tick_params('x', labelrotation=45)
ax3.tick_params('x', labelrotation=45)
ax4.tick_params('x', labelrotation=45)
ax5.tick_params('x', labelrotation=45)
ax6.tick_params('x', labelrotation=45)
ax7.tick_params('x', labelrotation=45)
ax8.tick_params('x', labelrotation=45)

# Define background rectangles
bg_colors = ['#27aae1', '#ffcf34']
for i, ax in enumerate([ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]):
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


ax1.text(-0.9, 0.5, 'LIM6.8-1', fontsize=16, transform=ax1.transAxes, horizontalalignment='center', verticalalignment='center', rotation=90)
ax5.text(-0.9, 0.5, 'LIM6.8-2', fontsize=16, transform=ax5.transAxes, horizontalalignment='center', verticalalignment='center', rotation=90)

ax3.text(-0.2, -0.7, 'Water is aerated before entering LIM6.8-2', fontsize=11, transform=ax3.transAxes, horizontalalignment='center', verticalalignment='center')
     
                  
plt.subplots_adjust(hspace=0.8,wspace=0.3)

#ax2.text(0.8, 1.6, str(d)[:10], fontsize=14, transform=ax2.transAxes, horizontalalignment='center', verticalalignment='center')  
ax1.legend(loc='best', fontsize=6)

ax3.legend(loc='upper center', bbox_to_anchor=(-0.5, -2.4), ncol=5, fontsize=10)    

plt.savefig('C:/Users/kruisdem/OneDrive - Delft University of Technology/Documents/Work/VIDI - Arsenic Removal/Work/Pilot Hammerflier/02_Data_sampling/Figures/Manuscript/C2+C3 v3.png',bbox_inches='tight', dpi=300)
 

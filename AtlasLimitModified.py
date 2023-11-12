import json
import argparse
import glob
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import atlas_mpl_style as ampl
import matplotlib.patheffects as path_effects
import pathlib
import glob

limits = pd.read_json('Atlas2023Limits.json')
print(limits) 
print(limits["X1000_S110"])
print("====================")
print((limits["X1000_S110"])[2])


## FIRST ELEMENT ADDED TWICE, REMEMBER
#for element in limits:
#    print(element)
#    print((limits[element])[3]) # prints column titles i.e for example X1000_S110 etc.
##    print(element[1])


mx = []
ms = []
limit_obs = []
limit_exp = []

for element in limits:
    mx.append((limits[element])[0])
    ms.append((limits[element])[1])
    limit_exp.append((limits[element])[2])
    limit_obs.append((limits[element])[3])

mx = np.array(mx)
ms = np.array(ms)
limit_exp = np.array(limit_exp)
limit_obs = np.array(limit_obs)

#x_min = ms.min()
#x_max = ms.max()
x_min, x_max = mx.min(), mx.max()
y_min, y_max = ms.min(), ms.max()
grid_x, grid_y = np.mgrid[x_min:x_max:100j, y_min:y_max:200j]
## Interpolate the limits on the grid
#    if args.observed:
grid_limit = griddata((mx, ms), limit_obs, (grid_x, grid_y), method='cubic')
#    else:
#        grid_limit = griddata(limits[['x', 'y']], limits['limit_exp_0'], (grid_x, grid_y), method='cubic')


ampl.use_atlas_style() # activate ATLAS style    
fig, ax = plt.subplots()
# transpose the data from mgrid (.T)
#im = ax.imshow(grid_limit.T, extent=(x_min,x_max,y_min,y_max), origin='lower', aspect='auto', cmap='viridis')#args.cmap, 
plotxmin, plotxmax = 150, 420
plotymin, plotymax = 0, 300
#im = ax.imshow(grid_limit.T, extent=(plotxmin, plotxmax, plotymin, plotymax), origin='lower', aspect='auto', cmap='viridis',#args.cmap, 
#im = ax.imshow(grid_limit.T, extent=(x_min, x_max, y_min, y_max), origin='lower', aspect='auto', cmap='viridis',#args.cmap, 
im = ax.imshow(grid_limit.T, origin='lower', aspect='auto', cmap='viridis',#args.cmap, 
               #norm=LogNorm(), if args.log else None, 
               vmin=0,#args.z_lim[0], if args.z_lim else None, 
               vmax=14)#args.z_lim[1]) if args.z_lim else None)
cbar = fig.colorbar(im, ax=ax)

    ## Remove values outside the grid                                                                                                         
#    if args.x_lim:
#        limits = limits[limits['x'] > args.x_lim[0]]
#        limits = limits[limits['x'] < args.x_lim[1]]

#    if args.y_lim:
#        limits = limits[limits['y'] > args.y_lim[0]]
#        limits = limits[limits['y'] < args.y_lim[1]]


#    print(limits)

    ## print the limit on the plot
#    if args.text:
#        for index, row in limits.iterrows():

#            if args.observed:
#                text = ax.text(row['x'], row['y'], f"{row['limit_obs']:0.2f}",
#                           color="black", ha="left", va="bottom")
#            else:
#                text = ax.text(row['x'], row['y'], f"{row['limit_exp_0']:0.2f}", 
#                           color="black", ha="left", va="bottom")
#            text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='white'),
#                                   path_effects.Normal()])

    ## draw atlas label
#    ampl.draw_atlas_label(0.05, 0.92, ax=ax, status='int', fontsize=20)
#    if args.label:
#        for i, t in enumerate(args.label):
#            ax.text(0.05, 0.89-((i+1)*0.05), t, transform=ax.transAxes)
ampl.set_ylabel("$m_S$ [GeV]", ax=ax)
ampl.set_xlabel("$m_X$ [GeV]", ax=ax)
ampl.set_zlabel(r'$\sigma( pp \rightarrow X)\times$ BR$ (X \rightarrow SH  \rightarrow bb \gamma \gamma)$ [fb]', ax=ax, cbar=cbar)

#    if args.x_lim: ax.set_xlim(args.x_lim[0], args.x_lim[1])
#    if args.y_lim: ax.set_ylim(args.y_lim[0], args.y_lim[1])

plt.tight_layout()


## create the dir if it does not exist
#    pathlib.Path(args.output_dir).mkdir(parents=True, exist_ok=True)
## save the png
fig.savefig("AtlasMassplottTest.png", format='png')


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
#print(limits) 
#print(limits["X1000_S110"])
#print("====================")
#print((limits["X1000_S110"])[2])


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

print(mx[0:10])
print("====================")
print(ms[0:10])
print("====================")
print(limit_exp[0:10])
print("====================")
print(limit_obs[0:10])

"""
mx = np.array(mx)
ms = np.array(ms)
limit_exp = np.array(limit_exp)
limit_obs = np.array(limit_obs)

x_min, x_max = mx.min(), mx.max()
y_min, y_max = ms.min(), ms.max()
grid_x, grid_y = np.mgrid[x_min:x_max:100j, y_min:y_max:200j]

## Interpolate the limits on the grid
grid_limit = griddata((mx, ms), limit_obs, (grid_x, grid_y), method='cubic')


ampl.use_atlas_style() # activate ATLAS style    
fig, ax = plt.subplots()

# transpose the data from mgrid (.T)
im = ax.imshow(grid_limit.T, origin='lower', aspect='auto', cmap='viridis', 
vmin=0, vmax=15)

cbar = fig.colorbar(im, ax=ax)

plotxmin, plotxmax = 160, 420
plotymin, plotymax = 0, 300
ax.set_xlim(plotxmin, plotxmax)
ax.set_ylim(plotymin, plotymax)


# draw atlas label
ampl.draw_atlas_label(0.05, 0.92, ax=ax, status='int', fontsize=20)
if args.label:
    for i, t in enumerate(args.label):
        ax.text(0.05, 0.89-((i+1)*0.05), t, transform=ax.transAxes)
ampl.set_ylabel("$m_S$ [GeV]", ax=ax)
ampl.set_xlabel("$m_X$ [GeV]", ax=ax)
ampl.set_zlabel(r'$\sigma( pp \rightarrow X)\times$ BR$ (X \rightarrow SH  \rightarrow bb \gamma \gamma)$ [fb]', ax=ax, cbar=cbar)

plt.tight_layout()

fig.savefig("AtlasMassplottTest.png", format='png')
"""

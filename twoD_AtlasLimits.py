import json
import argparse
import glob
import pandas
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib
import atlas_mpl_style as ampl
import pathlib
import glob
import matplotlib.ticker as mticker



norm = (31.02 * 0.0026)


limits = pandas.read_json('Atlas2023Limits.json')
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

x_min, x_max = mx.min(), mx.max()
y_min, y_max = ms.min(), ms.max()
#grid_x, grid_y = np.mgrid[x_min:x_max:100j, y_min:y_max:200j]
#grid_x, grid_y = np.meshgrid[x_min:x_max:100j, y_min:y_max:200j]
# xi, yi = np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 200)
# grid_x, grid_y = np.meshgrid(xi, yi)

# ## Interpolate the limits on the grid
# grid_limit = griddata((mx, ms), limit_obs, (grid_x, grid_y), method='cubic')


### Lowmass:

BP2_xi_verif, BP2_yi_verif = np.linspace(ms.min(), ms.max(), 200), np.linspace(mx.min(), mx.max(), 100)
BP2_grid_x_verif, BP2_grid_y_verif = np.meshgrid(BP2_xi_verif, BP2_yi_verif)

## BP2 Interpolate the limits on the grid
BP2_grid_limit_verif = griddata((ms, mx), limit_obs/norm, (BP2_grid_x_verif, BP2_grid_y_verif), method='cubic') 
# cubic does exclude a small region around (100, 275) but I believe that is just the interpolation playing tricks,
# because if you examine the datapoints (scatter plot below) you will see that all the data points are way above the  mass plots
# i.e nothing excluded


plt.imshow(BP2_grid_limit_verif,  origin='lower', vmin=0/norm, vmax=15/norm,
                extent=[ms.min(), ms.max(), mx.min(), mx.max()], aspect='auto')
                # extent=[BP2_x_min, BP2_x_max, BP2_y_min, BP2_y_max], aspect='auto')


#### create legends for BP2 and BP3 regions
###############################################################################
class AnyObject1:
    pass


class AnyObjectHandler1:
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = matplotlib.patches.Rectangle([x0, y0], width, height, facecolor='none',
                                   edgecolor='red', hatch='//', lw=1,
                                   transform=handlebox.get_transform())
        handlebox.add_artist(patch)
        return patch

class AnyObject2:
    pass


class AnyObjectHandler2:
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = matplotlib.patches.Rectangle([x0, y0], width, height, facecolor='none',
                                   edgecolor='blue', hatch='//', lw=1,
                                   transform=handlebox.get_transform())
        handlebox.add_artist(patch)
        return patch

plt.legend([AnyObject1(), AnyObject2()], ['BP2 mass region', 'BP3 mass region'], handler_map={AnyObject1: AnyObjectHandler1(), AnyObject2: AnyObjectHandler2()})


# BP2
plt.gca().add_patch(matplotlib.patches.Rectangle((1,126),123,374,linewidth=1,edgecolor='r',facecolor='none', hatch = '/'))
# BP3
plt.gca().add_patch(matplotlib.patches.Rectangle((126,255),374,395,linewidth=1,edgecolor='b',facecolor='none', hatch = '/'))
###############################################################################


plt.xlim(0, 300)
plt.ylim(160, 420)

# create a better x label
# from stackexchange: https://stackoverflow.com/a/49239362/17456342
ax = plt.gca()
ax.xaxis.set_minor_locator(mticker.FixedLocator(( 124/2, (126 + 300)/2 )))
ax.xaxis.set_minor_formatter(mticker.FixedFormatter((r"$M_{1}$ [GeV]", r"$M_{2}$ [GeV]")))
plt.setp(ax.xaxis.get_minorticklabels(), rotation=0, size=10, va="center")
ax.tick_params("x",which="minor",pad=25, left=False)

plt.ylabel(r'$M_{3}$ [GeV]')
plt.title(r'Upper limits at 95% C.L normalized, low mass')

plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{3}} \cdot \mathrm{BR}_{h_{3} \ \to \ h_{1,2}(b\bar{b}) \ h_{2,1}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )

plt.tight_layout()
plt.savefig("thesisAuxiliaryData/AtlasMassplotTest2_lowmass.png", format='png')
plt.savefig("thesisAuxiliaryData/AtlasMassplotTest2_lowmass.pdf")

plt.show()
plt.close()



### Highmass:

BP3_xi_verif, BP3_yi_verif = np.linspace(ms.min(), ms.max(), 200), np.linspace(mx.min(), mx.max(), 100)
BP3_grid_x_verif, BP3_grid_y_verif = np.meshgrid(BP3_xi_verif, BP3_yi_verif)

## BP3 Interpolate the limits on the grid
BP3_grid_limit_verif = griddata((ms, mx), limit_obs/norm, (BP3_grid_x_verif, BP3_grid_y_verif), method='cubic')

plt.imshow(BP3_grid_limit_verif,  origin='lower', vmin=0/norm, vmax=1/norm,
                extent=[ms.min(), ms.max(), mx.min(), mx.max()], aspect='auto')
                # extent=[BP3_x_min, BP3_x_max, BP3_y_min, BP3_y_max], aspect='auto')


#### create legends for BP2 and BP3 regions
###############################################################################
class AnyObject1:
    pass


class AnyObjectHandler1:
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = matplotlib.patches.Rectangle([x0, y0], width, height, facecolor='none',
                                   edgecolor='red', hatch='//', lw=1,
                                   transform=handlebox.get_transform())
        handlebox.add_artist(patch)
        return patch

class AnyObject2:
    pass


class AnyObjectHandler2:
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = matplotlib.patches.Rectangle([x0, y0], width, height, facecolor='none',
                                   edgecolor='blue', hatch='//', lw=1,
                                   transform=handlebox.get_transform())
        handlebox.add_artist(patch)
        return patch

plt.legend([AnyObject1(), AnyObject2()], ['BP2 mass region', 'BP3 mass region'], handler_map={AnyObject1: AnyObjectHandler1(), AnyObject2: AnyObjectHandler2()})

# BP2
plt.gca().add_patch(matplotlib.patches.Rectangle((1,126),123,374,linewidth=1,edgecolor='r',facecolor='none', hatch = '/'))
# BP3
plt.gca().add_patch(matplotlib.patches.Rectangle((126,255),374,395,linewidth=1,edgecolor='b',facecolor='none', hatch = '/'))
###############################################################################


plt.xlim(0, 545)
plt.ylim(420, 1020)

# create a better x label
# from stackexchange: https://stackoverflow.com/a/49239362/17456342
ax = plt.gca()
ax.xaxis.set_minor_locator(mticker.FixedLocator(( 124/2, (126 + 500)/2 )))
ax.xaxis.set_minor_formatter(mticker.FixedFormatter((r"$M_{1}$ [GeV]", r"$M_{2}$ [GeV]")))
plt.setp(ax.xaxis.get_minorticklabels(), rotation=0, size=10, va="center")
ax.tick_params("x",which="minor",pad=25, left=False)

plt.ylabel(r'$M_{3}$ [GeV]')

plt.title(r'Upper limits at 95% C.L normalized, high mass')

plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{3}} \cdot \mathrm{BR}_{h_{3} \ \to \ h_{1,2}(b\bar{b}) \ h_{2,1}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )

plt.tight_layout()
plt.savefig("thesisAuxiliaryData/AtlasMassplotTest2_highmass.png", format='png')
plt.savefig("thesisAuxiliaryData/AtlasMassplotTest2_highmass.pdf")

plt.show()
plt.close()




### mass range BP2:

plt.imshow(BP2_grid_limit_verif,  origin='lower', vmin=0/norm, vmax=15/norm,
                extent=[ms.min(), ms.max(), mx.min(), mx.max()], aspect='auto')

plt.xlim(1, 124)
plt.ylim(126, 500)

plt.xlabel(r'$M_{1}$ [GeV]')
plt.ylabel(r'$M_{3}$ [GeV]')
plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{3}} \cdot \mathrm{BR}_{h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
plt.title(r'BP2: upper limits at 95% C.L normalized')
plt.tight_layout()

plt.savefig("thesisAuxiliaryData/AtlasMassplotTest3_BP2.png", format='png')
plt.savefig("thesisAuxiliaryData/AtlasMassplotTest3_BP2.pdf")
plt.show()
plt.close()




### mass range BP3:

plt.imshow(BP2_grid_limit_verif,  origin='lower', vmin=0/norm, vmax=1/norm,
                extent=[ms.min(), ms.max(), mx.min(), mx.max()], aspect='auto')

plt.xlim(126, 500)
plt.ylim(255, 650)

plt.xlabel(r'$M_{2}$ [GeV]')
plt.ylabel(r'$M_{3}$ [GeV]')
plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{3}} \cdot \mathrm{BR}_{h_{3} \ \to \ h_{1}(\gamma\gamma) \ h_{2}(b\bar{b}) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
plt.title(r'BP3: upper limits at 95% C.L normalized')
plt.tight_layout()

plt.savefig("thesisAuxiliaryData/AtlasMassplotTest3_BP3.png", format='png')
plt.savefig("thesisAuxiliaryData/AtlasMassplotTest3_BP3.pdf")
plt.show()
plt.close()

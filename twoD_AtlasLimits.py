import json
import argparse
import glob
import pandas
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib
import mplhep as hep
import pathlib
import glob
import matplotlib.ticker as mticker
import twoDPlotter as twoDPlot

def cutter(ms, mx, z, xlim, ylim):

    # msCopy = np.copy(ms)
    # mxCopy = np.copy(mx)
    # zCopy =  np.copy(z)
    msCopy = []
    mxCopy = []
    zCopy = [] 
    for i in range(len(z)):

        if xlim[0] < ms[i] and ms[i] < xlim[1] and ylim[0] < mx[i] and mx[i] < ylim[1]:
            msCopy.append(ms[i])
            mxCopy.append(mx[i])
            zCopy.append(z[i])

        else: 
            continue
            print(i)
            # del msCopy[i]
            # del mxCopy[i]
            # del zCopy[i]

    return np.array(msCopy), np.array(mxCopy), np.array(zCopy)


if __name__ == '__main__':
    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    matplotlib.rcParams['axes.labelsize'] = 19
    matplotlib.rcParams['axes.titlesize'] = 19

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


    ### Low mass: ###

    BP2_xi_verif, BP2_yi_verif = np.linspace(ms.min(), ms.max(), 200), np.linspace(mx.min(), mx.max(), 100)
    BP2_grid_x_verif, BP2_grid_y_verif = np.meshgrid(BP2_xi_verif, BP2_yi_verif)

    ## BP2 Interpolate the limits on the grid
    BP2_grid_limit_verif = griddata((ms, mx), limit_obs/norm, (BP2_grid_x_verif, BP2_grid_y_verif), method='cubic') 
    # cubic does exclude a small region around (100, 275) but I believe that is just the interpolation playing tricks,
    # because if you examine the datapoints (scatter plot below) you will see that all the data points are way above the  mass plots
    # i.e nothing excluded

    #### create legends for BP2 and BP3 regions from https://matplotlib.org/stable/users/explain/axes/legend_guide.html#implementing-a-custom-legend-handler
    ###############################################################################
    class AnyObject1:
        pass


    class AnyObjectHandler1:
        def legend_artist(self, legend, orig_handle, fontsize, handlebox):
            x0, y0 = handlebox.xdescent, handlebox.ydescent
            width, height = handlebox.width, handlebox.height
            patch = matplotlib.patches.Rectangle([x0, y0], width, height, facecolor='none',
                                       edgecolor='red', hatch=r'//\\', lw=1,
                                       transform=handlebox.get_transform(), alpha=0.25)
            handlebox.add_artist(patch)
            return patch

    class AnyObject2:
        pass


    class AnyObjectHandler2:
        def legend_artist(self, legend, orig_handle, fontsize, handlebox):
            x0, y0 = handlebox.xdescent, handlebox.ydescent
            width, height = handlebox.width, handlebox.height
            patch = matplotlib.patches.Rectangle([x0, y0], width, height, facecolor='none',
                                       edgecolor='blue', hatch=r'//\\', lw=1,
                                       transform=handlebox.get_transform(), alpha=0.25)
            handlebox.add_artist(patch)
            return patch

    plt.legend([AnyObject1(), AnyObject2()], ['BP2 mass region', 'BP3 mass region'], handler_map={AnyObject1: AnyObjectHandler1(), AnyObject2: AnyObjectHandler2()},
               borderpad=0.1)

    # BP2
    plt.gca().add_patch(matplotlib.patches.Rectangle((1,126),123,374,linewidth=1,edgecolor='r',facecolor='none', hatch=r'//\\', alpha=0.25))
    # BP3
    plt.gca().add_patch(matplotlib.patches.Rectangle((126,255),374,395,linewidth=1,edgecolor='b',facecolor='none', hatch=r'//\\', alpha=0.25))
    ###############################################################################

    # following was used for the zoom box and colorbar: 
    # https://stackoverflow.com/questions/13583153/how-to-zoomed-a-portion-of-image-and-insert-in-the-same-plot-in-matplotlib
    # https://stackoverflow.com/questions/52399714/zooming-and-plotting-a-inset-plot
    # https://stackoverflow.com/questions/12324877/creating-inset-in-matplot-lib?rq=3
    # https://stackoverflow.com/questions/24035118/different-x-and-y-scale-in-zoomed-inset-matplotlib
    # OOP way of color bar https://stackoverflow.com/a/55614650/17456342
    im = plt.scatter(ms, mx, c=limit_obs/norm, vmin=0/norm, vmax=15/norm)

    ax = plt.gca()

    for i in range(len(limit_obs)):
        if ms[i] < 85 or ms[i] > 115 or mx[i] < 210 or mx[i] > 260:
            ax.annotate('{:.1f}'.format(limit_obs[i]/norm), (ms[i], mx[i]),
                         textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                         path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
        else: continue

    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
    from mpl_toolkits.axes_grid1.inset_locator import mark_inset   


    axins = zoomed_inset_axes(ax, 2, loc = 'lower right', bbox_to_anchor=(445, 158)) # zoom = 6
    axins.scatter(ms, mx, c=limit_obs/norm, vmin=0/norm, vmax=15/norm, zorder=2)

    
    # sub region of the original image
    x1, x2, y1, y2 = 86, 117, 215, 257
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)

    axins.set_xticks([])
    axins.set_yticks([])

    # draw a bbox of the region of the inset axes in the parent axes and
    # connecting lines between the bbox and the inset axes area
    # mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

    # add hatching
    axins.add_patch(matplotlib.patches.Rectangle((1,126),123,374,linewidth=1,edgecolor='r',facecolor='none', hatch = r'//\\', alpha=0.25, zorder=1))

    for i in range(len(limit_obs)):
        axins.annotate('{:.1f}'.format(limit_obs[i]/norm), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])

    ax.set_xlim(0, 270)
    ax.set_ylim(160, 420)

    ax.set_xlabel(r'$M_{X}$ [GeV]')
    ax.set_ylabel(r'$M_{S}$ [GeV]')
    ax.set_title(r'Upper limits at 95% C.L normalized, small $M_{X}$')

    fig = plt.gcf()
    fig.colorbar(im, ax=ax, label =r'$\left. \sigma(\mathrm{obs}) \ \right/ \ \sigma( \mathrm{SM})$' )

    plt.tight_layout()
    plt.savefig("thesisAuxiliaryData/AtlasMassplotTest4_lowmass.png", format='png')
    plt.savefig("thesisAuxiliaryData/AtlasMassplotTest4_lowmass.pdf")

    # DO NOT TURN ON SHOW, THE ZOOM BOX IS PLACE INCORRECTLY WHEN USING THE MATPLOTLIB WINDOW PANE OR SAVING IT AS A PNG COMPARED TO THE PDF
    # plt.show()
    plt.close()



    ### medium mass: ###

    BP3_xi_verif, BP3_yi_verif = np.linspace(ms.min(), ms.max(), 200), np.linspace(mx.min(), mx.max(), 100)
    BP3_grid_x_verif, BP3_grid_y_verif = np.meshgrid(BP3_xi_verif, BP3_yi_verif)

    ## BP3 Interpolate the limits on the grid
    BP3_grid_limit_verif = griddata((ms, mx), limit_obs/norm, (BP3_grid_x_verif, BP3_grid_y_verif), method='cubic')


    #### create legends for BP2 and BP3 regions
    ###############################################################################
    class AnyObject1:
        pass


    class AnyObjectHandler1:
        def legend_artist(self, legend, orig_handle, fontsize, handlebox):
            x0, y0 = handlebox.xdescent, handlebox.ydescent
            width, height = handlebox.width, handlebox.height
            patch = matplotlib.patches.Rectangle([x0, y0], width, height, facecolor='none',
                                       edgecolor='red', hatch=r'//\\', lw=1,
                                       transform=handlebox.get_transform(), alpha=0.25)
            handlebox.add_artist(patch)
            return patch

    class AnyObject2:
        pass


    class AnyObjectHandler2:
        def legend_artist(self, legend, orig_handle, fontsize, handlebox):
            x0, y0 = handlebox.xdescent, handlebox.ydescent
            width, height = handlebox.width, handlebox.height
            patch = matplotlib.patches.Rectangle([x0, y0], width, height, facecolor='none',
                                       edgecolor='blue', hatch=r'//\\', lw=1,
                                       transform=handlebox.get_transform(), alpha=0.25)
            handlebox.add_artist(patch)
            return patch

    legend = plt.legend([AnyObject1(), AnyObject2()], ['BP2 mass region', 'BP3 mass region'], handler_map={AnyObject1: AnyObjectHandler1(), AnyObject2: AnyObjectHandler2()},
                         loc='lower right', frameon=True, facecolor='white', framealpha=0.80, edgecolor='1', fancybox=False, borderpad=0.1)

    # BP2
    plt.gca().add_patch(matplotlib.patches.Rectangle((1,126),123,374,linewidth=1,edgecolor='r',facecolor='none', hatch = r'//\\', alpha=0.25))
    # BP3
    plt.gca().add_patch(matplotlib.patches.Rectangle((126,255),374,395,linewidth=1,edgecolor='b',facecolor='none', hatch = r'//\\', alpha=0.25))
    ###############################################################################

    plt.scatter(ms, mx, c=limit_obs/norm, vmin=0/norm, vmax=1/norm)
    msAnnotate, mxAnnotate, limit_obs_divNormAnnotate = cutter(ms, mx, limit_obs/norm, (0, 585), (420, 1020))
    twoDPlot.plotAuxAnnotator2D(msAnnotate, mxAnnotate, limit_obs_divNormAnnotate, '{:.1f}', rot=45, xytxt=(-3,-2), fontsize=8.9)

    plt.xlim(0, 525)
    plt.ylim(420, 620)

    plt.xlabel(r'$M_{S}$ [GeV]')
    plt.ylabel(r'$M_{X}$ [GeV]')

    plt.title(r'Upper limits at 95% C.L normalized, medium $M_{X}$')

    # plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{X}} \cdot \mathrm{BR}_{h_{X} \ \to \ h_{S}(b\bar{b}) \ h_{H}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
    plt.colorbar(label =r'$\left. \sigma(\mathrm{obs}) \ \right/ \ \sigma( \mathrm{SM})$' )

    plt.tight_layout()
    plt.savefig("thesisAuxiliaryData/AtlasMassplotTest4_mediummass.png", format='png')
    plt.savefig("thesisAuxiliaryData/AtlasMassplotTest4_mediummass.pdf")

    # plt.show()
    plt.close()




    ### large mass: ###

    BP3_xi_verif, BP3_yi_verif = np.linspace(ms.min(), ms.max(), 200), np.linspace(mx.min(), mx.max(), 100)
    BP3_grid_x_verif, BP3_grid_y_verif = np.meshgrid(BP3_xi_verif, BP3_yi_verif)

    ## BP3 Interpolate the limits on the grid
    BP3_grid_limit_verif = griddata((ms, mx), limit_obs/norm, (BP3_grid_x_verif, BP3_grid_y_verif), method='cubic')

    #### create legends for BP2 and BP3 regions
    ###############################################################################
    class AnyObject2:
        pass


    class AnyObjectHandler2:
        def legend_artist(self, legend, orig_handle, fontsize, handlebox):
            x0, y0 = handlebox.xdescent, handlebox.ydescent
            width, height = handlebox.width, handlebox.height
            patch = matplotlib.patches.Rectangle([x0, y0], width, height, facecolor='none',
                                       edgecolor='blue', hatch=r'//\\', lw=1,
                                       transform=handlebox.get_transform(), alpha=0.25)
            handlebox.add_artist(patch)
            return patch

    legend = plt.legend([AnyObject2()], ['BP3 mass region'], handler_map={AnyObject2: AnyObjectHandler2()},
                         loc='lower right', frameon=True, facecolor='white', framealpha=0.80, edgecolor='1', fancybox=False, borderpad=0.1)

    # BP3
    plt.gca().add_patch(matplotlib.patches.Rectangle((126,255),374,395,linewidth=1,edgecolor='b',facecolor='none', hatch = r'//\\', alpha=0.25))
    ###############################################################################

    plt.scatter(ms, mx, c=limit_obs/norm, vmin=0/norm, vmax=1/norm)
    msAnnotate, mxAnnotate, limit_obs_divNormAnnotate = cutter(ms, mx, limit_obs/norm, (0, 585), (420, 1020))
    twoDPlot.plotAuxAnnotator2D(msAnnotate, mxAnnotate, limit_obs_divNormAnnotate, '{:.1f}', rot=45, xytxt=(-3,-2), fontsize=8.9)

    plt.xlim(0, 525)
    plt.ylim(620, 1020)

    plt.xlabel(r'$M_{S}$ [GeV]')
    plt.ylabel(r'$M_{X}$ [GeV]')

    plt.title(r'Upper limits at 95% C.L normalized, large $M_{X}$')

    # plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{X}} \cdot \mathrm{BR}_{h_{X} \ \to \ h_{S}(b\bar{b}) \ h_{H}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
    plt.colorbar(label =r'$\left. \sigma(\mathrm{obs}) \ \right/ \ \sigma( \mathrm{SM})$' )


    plt.tight_layout()
    plt.savefig("thesisAuxiliaryData/AtlasMassplotTest4_largemass.png", format='png')
    plt.savefig("thesisAuxiliaryData/AtlasMassplotTest4_largemass.pdf")

    # plt.show()
    plt.close()





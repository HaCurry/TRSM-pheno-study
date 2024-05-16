import os
import json

import numpy as np
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import mplhep as hep

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/'

    # path to condor job output
    # E:
    pathOutputParent = '/eos/user/i/ihaque/AtlasLimitsGridSearchOutput'

    # path to plots
    # E:
    pathPlots = os.path.join(pathRepo, 'AtlasLimitsGridSearch', 'plots')

    # create plotting directory
    os.makedirs(pathPlots, exist_ok=True)

    df = pandas.read_table(os.path.join(pathRepo, 'AtlasLimitsGridSearch', 'AtlasLimitsGridSearchMax.tsv'))

    ms = np.array([element for element in df['ms']])
    mx = np.array([element for element in df['mx']])
    ObsLim = np.array([element for element in df['ObsLim']])
    max = np.array([element for element in df['x_X_S_bb_H_gamgam_max']])

    norm = (31.02 * 0.0026) * 10**(-3)

    ## plotting style

    with open(os.path.join(pathRepo, 'MatplotlibStyles.json')) as json_file:
        styles = json.load(json_file)

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})

    # change label fontsize
    mpl.rcParams['axes.labelsize'] = styles['axes.labelsize']
    mpl.rcParams['axes.titlesize'] = styles['axes.titlesize']

    # change ticksize
    mpl.rcParams['xtick.minor.size'] = styles['xtick.minor.size']
    mpl.rcParams['xtick.major.size'] = styles['xtick.major.size']
    mpl.rcParams['ytick.minor.size'] = styles['ytick.minor.size']
    mpl.rcParams['ytick.major.size'] = styles['ytick.major.size']

    # change legend font size and padding
    mpl.rcParams['legend.borderpad'] = styles['legend.borderpad']
    mpl.rcParams['legend.fontsize'] = styles['legend.fontsize']
    mpl.rcParams['legend.title_fontsize'] = styles['legend.title_fontsize']
    mpl.rcParams['legend.frameon'] = styles['legend.frameon']
    mpl.rcParams['legend.fancybox'] = styles['legend.fancybox']
    mpl.rcParams['legend.edgecolor'] = styles['legend.edgecolor']
    mpl.rcParams['legend.edgecolor'] = styles['legend.edgecolor']    
    
    ## Maximum cross cections from grid search

    ## Low mass

    # following was used for the zoom box and colorbar: 
    # https://stackoverflow.com/questions/13583153/how-to-zoomed-a-portion-of-image-and-insert-in-the-same-plot-in-matplotlib
    # https://stackoverflow.com/questions/52399714/zooming-and-plotting-a-inset-plot
    # https://stackoverflow.com/questions/12324877/creating-inset-in-matplot-lib?rq=3
    # https://stackoverflow.com/questions/24035118/different-x-and-y-scale-in-zoomed-inset-matplotlib
    # OOP way of color bar https://stackoverflow.com/a/55614650/17456342
    im = plt.scatter(ms, mx, c=max/norm)

    ax = plt.gca()

    for i in range(len(max/norm)):
        if ms[i] < 85 or ms[i] > 115 or mx[i] < 210 or mx[i] > 260:
            ax.annotate('{:.3f}'.format(max[i]/norm), (ms[i], mx[i]),
                         textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                         path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])
        else: continue

    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
    from mpl_toolkits.axes_grid1.inset_locator import mark_inset   


    axins = zoomed_inset_axes(ax, 2, loc = 'lower right', bbox_to_anchor=(445, 158)) # zoom = 6
    axins.scatter(ms, mx, c=max/norm, zorder=2)

    
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

    for i in range(len(max/norm)):
        axins.annotate('{:.3f}'.format(max[i]/norm), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])

    ax.set_xlim(0, 270)
    ax.set_ylim(160, 420)

    ax.set_xlabel(r'$M_{S}$ [GeV]')
    ax.set_ylabel(r'$M_{X}$ [GeV]')
    ax.set_title(r'$\sigma(S(b\bar{b})H(\gamma\gamma))/\sigma(SM)$, small $M_{X}$')

    fig = plt.gcf()
    fig.colorbar(im, ax=ax, label =r'$\sigma(S(b\bar{b})H(\gamma\gamma))/\sigma(SM)$' )

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'AtlasLimitsMax_lowmass.png'), format='png')
    plt.savefig(os.path.join(pathPlots, 'AtlasLimitsMax_lowmass.pdf'))
    plt.close()

    # DO NOT TURN ON SHOW, THE ZOOM BOX IS PLACE INCORRECTLY WHEN USING THE MATPLOTLIB WINDOW PANE OR SAVING IT AS A PNG  #  plt.close()

    ## medium mass:

    plt.scatter(ms, mx, c=max/norm)
    for i in range(len(max/norm)):
        plt.annotate('{:.3f}'.format(max[i]/norm), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])
    # msAnnotate, mxAnnotate, max_divNormAnnotate = cutter(ms, mx, max/norm, (0, 585), (420, 1020))
    # twoDPlot.plotAuxAnnotator2D(msAnnotate, mxAnnotate, max_divNormAnnotate, '{:.1f}', rot=45, xytxt=(-3,-2), fontsize=8.9)

    plt.xlim(0, 525)
    plt.ylim(420, 620)

    plt.xlabel(r'$M_{S}$ [GeV]')
    plt.ylabel(r'$M_{X}$ [GeV]')

    plt.title(r'$\sigma(S(b\bar{b})H(\gamma\gamma))/\sigma(SM)$, medium $M_{X}$')

    # plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{X}} \cdot \mathrm{BR}_{h_{X} \ \to \ h_{S}(b\bar{b}) \ h_{H}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
    plt.colorbar(label =r'$\sigma(S(b\bar{b})H(\gamma\gamma))/\sigma(SM)$' )

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'AtlasLimitsMax_mediummass.png'), format='png')
    plt.savefig(os.path.join(pathPlots, 'AtlasLimitsMax_mediummass.pdf'))

    # plt.show()
    plt.close()


    ## large mass:

    plt.scatter(ms, mx, c=max/norm)
    for i in range(len(max/norm)):
        plt.annotate('{:.3f}'.format(max[i]/norm), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])
    # msAnnotate, mxAnnotate, max_divNormAnnotate = cutter(ms, mx, max/norm, (0, 585), (420, 1020))
    # twoDPlot.plotAuxAnnotator2D(msAnnotate, mxAnnotate, max_divNormAnnotate, '{:.1f}', rot=45, xytxt=(-3,-2), fontsize=8.9)

    plt.xlim(0, 525)
    plt.ylim(620, 1020)

    plt.xlabel(r'$M_{S}$ [GeV]')
    plt.ylabel(r'$M_{X}$ [GeV]')

    plt.title(r'$\sigma(S(b\bar{b})H(\gamma\gamma))/\sigma(SM)$, large $M_{X}$')

    # plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{X}} \cdot \mathrm{BR}_{h_{X} \ \to \ h_{S}(b\bar{b}) \ h_{H}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
    plt.colorbar(label =r'$\sigma(S(b\bar{b})H(\gamma\gamma))/\sigma(SM)$' )


    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'AtlasLimitsMax_largemass.png'), format='png')
    plt.savefig(os.path.join(pathPlots, 'AtlasLimitsMax_largemass.pdf'))

    # plt.show()
    plt.close()


    ## Observed limits divided by maximum cross section from grid search

    # following was used for the zoom box and colorbar: 
    # https://stackoverflow.com/questions/13583153/how-to-zoomed-a-portion-of-image-and-insert-in-the-same-plot-in-matplotlib
    # https://stackoverflow.com/questions/52399714/zooming-and-plotting-a-inset-plot
    # https://stackoverflow.com/questions/12324877/creating-inset-in-matplot-lib?rq=3
    # https://stackoverflow.com/questions/24035118/different-x-and-y-scale-in-zoomed-inset-matplotlib
    # OOP way of color bar https://stackoverflow.com/a/55614650/17456342
    im = plt.scatter(ms, mx, c=ObsLim/max)

    ax = plt.gca()

    for i in range(len(ObsLim/max)):
        if ms[i] < 85 or ms[i] > 115 or mx[i] < 210 or mx[i] > 260:
            ax.annotate('{:.1f}'.format((ObsLim/max)[i]), (ms[i], mx[i]),
                         textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                         path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])
        else: continue

    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
    from mpl_toolkits.axes_grid1.inset_locator import mark_inset   


    axins = zoomed_inset_axes(ax, 2, loc = 'lower right', bbox_to_anchor=(445, 158)) # zoom = 6
    axins.scatter(ms, mx, c=ObsLim/max, zorder=2)

    
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

    for i in range(len(ObsLim/max)):
        axins.annotate('{:.1f}'.format((ObsLim/max)[i]), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])

    ax.set_xlim(0, 270)
    ax.set_ylim(160, 420)

    ax.set_xlabel(r'$M_{S}$ [GeV]')
    ax.set_ylabel(r'$M_{X}$ [GeV]')
    ax.set_title(r'$\sigma(obs)/\sigma(S(b\bar{b})H(\gamma\gamma))/$, small $M_{X}$')

    fig = plt.gcf()
    fig.colorbar(im, ax=ax, label =r'$\sigma(obs)/\sigma(S(b\bar{b})H(\gamma\gamma))/$' )

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ObsLimVsAtlasLimitsMax_lowmass.png'), format='png')
    plt.savefig(os.path.join(pathPlots, 'ObsLimVsAtlasLimitsMax_lowmass.pdf'))
    plt.close()

    # DO NOT TURN ON SHOW, THE ZOOM BOX IS PLACE INCORRECTLY WHEN USING THE MATPLOTLIB WINDOW PANE OR SAVING IT AS A PNG  #  plt.close()

    ## medium mass:

    plt.scatter(ms, mx, c=ObsLim/max)
    for i in range(len(ObsLim/max)):
        plt.annotate('{:.1f}'.format((ObsLim/max)[i]), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])
    # msAnnotate, mxAnnotate, max_divNormAnnotate = cutter(ms, mx, ObsLim/max, (0, 585), (420, 1020))
    # twoDPlot.plotAuxAnnotator2D(msAnnotate, mxAnnotate, max_divNormAnnotate, '{:.1f}', rot=45, xytxt=(-3,-2), fontsize=8.9)

    plt.xlim(0, 525)
    plt.ylim(420, 620)

    plt.xlabel(r'$M_{S}$ [GeV]')
    plt.ylabel(r'$M_{X}$ [GeV]')

    plt.title(r'$\sigma(obs)/\sigma(S(b\bar{b})H(\gamma\gamma))/$, medium $M_{X}$')

    # plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{X}} \cdot \mathrm{BR}_{h_{X} \ \to \ h_{S}(b\bar{b}) \ h_{H}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
    plt.colorbar(label =r'$\sigma(obs)/\sigma(S(b\bar{b})H(\gamma\gamma))/$' )

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ObsLimVsAtlasLimitsMax_mediummass.png'), format='png')
    plt.savefig(os.path.join(pathPlots, 'ObsLimVsAtlasLimitsMax_mediummass.pdf'))

    # plt.show()
    plt.close()


    ## large mass:

    plt.scatter(ms, mx, c=ObsLim/max)
    for i in range(len(ObsLim/max)):
        plt.annotate('{:.1f}'.format((ObsLim/max)[i]), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])
    # msAnnotate, mxAnnotate, max_divNormAnnotate = cutter(ms, mx, ObsLim/max, (0, 585), (420, 1020))
    # twoDPlot.plotAuxAnnotator2D(msAnnotate, mxAnnotate, max_divNormAnnotate, '{:.1f}', rot=45, xytxt=(-3,-2), fontsize=8.9)

    plt.xlim(0, 525)
    plt.ylim(620, 1020)

    plt.xlabel(r'$M_{S}$ [GeV]')
    plt.ylabel(r'$M_{X}$ [GeV]')

    plt.title(r'$\sigma(obs)/\sigma(S(b\bar{b})H(\gamma\gamma))/$, large $M_{X}$')

    # plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{X}} \cdot \mathrm{BR}_{h_{X} \ \to \ h_{S}(b\bar{b}) \ h_{H}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
    plt.colorbar(label =r'$\sigma(obs)/\sigma(S(b\bar{b})H(\gamma\gamma))/$' )


    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ObsLimVsAtlasLimitsMax_largemass.png'), format='png')
    plt.savefig(os.path.join(pathPlots, 'ObsLimVsAtlasLimitsMax_largemass.pdf'))

    # plt.show()
    plt.close()


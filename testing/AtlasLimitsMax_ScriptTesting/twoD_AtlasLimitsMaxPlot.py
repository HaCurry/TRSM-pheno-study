import pandas
import numpy as np
import os

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patheffects
import mplhep as hep

import twoDPlotter as twoDPlot

if __name__ == '__main__':
    
    # submission path
    afsPath ='/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_ScriptTesting/AtlasLimitsMaxCondor_ScriptTesting/AtlasLimitsMax_configure_ScriptTesting'
    # input and output path
    eosPath = '/eos/user/i/ihaque/testing/AtlasLimitsMax_ScriptTesting/AtlasLimitsMax_configure_ScriptTesting'
 
    df = pandas.read_table(os.path.join(eosPath, 'AtlasLimitsMax_AtlasNotation.tsv'))
    
    ms = np.array([element for element in df['ms']])
    mx = np.array([element for element in df['mx']])
    ObsLim = np.array([element for element in df['ObservedLimit']])
    max = np.array([element for element in df['maximum']])

    norm = (31.02 * 0.0026) * 10**(-3)

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    matplotlib.rcParams['axes.labelsize'] = 19
    matplotlib.rcParams['axes.titlesize'] = 19


    #### Maximum Cross Sections ####
    
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
                         path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
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
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])

    ax.set_xlim(0, 270)
    ax.set_ylim(160, 420)

    ax.set_xlabel(r'$M_{S}$ [GeV]')
    ax.set_ylabel(r'$M_{X}$ [GeV]')
    ax.set_title(r'$\sigma(S(b\bar{b})H(\gamma\gamma))/\sigma(SM)$, small $M_{X}$')

    fig = plt.gcf()
    fig.colorbar(im, ax=ax, label =r'$\sigma(S(b\bar{b})H(\gamma\gamma))/\sigma(SM)$' )

    plt.tight_layout()
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsMax_lowmass.png"), format='png')
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsMax_lowmass.pdf"))
    plt.close()

    # DO NOT TURN ON SHOW, THE ZOOM BOX IS PLACE INCORRECTLY WHEN USING THE MATPLOTLIB WINDOW PANE OR SAVING IT AS A PNG  #  plt.close()

    ### medium mass: ###

    plt.scatter(ms, mx, c=max/norm)
    for i in range(len(max/norm)):
        plt.annotate('{:.3f}'.format(max[i]/norm), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
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
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsMax_mediummass.png"), format='png')
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsMax_mediummass.pdf"))

    # plt.show()
    plt.close()


    ### large mass: ###

    plt.scatter(ms, mx, c=max/norm)
    for i in range(len(max/norm)):
        plt.annotate('{:.3f}'.format(max[i]/norm), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
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
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsMax_largemass.png"), format='png')
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsMax_largemass.pdf"))

    # plt.show()
    plt.close()


    #### Exclusion Plots ####
    
    ## Low mass

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
            ax.annotate('{:.1f}'.format(ObsLim[i]/max[i]), (ms[i], mx[i]),
                         textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                         path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
        else: continue
    
    # mark the points which are excluded by a red circle
    for i in range(len(ObsLim/max)):
        if ObsLim[i]/max[i] < 1:
            ax.plot(ms[i], mx[i], ObsLim[i]/max[i], marker='o', markerfacecolor='none', color='red')

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
        if ObsLim[i]/max[i] < 1:
            axins.plot(ms[i], mx[i], ObsLim[i]/max[i], marker='o', markerfacecolor='none', color='red')
        axins.annotate('{:.1f}'.format(ObsLim[i]/max[i]), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])

    ax.set_xlim(0, 270)
    ax.set_ylim(160, 420)

    ax.set_xlabel(r'$M_{S}$ [GeV]')
    ax.set_ylabel(r'$M_{X}$ [GeV]')
    ax.set_title(r'$\sigma(lim) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$, small $M_{X}$')

    fig = plt.gcf()
    fig.colorbar(im, ax=ax, label =r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$' )

    plt.tight_layout()
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsExclusion_lowmass.png"), format='png')
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsExclusion_lowmass.pdf"))
    plt.close()


    ### medium mass: ###

    plt.scatter(ms, mx, c=ObsLim/max)
    for i in range(len(ObsLim/max)):
        plt.annotate('{:.1f}'.format(ObsLim[i]/max[i]), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
    # msAnnotate, mxAnnotate, max_divNormAnnotate = cutter(ms, mx, ObsLim/max, (0, 585), (420, 1020))
    # twoDPlot.plotAuxAnnotator2D(msAnnotate, mxAnnotate, max_divNormAnnotate, '{:.1f}', rot=45, xytxt=(-3,-2), fontsize=8.9)

    # mark the points which are excluded by a red circle
    for i in range(len(ObsLim/max)):
        if ObsLim[i]/max[i] < 1:
            plt.plot(ms[i], mx[i], ObsLim[i]/max[i], marker='o', markerfacecolor='none', color='red')

    plt.xlim(0, 525)
    plt.ylim(420, 620)

    plt.xlabel(r'$M_{S}$ [GeV]')
    plt.ylabel(r'$M_{X}$ [GeV]')

    plt.title(r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$, medium $M_{X}$')

    # plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{X}} \cdot \mathrm{BR}_{h_{X} \ \to \ h_{S}(b\bar{b}) \ h_{H}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
    plt.colorbar(label =r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$' )

    plt.tight_layout()
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsExclusion_mediummass.png"), format='png')
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsExclusion_mediummass.pdf"))

    # plt.show()
    plt.close()



    ### large mass: ###

    plt.scatter(ms, mx, c=ObsLim/max)
    for i in range(len(ObsLim/max)):
        plt.annotate('{:.1f}'.format(ObsLim[i]/max[i]), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
    # msAnnotate, mxAnnotate, max_divNormAnnotate = cutter(ms, mx, ObsLim/max, (0, 585), (420, 1020))
    # twoDPlot.plotAuxAnnotator2D(msAnnotate, mxAnnotate, max_divNormAnnotate, '{:.1f}', rot=45, xytxt=(-3,-2), fontsize=8.9)

    # mark the points which are excluded by a red circle
    for i in range(len(ObsLim/max)):
        if ObsLim[i]/max[i] < 1:
            plt.plot(ms[i], mx[i], ObsLim[i]/max[i], marker='o', markerfacecolor='none', color='red')

    plt.xlim(0, 525)
    plt.ylim(620, 1020)

    plt.xlabel(r'$M_{S}$ [GeV]')
    plt.ylabel(r'$M_{X}$ [GeV]')

    plt.title(r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$, large $M_{X}$')

    # plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{X}} \cdot \mathrm{BR}_{h_{X} \ \to \ h_{S}(b\bar{b}) \ h_{H}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
    plt.colorbar(label =r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$' )


    plt.tight_layout()
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsExclusion_largemass.png"), format='png')
    plt.savefig(os.path.join(eosPath, "plots/AtlasLimitsExclusion_largemass.pdf"))

    # plt.show()
    plt.close()


    #### BP Exclusion plots ####

    ### BP2 Exclusion plots ###
    
    x, y, z = [], [], []
    for i in range(len(ObsLim/max)):
        if 1 < ms[i] and ms[i] < 124 and 126 < mx[i] and mx[i] < 500:
            x.append(ms[i])
            y.append(mx[i])
            z.append(ObsLim[i]/max[i])
    
    # x = ms
    # y = mx
    # z = ObsLim/max

    # twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.0f}')
    nanmarkz, nanmarkx, nanmarky = [], [], []
    for i in range(len(z)):
        if np.isnan(z[i]):
            nanmarkz.append(z[i])
            nanmarkx.append(x[i])
            nanmarky.append(y[i])
        else:
            plt.annotate('{:.0f}'.format(z[i]), (x[i], y[i]),
                         textcoords='offset points', xytext=(-3,-2), fontsize=9, rotation=45,
                         path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
    plt.scatter(nanmarkx, nanmarky, facecolors='None', edgecolors='grey', linestyle='dotted', label='Excluded by ScannerS')
    plt.legend()

    plt.scatter(x, y, c=z)

    twoDPlot.plotAuxTitleAndBounds2D(r'BP2: $\sigma(\mathrm{lim})/\sigma(gg \ \to \ h _{3} \ \to \ h _{1}(b\bar{b}) \ h _{2}(\gamma\gamma) )$',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\sigma(\mathrm{lim})/\sigma(gg \ \to \ h _{3} \ \to h _{1}(b\bar{b}) \ h _{2}(\gamma\gamma) )$', xlims=(1, 124), ylims=(126, 500))
    plt.tight_layout()

    plt.savefig(os.path.join(eosPath, 'plots/AtlasLimitsExclusion_BP2.pdf'))
    # plt.show()
    plt.close()

    del x, y, z


    ### BP3 Exclusion plots ###

    x, y, z = [], [], []
    for i in range(len(ObsLim/max)):
        if 126 < ms[i] and ms[i] < 500 and 255 < mx[i] and mx[i] < 650:
            x.append(ms[i])
            y.append(mx[i])
            z.append(ObsLim[i]/max[i])

    # twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.0f}', rot=45, xytxt=(-3,-2), fontsize=9)
    nanmarkz, nanmarkx, nanmarky = [], [], []
    for i in range(len(z)):
        if np.isnan(z[i]):
            nanmarkz.append(z[i])
            nanmarkx.append(x[i])
            nanmarky.append(y[i])
        else:
            plt.annotate('{:.0f}'.format(z[i]), (x[i], y[i]),
                         textcoords='offset points', xytext=(-3,-2), fontsize=9, rotation=45,
                         path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
    plt.scatter(nanmarkx, nanmarky, facecolors='None', edgecolors='grey', linestyle='dotted', label='Excluded by ScannerS')
    plt.legend()

    plt.scatter(x, y, c=z)

    twoDPlot.plotAuxTitleAndBounds2D(r'BP3: $\left. \sigma(\mathrm{lim}) \right/ \sigma(gg \ \to \  h _{3} \ \to \ h _{1}(b\bar{b}) \ h _{2}(\gamma\gamma) )$', r'$M_{2}$ [GeV]', r'$M_{3}$ [GeV]', r'$\left. \sigma(\mathrm{lim}) \right/ \sigma(gg \ \to \ h _{3} \ \to \ h _{1}(\gamma\gamma) \ h _{2}(b\bar{b}) )$', xlims=(126, 500), ylims=(255, 650))
    plt.tight_layout()

    plt.savefig(os.path.join(eosPath, 'plots/AtlasLimitsExclusion_BP3.pdf'))
    # plt.show()
    plt.close()

    del x, y, z

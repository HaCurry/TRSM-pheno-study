import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patheffects
import mplhep as hep

if __name__ == '__main__':
    
    df = pandas.read_table('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/AtlasLimitsMax_AtlasNotation.tsv')
    
    ms = np.array([element for element in df['ms']])
    mx = np.array([element for element in df['mx']])
    ObsLim = np.array([element for element in df['ObservedLimit']])
    max = np.array([element for element in df['maximum']])

    norm = (31.02 * 0.0026) * 10**(-3)

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    matplotlib.rcParams['axes.labelsize'] = 19
    matplotlib.rcParams['axes.titlesize'] = 19


    ### Maximum Cross Sections ###
    
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
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsMax_lowmass.png", format='png')
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsMax_lowmass.pdf")
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
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsMax_mediummass.png", format='png')
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsMax_mediummass.pdf")

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
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsMax_largemass.png", format='png')
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsMax_largemass.pdf")

    # plt.show()
    plt.close()


    ### Exclusion Plots ###
    
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
            #ax.plot(ms[i], mx[i], ObsLim[i]/max[i], marker='o', markerfacecolor='none', color='red')
            ax.scatter(ms[i], mx[i], marker='o', facecolor='none', color='red', linestyle='dashed', s=120)
             

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
            #axins.plot(ms[i], mx[i], ObsLim[i]/max[i], marker='o', markerfacecolor='none', color='red')
            axins.scatter(ms[i], mx[i], marker='o', facecolor='none', color='red', linestyle='dashed', s=120)
 
        axins.annotate('{:.1f}'.format(ObsLim[i]/max[i]), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])

    ax.set_xlim(0, 270)
    ax.set_ylim(160, 420)

    ax.set_xlabel(r'$M_{S}$ [GeV]')
    ax.set_ylabel(r'$M_{X}$ [GeV]')
    ax.set_title(r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$, small $M_{X}$')

    fig = plt.gcf()
    fig.colorbar(im, ax=ax, label =r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$' )

    plt.tight_layout()
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsExclusion_lowmass.png", format='png')
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsExclusion_lowmass.pdf")
    plt.close()


    ### medium mass: ###

    im = plt.scatter(ms, mx, c=ObsLim/max)
    for i in range(len(ObsLim/max)):
        plt.annotate('{:.1f}'.format(ObsLim[i]/max[i]), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
    # msAnnotate, mxAnnotate, max_divNormAnnotate = cutter(ms, mx, ObsLim/max, (0, 585), (420, 1020))
    # twoDPlot.plotAuxAnnotator2D(msAnnotate, mxAnnotate, max_divNormAnnotate, '{:.1f}', rot=45, xytxt=(-3,-2), fontsize=8.9)

    # mark the points which are excluded by a red circle
    for i in range(len(ObsLim/max)):
        if ObsLim[i]/max[i] < 1:
            hejsan=4
            #plt.plot(ms[i], mx[i], ObsLim[i]/max[i], marker='o', markerfacecolor='none', color='red')
            #plt.scatter(ms[i], mx[i], marker='o', facecolor='none', linestyle='dashed', color='red', s=120)
            plt.scatter(ms[i], mx[i], marker='o', facecolor='none', color='red', linestyle='dashed', s=120)


    plt.xlim(0, 525)
    plt.ylim(420, 620)

    plt.xlabel(r'$M_{S}$ [GeV]')
    plt.ylabel(r'$M_{X}$ [GeV]')

    plt.title(r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$, medium $M_{X}$')

    # plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{X}} \cdot \mathrm{BR}_{h_{X} \ \to \ h_{S}(b\bar{b}) \ h_{H}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
    fig = plt.gcf()
    ax = plt.gca()
    fig.colorbar(im, ax=ax, label=r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$' )

    plt.tight_layout()
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsExclusion_mediummass.png", format='png')
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsExclusion_mediummass.pdf")

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
            hejsan=4
            #plt.plot(ms[i], mx[i], ObsLim[i]/max[i], marker='o', markerfacecolor='none', color='red')
            plt.scatter(ms[i], mx[i], marker='o', facecolor='none', linestyle='dashed', color='red', s=120)

    plt.xlim(0, 525)
    plt.ylim(620, 1020)

    plt.xlabel(r'$M_{S}$ [GeV]')
    plt.ylabel(r'$M_{X}$ [GeV]')

    plt.title(r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$, large $M_{X}$')

    # plt.colorbar(label =r'$\sigma_{ gg \ \rightarrow \ h_{X}} \cdot \mathrm{BR}_{h_{X} \ \to \ h_{S}(b\bar{b}) \ h_{H}(\gamma\gamma) } \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$' )
    
    fig = plt.gcf()
    ax = plt.gca()
    fig.colorbar(im, ax=ax, label=r'$\sigma(obs) \ / \ \sigma(S(b\bar{b})H(\gamma\gamma))$' )


    plt.tight_layout()
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsExclusion_largemass.png", format='png')
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4/plots/AtlasLimitsExclusion_largemass.pdf")

    # plt.show()
    plt.close()











    


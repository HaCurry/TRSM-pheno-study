import pandas
import numpy
import matplotlib.pyplot as plt

if __name__ == '__main__':

    ms = []
    mx = []
    max = []
    ObsLim = []

    df_H1_bb_H2_gamgam = pandas.read_table('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_bb_H2_gamgam_Max.tsv')
    
    print(df_H1_bb_H2_gamgam)

    mH1_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH1']]
    mH2_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH2']]
    mH3_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH3']]
    
    x_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['pp_X_H1_bb_H2_gamgam']]
    ObsLim_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['ObservedLimit']]
    
    for i in range(len(x_H1_bb_H2_gamgam)):
        if abs(mH1_H1_bb_H2_gamgam[i] - 125.09) < 10**(-10):
            # ms.append(mH2_H1_bb_H2_gamgam[i])
            # mx.append(mH3_H1_bb_H2_gamgam[i])
            # max.append(x_H1_bb_H2_gamgam[i])
            # ObsLim.append(ObsLim_H1_bb_H2_gamgam[i])
            continue
        
        elif abs(mH2_H1_bb_H2_gamgam[i] - 125.09) < 10**(-10):
            ms.append(mH1_H1_bb_H2_gamgam[i])
            mx.append(mH3_H1_bb_H2_gamgam[i])
            max.append(x_H1_bb_H2_gamgam[i])
            ObsLim.append(ObsLim_H1_bb_H2_gamgam[i])

        else:
            raise Exception(f'Something went wrong at H1_bb_H2_gamgam at\n\
                            index {i},\n\
                            mH1 = {mH1_H1_bb_H2_gamgam[i]}\n\
                            mH2 = {mH2_H1_bb_H2_gamgam}\n\
                            mH3 = {mH3_H1_bb_H2_gamgam}\n\
                            max = {x_H1_bb_H2_gamgam}\n\
                            ObsLim = {ObsLim_H1_bb_H2_gamgam}')

    del df_H1_bb_H2_gamgam, mH1_H1_bb_H2_gamgam, mH2_H1_bb_H2_gamgam, mH3_H1_bb_H2_gamgam, x_H1_bb_H2_gamgam, ObsLim_H1_bb_H2_gamgam
    
    df_H1_gamgam_H2_bb = pandas.read_table('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_gamgam_H2_bb_Max.tsv')
    
    print(df_H1_gamgam_H2_bb)

    mH1_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH1']]
    mH2_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH2']]
    mH3_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH3']]

    x_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['pp_X_H1_gamgam_H2_bb']]
    ObsLim_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['ObservedLimit']]


    for i in range(len(x_H1_gamgam_H2_bb)):
        if abs(mH1_H1_gamgam_H2_bb[i] - 125.09) < 10**(-10):
            ms.append(mH2_H1_gamgam_H2_bb[i])
            mx.append(mH3_H1_gamgam_H2_bb[i])
            max.append(x_H1_gamgam_H2_bb[i])
            ObsLim.append(ObsLim_H1_gamgam_H2_bb[i])
        
        elif abs(mH2_H1_gamgam_H2_bb[i] - 125.09) < 10**(-10):
            # ms.append(mH1_H1_gamgam_H2_bb[i])
            # mx.append(mH3_H1_gamgam_H2_bb[i])
            # max.append(x_H1_gamgam_H2_bb[i])
            # ObsLim.append(ObsLim_H1_gamgam_H2_bb[i])
            continue

        else:
            raise Exception(f'Something went wrong at H1_gamgam_H2_bb at\n\
                            index {i},\n\
                            mH1 = {mH1_H1_gamgam_H2_bb[i]}\n\
                            mH2 = {mH2_H1_gamgam_H2_bb}\n\
                            mH3 = {mH3_H1_gamgam_H2_bb}\n\
                            max = {x_H1_gamgam_H2_bb}\n\
                            ObsLim = {ObsLim_H1_gamgam_H2_bb}')


    print(f'# of elements: ms: {len(ms)}, mx: {len(mx)}, max: {len(max)}, ObsLim: {len(ObsLim)}')

    print('testing')

    ## Low mass

    # following was used for the zoom box and colorbar: 
    # https://stackoverflow.com/questions/13583153/how-to-zoomed-a-portion-of-image-and-insert-in-the-same-plot-in-matplotlib
    # https://stackoverflow.com/questions/52399714/zooming-and-plotting-a-inset-plot
    # https://stackoverflow.com/questions/12324877/creating-inset-in-matplot-lib?rq=3
    # https://stackoverflow.com/questions/24035118/different-x-and-y-scale-in-zoomed-inset-matplotlib
    # OOP way of color bar https://stackoverflow.com/a/55614650/17456342
    im = plt.scatter(ms, mx, c=max)

    ax = plt.gca()

    for i in range(len(max)):
        if ms[i] < 85 or ms[i] > 115 or mx[i] < 210 or mx[i] > 260:
            ax.annotate('{:.1f}'.format(max[i]), (ms[i], mx[i]),
                         textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                         path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])
        else: continue

    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
    from mpl_toolkits.axes_grid1.inset_locator import mark_inset   


    axins = zoomed_inset_axes(ax, 2, loc = 'lower right', bbox_to_anchor=(445, 158)) # zoom = 6
    axins.scatter(ms, mx, c=max, vmin=0, vmax=15, zorder=2)

    
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

    for i in range(len(max)):
        axins.annotate('{:.1f}'.format(max[i]), (ms[i], mx[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                     path_effects=[matplotlib.patheffects.withStroke(linewidth=1.5, foreground='w')])

    ax.set_xlim(0, 270)
    ax.set_ylim(160, 420)

    ax.set_xlabel(r'$M_{S}$ [GeV]')
    ax.set_ylabel(r'$M_{X}$ [GeV]')
    ax.set_title(r'Upper limits at 95% C.L normalized, small $M_{X}$')

    fig = plt.gcf()
    fig.colorbar(im, ax=ax, label =r'$\left. \sigma(\mathrm{obs}) \ \right/ \ \sigma( \mathrm{SM})$' )

    plt.tight_layout()
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/plots/AtlasLimitsMax_lowmass.png", format='png')
    plt.savefig("/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/plots/AtlasLimitsMax_lowmass.pdf")

    # DO NOT TURN ON SHOW, THE ZOOM BOX IS PLACE INCORRECTLY WHEN USING THE MATPLOTLIB WINDOW PANE OR SAVING IT AS A PNG  #  plt.close()























    
    plt.scatter(ms, mx, c=ObsLim)
    plt.savefig('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/plots/scatter')
    plt.close()


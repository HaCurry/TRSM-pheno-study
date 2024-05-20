import os
import json

import numpy as np
import pandas
import scipy.interpolate
import matplotlib as mpl
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import mplhep as hep

from helpScannerS import twoDPlotter as twoDPlot

def cutter(x, y, z, xlim, ylim):

    xNewlist = []
    yNewlist = []
    zNewlist = []

    tol = 10 ** (-6)

    for i in range(len(x)):
        if (xlim[0] < x[i] and x[i] < xlim[1] and 
            ylim[0] < y[i] and y[i] < ylim[1]):
            xNewlist.append(x[i])
            yNewlist.append(y[i])
            zNewlist.append(z[i])

            if (abs(x[i] - xlim[0]) < tol and
                abs(x[i] - xlim[1]) < tol and
                abs(y[i] - ylim[0]) < tol and
                abs(y[i] - ylim[1]) < tol):
                raise Exception('Function cutter is not precise enough for this.')

    return xNewlist, yNewlist, zNewlist


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
    XSmax = np.array([element for element in df['x_X_S_bb_H_gamgam_max']])

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

    # annotation settings
    fontsize = 10
    rotation = 45
    color = 'red'

    # annotation path effects
    path_effects = [pe.withStroke(linewidth=0.0, foreground='black')]

    # scatter settings
    scatterFacecolor = 'black'
    scatterMarkersize = 15

    # legend settings
    title = '$\sqrt{s}=13$ TeV\n$gg\\to X\\to S(b\\bar{b}) H(\gamma \gamma)$\n95% C.L observed limit\nGrid search: 100000 models'

    ## Maximum cross cections from grid search

    msLini, mxLini = np.linspace(min(ms), max(ms), 800), np.linspace(min(mx), max(mx), 1000)
    msMeshi, mxMeshi = np.meshgrid(msLini, mxLini)

    zi = scipy.interpolate.griddata((ms, mx), ObsLim/XSmax, (msMeshi, mxMeshi), method='cubic')

    msLinConti, mxLinConti = np.linspace(min(ms), max(ms), 25), np.linspace(min(mx), max(mx), 25)
    msMeshConti, mxMeshConti = np.meshgrid(msLini, mxLini)

    ziCont = scipy.interpolate.griddata((ms, mx), ObsLim/XSmax, (msMeshConti, mxMeshConti), method='nearest')

    ## low mass

    fig, ax = plt.subplots()

    msLow, mxLow, ObsLimVsXSmaxLow = cutter(ms, mx, ObsLim/XSmax,
                                     (0, 270), (160, 420))

    im = ax.imshow(zi, origin='lower', vmin=min(ObsLimVsXSmaxLow), vmax=max(ObsLimVsXSmaxLow),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # where the points are
    ax.scatter(msLow, mxLow, facecolor=scatterFacecolor, s=scatterMarkersize)

    ax.contour(msMeshConti, mxMeshConti, ziCont, levels=[-1, 1], colors=['blue', 'red'])

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(gg\to X \to S(b\bar{b})~H(\gamma\gamma))$',
                                     xlims=(0, 270), ylims=(160, 420),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(ObsLimVsXSmaxLow)):
        if 80 < msLow[i] and mxLow[i] < 260:
            continue
        else:
            ax.annotate('{:.1f}'.format(ObsLimVsXSmaxLow[i]), (msLow[i], mxLow[i]),
                        textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, color=color, 
                        path_effects=path_effects)

    # subregion of the original image
    x1, x2, y1, y2 = 86, 117, 215, 257
    axins = ax.inset_axes([200, 250, 60, 60],
                          transform=ax.transData,
                          xlim=(x1, x2), ylim=(y1, y2),
                          xticklabels=[], yticklabels=[])

    for i in range(len(ObsLimVsXSmaxLow)):
        if 80 > msLow[i] and mxLow[i] > 260:
            continue
        else:
            axins.annotate('{:.1f}'.format(ObsLimVsXSmaxLow[i]), (msLow[i], mxLow[i]),
                        textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, color=color, 
                        path_effects=path_effects)

    axins.imshow(zi, origin='lower', vmin=min(ObsLimVsXSmaxLow), vmax=max(ObsLimVsXSmaxLow),
                 extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # where the points are
    axins.scatter(msLow, mxLow, facecolor=scatterFacecolor, s=scatterMarkersize)

    ax.indicate_inset_zoom(axins, edgecolor="black")


    ax.legend(title=title,
              handles=[
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ObsLim_XSH_bbgamgam_max_lowmass.pdf'))
    plt.close()


    ## medium mass

    fig, ax = plt.subplots()

    msMed, mxMed, ObsLimVsXSmaxMed = cutter(ms, mx, ObsLim/XSmax,
                                     (0, 525), (420, 620))

    im = ax.imshow(zi, origin='lower', vmin=min(ObsLimVsXSmaxMed), vmax=max(ObsLimVsXSmaxMed),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # where the points are
    ax.scatter(msMed, mxMed, facecolor=scatterFacecolor, s=scatterMarkersize)

    ax.contour(msMeshConti, mxMeshConti, ziCont, levels=[-1, 1], colors=['blue', 'red'])

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(gg\to X \to S(bb)~H(\gamma\gamma))$',
                                     xlims=(15, 510), ylims=(415, 620),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(ObsLimVsXSmaxMed)):
        ax.annotate('{:.1f}'.format(ObsLimVsXSmaxMed[i]), (msMed[i], mxMed[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, color=color, 
                    path_effects=path_effects)

    ax.legend(title=title,
              handles=[
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ObsLim_XSH_bbgamgam_max_mediummass.pdf'))
    plt.close()


    ## high mass

    fig, ax = plt.subplots()

    msHigh, mxHigh, ObsLimVsXSmaxHigh = cutter(ms, mx, ObsLim/XSmax,
                                        (0, 525), (620, 1200))

    im = ax.imshow(zi, origin='lower', vmin=min(ObsLimVsXSmaxHigh), vmax=max(ObsLimVsXSmaxHigh),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # where the points are
    ax.scatter(msHigh, mxHigh, facecolor=scatterFacecolor, s=scatterMarkersize)

    ax.contour(msMeshConti, mxMeshConti, ziCont, levels=[-1, 1], colors=['blue', 'red'])

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(gg\to X \to S(b\bar{b})~H(\gamma\gamma))$',
                                     xlims=(40, 535), ylims=(620, 1200),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(ObsLimVsXSmaxHigh)):
        ax.annotate('{:.1f}'.format(ObsLimVsXSmaxHigh[i]), (msHigh[i], mxHigh[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=8, rotation=rotation, color=color, 
                    path_effects=path_effects)

    ax.legend(title=title,
              handles=[
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ObsLim_XSH_bbgamgam_max_highmass.pdf'))
    plt.close()


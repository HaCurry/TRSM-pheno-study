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
    survModelsRat = np.array([element/100000 for element in df['numOfModels']])

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
    fontsize = 12
    rotation = 45
    linewidth = 2.0

    # annotation settings
    fontsize = 10
    rotation = 45
    linewidth = 2.0

    # BP2 BP3 dashed line settings
    axvlineColor = 'blue'
    axvlineLinestyle = 'dashed'
    axvlineLinewidth = 1
    axvlineLabel = r'$\text{BP2}\leftrightarrow\text{BP3}$'

    # scatter settings
    scatterFacecolor = 'red'
    scatterMarkersize = 15

    # legend settings
    title = 'Fraction of surviving models (%)\nGrid search: 100000 models'

    ## Maximum cross cections from grid search

    msLini, mxLini = np.linspace(min(ms), max(ms), 800), np.linspace(min(mx), max(mx), 1000)
    msMeshi, mxMeshi = np.meshgrid(msLini, mxLini)

    zi = scipy.interpolate.griddata((ms, mx), survModelsRat, (msMeshi, mxMeshi), method='cubic')

    ## low mass

    fig, ax = plt.subplots()

    msLow, mxLow, survModelsRatLow = cutter(ms, mx, survModelsRat,
                                     (0, 270), (160, 420))

    im = ax.imshow(zi, origin='lower', vmin=min(survModelsRatLow), vmax=max(survModelsRatLow),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # where the points are
    ax.scatter(msLow, mxLow, facecolor=scatterFacecolor, s=scatterMarkersize)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'survived models (%)',
                                     xlims=(0, 270), ylims=(160, 420),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(survModelsRatLow)):
        if 80 < msLow[i] and mxLow[i] < 260:
            continue
        else:
            ax.annotate('{:.2f}'.format(survModelsRatLow[i]), (msLow[i], mxLow[i]),
                        textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, 
                        path_effects=[pe.withStroke(linewidth=linewidth, foreground='w')])

    # subregion of the original image
    x1, x2, y1, y2 = 86, 117, 215, 257
    axins = ax.inset_axes([200, 250, 60, 60],
                          transform=ax.transData,
                          xlim=(x1, x2), ylim=(y1, y2),
                          xticklabels=[], yticklabels=[])

    for i in range(len(survModelsRatLow)):
        if 80 > msLow[i] and mxLow[i] > 260:
            continue
        else:
            axins.annotate('{:.2f}'.format(survModelsRatLow[i]), (msLow[i], mxLow[i]),
                        textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, 
                        path_effects=[pe.withStroke(linewidth=linewidth, foreground='w')])

    axins.imshow(zi, origin='lower', vmin=min(survModelsRatLow), vmax=max(survModelsRatLow),
                 extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # where the points are
    axins.scatter(msLow, mxLow, facecolor=scatterFacecolor, s=scatterMarkersize)

    ax.indicate_inset_zoom(axins, edgecolor="black")


    ax.legend(title=title,
              loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ObsLim_XSH_bbgamgam_survModel_lowmass.pdf'))
    plt.close()


    ## medium mass

    fig, ax = plt.subplots()

    msMed, mxMed, survModelsRatMed = cutter(ms, mx, survModelsRat,
                                         (0, 525), (420, 620))

    im = ax.imshow(zi, origin='lower', vmin=min(survModelsRatMed), vmax=max(survModelsRatMed),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # where the points are
    ax.scatter(msMed, mxMed, facecolor=scatterFacecolor, s=scatterMarkersize)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'survived models (%)',
                                     xlims=(15, 510), ylims=(415, 620),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(survModelsRatMed)):
        ax.annotate('{:.2f}'.format(survModelsRatMed[i]), (msMed[i], mxMed[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, 
                    path_effects=[pe.withStroke(linewidth=linewidth, foreground='w')])

    ax.legend(title=title,
              loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ObsLim_XSH_bbgamgam_survModel_mediummass.pdf'))
    plt.close()


    ## high mass

    fig, ax = plt.subplots()

    msHigh, mxHigh, survModelsRatHigh = cutter(ms, mx, survModelsRat,
                                        (0, 525), (620, 1200))

    im = ax.imshow(zi, origin='lower', vmin=min(survModelsRatHigh), vmax=max(survModelsRatHigh),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # where the points are
    ax.scatter(msHigh, mxHigh, facecolor=scatterFacecolor, s=scatterMarkersize)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'survived models (%)',
                                     xlims=(40, 535), ylims=(620, 1080),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(survModelsRatHigh)):
        ax.annotate('{:.2f}'.format(survModelsRatHigh[i]), (msHigh[i], mxHigh[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=8, rotation=rotation, 
                    path_effects=[pe.withStroke(linewidth=linewidth, foreground='w')])

    ax.legend(title=title,
              loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ObsLim_XSH_bbgamgam_survModel_highmass.pdf'))
    plt.close()


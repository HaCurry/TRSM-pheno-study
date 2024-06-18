import json
import os

import pandas
import numpy as np
import scipy.interpolate
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
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

    # path to plots
    # E: (or you can leave it as is)
    pathPlots = os.path.join(pathRepo, 'AtlasLimits', 'plots')

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


    ## read in the 2023 Atlas limits
    limitsUntransposed = pandas.read_json(os.path.join(pathRepo, 'Atlas2023Limits.json'))
    print(limitsUntransposed)
    limits = limitsUntransposed.T
    print(limits)

    ms = [element for element in limits['S']]
    mx = [element for element in limits['X']]

    # save it in pb
    XS = [element for element in 10**(-3) * limits['ObservedLimit']]
    dataIds = [element for element in limits.index]

    # normalize the limits by the SM ggF di-Higgs cross section
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH
    # and bbgamgam BR
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR?sortcol=0;table=1;up=0#sorted_table

    norm = (31.05 * 10**(-3)) * 0.002637 

    # annotation settings
    fontsize = 10
    rotation = 45
    color = 'red'

    # annotation path effects
    path_effects = [pe.withStroke(linewidth=0.0, foreground='black')]

    # BP2 BP3 dashed line settings
    axvlineColor = 'blue'
    axvlineLinestyle = 'dashed'
    axvlineLinewidth = 1
    axvlineLabel = r'$\text{BP2}\leftrightarrow\text{BP3}$'

    # scatter settings
    scatterFacecolor = 'black'
    scatterMarkersize = 15

    # legend settings
    title = '$\sqrt{s}=13$ TeV\n$gg\\to X\\to S(b\\bar{b}) H(\gamma \gamma)$\n95% C.L observed limit\n\
$ref=gg\\to h_{SM}h_{SM}\\to b\\bar{b}\gamma\gamma$'
    
    msLini, mxLini = np.linspace(min(ms), max(ms), 800), np.linspace(min(mx), max(mx), 1000)
    msMeshi, mxMeshi = np.meshgrid(msLini, mxLini)

    zi = scipy.interpolate.griddata((ms, mx), np.array(XS)/norm, (msMeshi, mxMeshi), method='cubic')

    print(zi)
    print(f'nanmax: {np.nanmax(zi)} and actual max {np.nanmax(np.array(XS)/norm)}')


    ## low mass

    fig, ax = plt.subplots()

    msLow, mxLow, XSnormLow = cutter(ms, mx, np.array(XS)/norm,
                                     (0, 270), (160, 420))

    im = ax.imshow(zi, origin='lower', vmin=min(XSnormLow), vmax=max(XSnormLow),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    ax.axvline(125.09, color=axvlineColor, linestyle=axvlineLinestyle, linewidth=axvlineLinewidth)

    # where the points are
    ax.scatter(msLow, mxLow, facecolor=scatterFacecolor, s=scatterMarkersize)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(ref)$',
                                     xlims=(0, 270), ylims=(160, 420),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(XSnormLow)):
        if 80 < msLow[i] and mxLow[i] < 260:
            continue
        else:
            ax.annotate('{:.1f}'.format(XSnormLow[i]), (msLow[i], mxLow[i]),
                        textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, color=color, 
                        path_effects=path_effects)

    # subregion of the original image
    x1, x2, y1, y2 = 86, 117, 215, 257
    axins = ax.inset_axes([200, 250, 60, 60],
                          transform=ax.transData,
                          xlim=(x1, x2), ylim=(y1, y2),
                          xticklabels=[], yticklabels=[])

    for i in range(len(XSnormLow)):
        if 80 > msLow[i] and mxLow[i] > 260:
            continue
        else:
            axins.annotate('{:.1f}'.format(XSnormLow[i]), (msLow[i], mxLow[i]),
                        textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, color=color, 
                        path_effects=path_effects)

    # axins.scatter(msLow, mxLow, c=XSnormLow)
    axins.imshow(zi, origin='lower', vmin=min(XSnormLow), vmax=max(XSnormLow),
                 extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # where the points are
    axins.scatter(msLow, mxLow, facecolor=scatterFacecolor, s=scatterMarkersize)

    ax.indicate_inset_zoom(axins, edgecolor="black")

    ax.legend(title=title,
              handles=[
              mlines.Line2D([], [], linestyle=axvlineLinestyle, linewidth=axvlineLinewidth, color=axvlineColor, label=axvlineLabel),
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'AtlasLimits_lowmass.pdf'))
    plt.close()


    ## medium mass

    fig, ax = plt.subplots()

    msMed, mxMed, XSnormMed = cutter(ms, mx, np.array(XS)/norm,
                                     (0, 525), (420, 620))

    im = ax.imshow(zi, origin='lower', vmin=min(XSnormMed), vmax=max(XSnormMed),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    ax.axvline(125.09, color=axvlineColor, linestyle=axvlineLinestyle, linewidth=axvlineLinewidth)

    # where the points are
    ax.scatter(msMed, mxMed, facecolor=scatterFacecolor, s=scatterMarkersize)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(ref)$',
                                     xlims=(15, 490), ylims=(420, 610),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(XSnormMed)):
        ax.annotate('{:.1f}'.format(XSnormMed[i]), (msMed[i], mxMed[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, color=color, 
                    path_effects=path_effects)

    ax.legend(title=title,
              handles=[
              mlines.Line2D([], [], linestyle=axvlineLinestyle, linewidth=axvlineLinewidth, color=axvlineColor, label=axvlineLabel),
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'AtlasLimits_mediummass.pdf'))
    plt.close()


    ## high mass

    fig, ax = plt.subplots()

    msHigh, mxHigh, XSnormHigh = cutter(ms, mx, np.array(XS)/norm,
                                        (0, 525), (620, 1200))

    im = ax.imshow(zi, origin='lower', vmin=min(XSnormHigh), vmax=max(XSnormHigh),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    ax.axvline(125.09, color=axvlineColor, linestyle=axvlineLinestyle, linewidth=axvlineLinewidth)

    # where the points are
    ax.scatter(msHigh, mxHigh, facecolor=scatterFacecolor, s=scatterMarkersize)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(ref)$',
                                     xlims=(40, 525), ylims=(620, 1200),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(XSnormHigh)):
        ax.annotate('{:.1f}'.format(XSnormHigh[i]), (msHigh[i], mxHigh[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, color=color, 
                    path_effects=path_effects)

    ax.legend(title=title,
              handles=[
              mlines.Line2D([], [], linestyle=axvlineLinestyle, linewidth=axvlineLinewidth, color=axvlineColor, label=axvlineLabel),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'AtlasLimits_highmass.pdf'))
    plt.close()

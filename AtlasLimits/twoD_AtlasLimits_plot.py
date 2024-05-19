import json
import os

import pandas
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
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

    # normalize the limits by the SM di-Higgs to bbgamgam cross section
    # norm = (31.05 * 10**(-3)) * 0.002637
    norm = (31.02 * 10**(-3) * 0.0026)

    fontsize = 12
    rotation = 45
    linewidth = 2.0

    ## low mass

    fig, ax = plt.subplots()

    msLow, mxLow, XSnormLow = cutter(ms, mx, np.array(XS)/norm,
                                     (0, 270), (160, 420))

    im = ax.scatter(msLow, mxLow, c=XSnormLow)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(ref)$',
                                     xlims=(0, 270), ylims=(160, 420),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(XSnormLow)):
        ax.annotate('{:.1f}'.format(XSnormLow[i]), (msLow[i], mxLow[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, 
                    path_effects=[pe.withStroke(linewidth=linewidth, foreground='w')])

    # BP2
    ax.add_patch(mpatches.Rectangle((1,126), 123, 874,
                 linewidth=1, edgecolor='r', facecolor='none',
                 hatch=r'//\\', alpha=0.25, zorder=0))

    # BP3
    ax.add_patch(mpatches.Rectangle((126,255), 374, 745,
                 linewidth=1, edgecolor='b', facecolor='none',
                 hatch=r'//\\', alpha=0.25, zorder=0))

    # subregion of the original image
    x1, x2, y1, y2 = 86, 117, 215, 257
    axins = ax.inset_axes([200, 250, 60, 60],
                          transform=ax.transData,
                          xlim=(x1, x2), ylim=(y1, y2),
                          xticklabels=[], yticklabels=[])

    axins.scatter(msLow, mxLow, c=XSnormLow)

    ax.indicate_inset_zoom(axins, edgecolor="black")

    title = 'ATLAS $\sqrt{s}=13$ TeV\n$gg\\to X\\to S(b\\bar{b}) H(\gamma \gamma)$\n95% C.L observed limit\n\
$ref=gg\\to h_{SM}h_{SM}\\to b\\bar{b}\gamma\gamma$'
    ax.legend(title=title,
              handles=[
              mpatches.Patch(linewidth=0, fill=None, alpha=0.25, color='r', hatch=r'//\\', label='BP2'),
              mpatches.Patch(linewidth=0, fill=None, alpha=0.25, color='b', hatch=r'//\\', label='BP3'),
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'AtlasLimits_lowmass.pdf'))
    plt.close()


    ## medium mass

    fig, ax = plt.subplots()

    msMed, mxMed, XSnormMed = cutter(ms, mx, np.array(XS)/norm,
                                     (0, 525), (420, 620))

    im = ax.scatter(msMed, mxMed, c=XSnormMed)
    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(ref)$',
                                     xlims=(15, 490), ylims=(420, 610),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(XSnormMed)):
        ax.annotate('{:.1f}'.format(XSnormMed[i]), (msMed[i], mxMed[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, 
                    path_effects=[pe.withStroke(linewidth=linewidth, foreground='w')])

    # BP2
    ax.add_patch(mpatches.Rectangle((1,126), 123, 874,
                 linewidth=1, edgecolor='r', facecolor='none',
                 hatch=r'//\\', alpha=0.25, zorder=0))

    # BP3
    ax.add_patch(mpatches.Rectangle((126,255), 374, 745,
                 linewidth=1, edgecolor='b', facecolor='none',
                 hatch=r'//\\', alpha=0.25, zorder=0))

    title = 'ATLAS $\sqrt{s}=13$ TeV\n$gg\\to X\\to S(b\\bar{b}) H(\gamma \gamma)$\n95% C.L observed limit\n\
$ref=gg\\to h_{SM}h_{SM}\\to b\\bar{b}\gamma\gamma$'
    ax.legend(title=title,
              handles=[
              mpatches.Patch(linewidth=0, fill=None, alpha=0.25, color='r', hatch=r'//\\', label='BP2'),
              mpatches.Patch(linewidth=0, fill=None, alpha=0.25, color='b', hatch=r'//\\', label='BP3'),
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'AtlasLimits_mediummass.pdf'))
    plt.close()


    ## high mass

    fig, ax = plt.subplots()

    msHigh, mxHigh, XSnormHigh = cutter(ms, mx, np.array(XS)/norm,
                                        (0, 525), (620, 1200))

    im = ax.scatter(msHigh, mxHigh, c=XSnormHigh)
    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(ref)$',
                                     xlims=(0, 525), ylims=(620, 1200),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(XSnormHigh)):
        ax.annotate('{:.1f}'.format(XSnormHigh[i]), (msHigh[i], mxHigh[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=fontsize, rotation=rotation, 
                    path_effects=[pe.withStroke(linewidth=linewidth, foreground='w')])

    # BP2
    ax.add_patch(mpatches.Rectangle((1,126), 123, 874,
                 linewidth=1, edgecolor='r', facecolor='none',
                 hatch=r'//\\', alpha=0.25, zorder=0))

    # BP3
    ax.add_patch(mpatches.Rectangle((126,255), 374, 745,
                 linewidth=1, edgecolor='b', facecolor='none',
                 hatch=r'//\\', alpha=0.25, zorder=0))

    title = 'ATLAS $\sqrt{s}=13$ TeV\n$gg\\to X\\to S(b\\bar{b}) H(\gamma \gamma)$\n95% C.L observed limit\n\
$ref=gg\\to h_{SM}h_{SM}\\to b\\bar{b}\gamma\gamma$'
    ax.legend(title=title,
              handles=[
              mpatches.Patch(linewidth=0, fill=None, alpha=0.25, color='r', hatch=r'//\\', label='BP2'),
              mpatches.Patch(linewidth=0, fill=None, alpha=0.25, color='b', hatch=r'//\\', label='BP3'),
              ], loc='upper left', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'AtlasLimits_highmass.pdf'))
    plt.close()

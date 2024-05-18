import json
import os

import pandas
import numpy as np
import scipy.interpolate
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
import mplhep as hep

from helpScannerS import twoDPlotter as twoDPlot

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
    norm = (31.05 * 10**(-3)) * 0.002637
    norm = (31.02 * 10**(-3) * 0.0026)

    ## low mass

    fig, ax = plt.subplots()

    # x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ms, mx, np.array(XS)/norm)

    msi, mxi = np.linspace(min(ms), max(ms), 100), np.linspace(min(mx), max(mx), 200)
    msi, mxi = np.meshgrid(msi, mxi)

    zi = scipy.interpolate.griddata((ms, mx), np.array(XS)/norm, (msi, mxi), method='linear')

    print(zi)
    print(f'nanmax: {np.nanmax(zi)}')

    # im = ax.scatter(ms, mx, c=np.array(XS)/norm)
    im = ax.imshow(zi, origin='lower',
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(ref)$',
                                     xlims=(0, 270), ylims=(160, 420),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(XS)):
        ax.annotate('{:.1f}'.format(XS[i]/norm), (ms[i], mx[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                    path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])

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

    plt.savefig(os.path.join(pathPlots, 'AtlasLimits_lowmass.pdf'))
    plt.close()


    ## medium mass

    fig, ax = plt.subplots()

    im = ax.scatter(ms, mx, c=np.array(XS)/norm)
    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(ref)$',
                                     xlims=(0, 525), ylims=(420, 620),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(XS)):
        ax.annotate('{:.1f}'.format(XS[i]/norm), (ms[i], mx[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                    path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])

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

    plt.savefig(os.path.join(pathPlots, 'AtlasLimits_mediummass.pdf'))
    plt.close()


    ## high mass

    fig, ax = plt.subplots()

    im = ax.scatter(ms, mx, c=np.array(XS)/norm)
    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\sigma(obs)/\sigma(ref)$',
                                     xlims=(0, 525), ylims=(620, 1200),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(XS)):
        ax.annotate('{:.1f}'.format(XS[i]/norm), (ms[i], mx[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45, 
                    path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])

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

    plt.savefig(os.path.join(pathPlots, 'AtlasLimits_highmass.pdf'))
    plt.close()

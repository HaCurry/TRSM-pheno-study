import os
import json

import pandas
import numpy as np
import scipy.interpolate
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import mplhep as hep
from helpScannerS import functions as TRSM
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
    # E: (or you can leave as is)
    pathPlots = os.path.join(pathRepo, 'testing', 'MadGraph_ResonVsNonReson',
                             'plots')

    # path to ScannerS values at Atlas limit points
    pathMadgraph = os.path.join(pathRepo, 'testing', 'MadGraph_ResonVsNonReson',
                                'MadgraphResonVsNonReson.tsv')

    os.makedirs(pathPlots, exist_ok=True)

    # path to ScannerS output with BP2 and BP3 settings (for hatching constraints)
    pathScannerSBP2 = os.path.join(pathRepo, 'Benchmarkplanes',
                                   'BPs_extendedmass', 'BP2', 'output_BP2.tsv')
    pathScannerSBP3 = os.path.join(pathRepo, 'Benchmarkplanes',
                                   'BPs_extendedmass', 'BP3', 'output_BP3.tsv')

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

    dfMadgraph = pandas.read_table(pathMadgraph)

    ms = [dfMadgraph['ms'][i] for i in range(len(dfMadgraph))]
    mx = [dfMadgraph['mx'][i] for i in range(len(dfMadgraph))]
    pp_iota0_eta0h = [dfMadgraph['pp_iota0_eta0h'][i] for i in range(len(dfMadgraph))]
    pp_eta0h = [dfMadgraph['pp_eta0h'][i] for i in range(len(dfMadgraph))]
    ratio = [dfMadgraph['ratio'][i] for i in range(len(dfMadgraph))]

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

    # constraint hatching settings
    constraints = {'BFB': '++', 'Higgs': r'//', 'STU': r'\\ ', 'Uni': '..'}
    alpha = 0.1
    
    # ScannerS output for constraint hatching
    ScannerS_BP2 = TRSM.observables(pathScannerSBP2 ,
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    'valid_BFB', 'valid_Higgs',
                                    'valid_STU', 'valid_Uni',
                                    kineticExclude=True)

    ScannerS_BP3 = TRSM.observables(pathScannerSBP3 ,
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    'valid_BFB', 'valid_Higgs', 
                                    'valid_STU', 'valid_Uni',
                                    kineticExclude=True)

    # legend settings
    title = '$\sqrt{s}=13$ TeV'

    # create a fit out of all the points, this fit is used to plot the color plots
    msLini, mxLini = np.linspace(min(ms), max(ms), 800), np.linspace(min(mx), max(mx), 1000)
    msMeshi, mxMeshi = np.meshgrid(msLini, mxLini)

    zi = scipy.interpolate.griddata((ms, mx), ratio, (msMeshi, mxMeshi), method='cubic')

    print(f'nanmax: {np.nanmax(zi)} and actual max {np.nanmax(ratio)}')


    ## low mass

    fig, ax = plt.subplots()

    msLow, mxLow, ratioLow = cutter(ms, mx, ratio,
                                     (0, 270), (160, 420))

    im = ax.imshow(zi, origin='lower', vmin=min(ratioLow), vmax=max(ratioLow),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # plot the constraints according to the patterns below below
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP2, 'mH1', 'mH3', 
                                            f'valid_{key}',
                                            ax, constraints[key], alpha=alpha)
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3', 
                                            f'valid_{key}',
                                            ax, constraints[key], alpha=alpha)

    ax.axvline(125.09, color=axvlineColor, linestyle=axvlineLinestyle,
               linewidth=axvlineLinewidth)

    # where the points are
    ax.scatter(msLow, mxLow, facecolor=scatterFacecolor, s=scatterMarkersize)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\left.\sigma(gg\to SH) \right/ \sigma(gg \to X \to SH)$',
                                     xlims=(0, 270), ylims=(160, 420),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(ratioLow)):
        if 80 < msLow[i] and mxLow[i] < 260:
            continue
        else:
            ax.annotate('{:.3f}'.format(ratioLow[i]), (msLow[i], mxLow[i]),
                        textcoords='offset points', xytext=(-3, -2),
                        fontsize=fontsize, rotation=rotation, color=color,
                        path_effects=path_effects)
                        

    # subregion of the original image
    x1, x2, y1, y2 = 86, 117, 215, 257
    axins = ax.inset_axes([200, 250, 60, 60],
                          transform=ax.transData,
                          xlim=(x1, x2), ylim=(y1, y2),
                          xticklabels=[], yticklabels=[])

    for i in range(len(ratioLow)):
        if 80 > msLow[i] and mxLow[i] > 260:
            continue
        else:
            axins.annotate('{:.3f}'.format(ratioLow[i]), (msLow[i], mxLow[i]),
                           textcoords='offset points', xytext=(-3, -2),
                           fontsize=fontsize, rotation=rotation, color=color,
                           path_effects=path_effects)

    axins.imshow(zi, origin='lower', vmin=min(ratioLow), vmax=max(ratioLow),
                 extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # where the points are
    axins.scatter(msLow, mxLow, facecolor=scatterFacecolor, s=scatterMarkersize)

    ax.indicate_inset_zoom(axins, edgecolor="black")

    ax.legend(title=title,
              handles=[
              mlines.Line2D([], [], linestyle=axvlineLinestyle, linewidth=axvlineLinewidth, color=axvlineColor, label=axvlineLabel),
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ResonVsNonResonRatio_lowmass.pdf'))
    plt.close()


    ## medium mass

    fig, ax = plt.subplots()

    msMed, mxMed, ratioMed = cutter(ms, mx, ratio,
                                     (0, 525), (420, 620))

    im = ax.imshow(zi, origin='lower', vmin=min(ratioMed), vmax=max(ratioMed),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # plot the constraints according to the patterns below below
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP2, 'mH1', 'mH3', 
                                            f'valid_{key}',
                                            ax, constraints[key], alpha=alpha)
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3', 
                                            f'valid_{key}',
                                            ax, constraints[key], alpha=alpha)

    ax.axvline(125.09, color=axvlineColor, linestyle=axvlineLinestyle,
               linewidth=axvlineLinewidth)

    # where the points are
    ax.scatter(msMed, mxMed, facecolor=scatterFacecolor, s=scatterMarkersize)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\left.\sigma(gg\to SH) \right/ \sigma(gg \to X \to SH)$',
                                     xlims=(15, 490), ylims=(415, 620),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(ratioMed)):
        ax.annotate('{:.3f}'.format(ratioMed[i]), (msMed[i], mxMed[i]),
                    textcoords='offset points', xytext=(-3, -2),
                    fontsize=fontsize, rotation=rotation, color=color,
                    path_effects=path_effects)

    ax.legend(title=title,
              handles=[
              mlines.Line2D([], [], linestyle=axvlineLinestyle, linewidth=axvlineLinewidth, color=axvlineColor, label=axvlineLabel),
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mpatches.Patch(linewidth=0, fill=None, hatch='//', label='HiggsBounds'),
              mpatches.Patch(linewidth=0, fill=None, hatch='..', label='Unitarity'),
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ResonVsNonResonRatio_mediummass.pdf'))
    plt.close()


    ## high mass

    fig, ax = plt.subplots()

    msHigh, mxHigh, ratioHigh = cutter(ms, mx, ratio,
                                        (0, 525), (620, 1200))

    im = ax.imshow(zi, origin='lower', vmin=min(ratioHigh), vmax=max(ratioHigh),
                   extent=[min(ms), max(ms), min(mx), max(mx)], aspect='auto')

    # plot the constraints according to the patterns below below
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP2, 'mH1', 'mH3', f'valid_{key}',
                                            ax, constraints[key], alpha=alpha)
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3', f'valid_{key}',
                                            ax, constraints[key], alpha=alpha)

    ax.axvline(125.09, color=axvlineColor, linestyle=axvlineLinestyle,
               linewidth=axvlineLinewidth)

    # where the points are
    ax.scatter(msHigh, mxHigh, facecolor=scatterFacecolor, s=scatterMarkersize)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{S}$ [GeV]', r'$M_{X}$ [GeV]',
                                     r'$\left.\sigma(gg\to SH) \right/ \sigma(gg \to X \to SH)$',
                                     xlims=(40, 535), ylims=(620, 1300),
                                     fig=fig, ax=ax, im=im)

    for i in range(len(ratioHigh)):
        ax.annotate('{:.3f}'.format(ratioHigh[i]), (msHigh[i], mxHigh[i]),
                    textcoords='offset points', xytext=(-3,-2), fontsize=8, rotation=rotation, color=color,
                    path_effects=path_effects)

    ax.legend(title=title,
              handles=[
              mlines.Line2D([], [], linestyle=axvlineLinestyle, linewidth=axvlineLinewidth, color=axvlineColor, label=axvlineLabel),
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mpatches.Patch(linewidth=0, fill=None, hatch='..', label='Unitarity'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'ResonVsNonResonRatio_highmass.pdf'))
    plt.close()


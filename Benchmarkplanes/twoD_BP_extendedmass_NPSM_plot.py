from helpScannerS import functions as TRSM
from helpScannerS import twoDPlotter as twoDPlot

import os
import json

import numpy as np
import pandas
import scipy.interpolate
from scipy.interpolate import CubicSpline

import mplhep as hep
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

if __name__ == '__main__': 

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to plotting directory
    pathPlots = os.path.join(pathRepo, 'Benchmarkplanes', 'plots')

    # create directories inside plotting directory for saving figures
    os.makedirs(pathPlots, exist_ok=True)
    os.makedirs(os.path.join(pathPlots, 'BP2'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, 'BP3'), exist_ok=True)


    path13_BP = os.path.join(pathRepo, 'Benchmarkplanes', 'BPs_extendedmass')

    # path to 13 TeV TRSM ScannerS cross sections with BP2 settings
    path13_BP2 = os.path.join(path13_BP, 'BP2', 'output_BP2.tsv')

    # path to 13 TeV TRSM ScannerS cross sections with BP3 settings
    path13_BP3 = os.path.join(path13_BP, 'BP3', 'output_BP3.tsv')

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

    contourFontsize = 13

    ## BP2

    # calculate the cross sections of gg -> H3 -> H1(bb)H2(gamgam) at 13 TeV with BP2 settings.
    # This is done by using the NWA where the branching ratio H3 -> H1 H2, H1(bb)H2(gamgam) is 
    # generated by the ScannerS TRSM executable (path13_BP2, path13_BP3) and the gg -> H3
    # cross section is generated elsewhere at 13 TeV (see twoD_ScannerSCrossSections.py)
    ScannerS_BP2 = TRSM.observables(path13_BP2, 
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    'valid_BFB', 'valid_Higgs',
                                    'valid_STU', 'valid_Uni',
                                    kineticExclude=True)

    # BP2 13 TeV gg -> H3 -> H1(bb) H2(gamgam)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP2['mH1'],
                                            ScannerS_BP2['mH3'],
                                            ScannerS_BP2['x_H3_H1_bb_H2_gamgam'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [1, 2, 3, 10]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower', linewidths=0.75, colors='red')
    manualLabelPositions = [(75, 460), (40, 360), (50, 310),
                            (32.5, 260), (20, 170)]
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelPositions)

    # the line M3 = M1 + M2
    ax.plot([1, 124], [1 + 125.09, 124 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b})~h_{2}(\gamma\gamma)) \right/ \sigma(ref)$',
                                     xlims=(-3, 127), ylims=(117, 1010),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP2, 'mH1', 'mH3',
                                            f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    # ax.legend(title='BP2 $\sqrt{s}=13$ TeV:\n$h_1=S$, $h_2=H$, $h_3=X$\n$ref=gg\\to h_{SM}h_{SM}\\to b\\bar{b}\gamma\gamma$',
    ax.legend(title='BP2 $\sqrt{s}=13$ TeV:\n$h_1=S$, $h_2=H$, $h_3=X$\n$ref=gg\\to h_{SM}h_{SM}\\to b\\bar{b}\gamma\gamma$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP2', 'BP2_extendedmass_extendedmass_XS_XSH_bbgamgam_1.pdf'))
    plt.close()

    del x, y, z, xi, yi


    # BP2 13 TeV gg -> H3 -> H1(gamgam) H2(bb)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP2['mH1'],
                                            ScannerS_BP2['mH3'],
                                            ScannerS_BP2['x_H3_H1_gamgam_H2_bb'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0.1, 0.25, 0.5, 0.75, 1.25, 1.5]
    cont = ax.contour(xi, yi, zi, levels, origin='lower', linewidths=0.75, colors='red')
    manualLabelsPositions = [(35, 285), (50, 280), (67.5, 270),
                             (80, 265), (100, 260), (120, 375), 
                             (112.5, 255)]
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelsPositions)

    # the line M3 = M1 + M2
    ax.plot([1, 124], [1 + 125.09, 124 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D('',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\left.\sigma(gg\to h_{3} \to h_{1}(\gamma\gamma)~h_{2}(b\bar{b})) \right/ \sigma(ref)$',
                                     xlims=(-3, 127), ylims=(110, 1010),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP2, 'mH1', 'mH3',
                                            f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    ax.legend(title='BP2 $\sqrt{s}=13$ TeV:\n$h_1=S$, $h_2=H$, $h_3=X$\n$ref=gg\\to h_{SM}h_{SM}\\to b\\bar{b}\gamma\gamma$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP2', 'BP2_extendedmass_XS_XSH_bbgamgam_2.pdf'))
    plt.close()

    del x, y, z, xi, yi


    ## BP3

    ScannerS_BP3 = TRSM.observables(path13_BP3,
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    'valid_BFB', 'valid_Higgs',
                                    'valid_STU', 'valid_Uni',
                                    kineticExclude=True)


    # BP3 13 TeV gg -> H3 -> H1(bb) H2(gamgam)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP3['mH2'],
                                            ScannerS_BP3['mH3'],
                                            ScannerS_BP3['x_H3_H1_bb_H2_gamgam'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0.01, 0.1, 1, 4]
    manualLabelsPositions = [(160, 420), (180, 460), (250, 510), (135, 290),
                             (135, 370)]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower',
                      linewidths=0.75, colors='red')
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelsPositions)

    # the line M3 = M1 + M2
    ax.plot([126, 500], [126 + 125.09, 500 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{2}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b})~h_{2}(\gamma\gamma)) \right/ \sigma(ref)$',
                                     xlims=(115, 510), ylims=(245, 1060),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3',
                                            f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    ax.legend(title='BP3 $\sqrt{s}=13$ TeV:\n$h_1=H$, $h_2=S$, $h_3=X$\n$ref=gg\\to h_{SM}h_{SM}\\to b\\bar{b}\gamma\gamma$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mpatches.Patch(linewidth=0, fill=None, hatch='//', label='HiggsBounds'),
              mpatches.Patch(linewidth=0, fill=None, hatch='..', label='Unitarity'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP3', 'BP3_extendedmass_extendedmass_XS_XSH_bbgamgam_1.pdf'))
    plt.close()

    del x, y, z, xi, yi


    ## BP3 13 TeV gg -> H3 -> H1(gamgam) H2(bb)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP3['mH2'],
                                            ScannerS_BP3['mH3'],
                                            ScannerS_BP3['x_H3_H1_gamgam_H2_bb'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0, 0.01, 0.1, 1, 3]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower',
                      linewidths=0.75, colors='red')
    manualLabelPositions = [(130, 380), (150, 450), (160, 510),
                            (180, 570)]
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelPositions)

    # the line M3 = M1 + M2
    ax.plot([126, 500], [126 + 125.09, 500 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{2}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\left.\sigma(gg\to h_{3} \to h_{1}(\gamma\gamma)~h_{2}(b\bar{b})) \right/ \sigma(ref)$',
                                     xlims=(115, 510), ylims=(245, 1060),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3',
                                            f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    ax.legend(title='BP3 $\sqrt{s}=13$ TeV:\n$h_1=H$, $h_2=S$, $h_3=X$\n$ref=gg\\to h_{SM}h_{SM}\\to b\\bar{b}\gamma\gamma$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mpatches.Patch(linewidth=0, fill=None, hatch='//', label='HiggsBounds'),
              mpatches.Patch(linewidth=0, fill=None, hatch='..', label='Unitarity'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP3', 'BP3_extendedmass_XS_XSH_bbgamgam_2.pdf'))
    plt.close()

    del x, y, z, xi, yi

    # everything below this comment can be ignored (some sanity checks)
    print('Running some sanity checks, this can be ignored...')

    ScannerS_BP2 = TRSM.observables(path13_BP2,
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    normSM=1,
                                    kineticExclude=False)

    ScannerS_BP3 = TRSM.observables(path13_BP3,
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    normSM=1,
                                    kineticExclude=False)


    ScannerS_BP2_H1H2, ScannerS_BP2_H1H1, ScannerS_BP2_H2H2 = TRSM.ppXNPSM_massfree(path13_BP2,
                                                                                    'mH1', 'mH2', 'mH3', 'bb', 'gamgam', 
                                                                                    normalizationSM=1, run3=True)

    ScannerS_BP3_H1H2, ScannerS_BP3_H1H1, ScannerS_BP3_H2H2 = TRSM.ppXNPSM_massfree(path13_BP3,
                                                                                    'mH1', 'mH2', 'mH3', 'bb', 'gamgam',
                                                                                    normalizationSM=1, run3=True)

    TRSM.comparer(ScannerS_BP2, ScannerS_BP2_H1H2)
    TRSM.comparer(ScannerS_BP3, ScannerS_BP3_H1H2)

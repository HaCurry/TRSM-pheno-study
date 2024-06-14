import os
import json

import scipy.interpolate
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import mplhep as hep
from helpScannerS import functions as TRSM
from helpScannerS import twoDPlotter as twoDPlot

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

    path13_BP = os.path.join(pathRepo, 'Benchmarkplanes', 'BPs_noconstraints')

    # path to 13 TeV TRSM ScannerS cross sections with BP2 settings
    path13_BP2 = os.path.join(path13_BP, 'BP2', 'output_BP2_noconstraints.tsv')

    # path to 13 TeV TRSM ScannerS cross sections with BP3 settings
    path13_BP3 = os.path.join(path13_BP, 'BP3', 'output_BP3_noconstraints.tsv')

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

    # standard model HH cross section
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH
    normCrossSec = 31.05 * 10**(-3)

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
                                    saveAll=True,
                                    kineticExclude=True)

    # BP2 13 TeV H3 -> H1 H2 (branching ratio)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP2['mH1'],
                                            ScannerS_BP2['mH3'],
                                            ScannerS_BP2['b_H3_H1H2'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0.2, 0.3, 0.4]
    manualLabelsPositions = [(20, 185), (42.5, 250), (65, 330)]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower',
                      linewidths=0.75, colors='red')
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelsPositions)

    # # change contour label edgecolor
    # plt.setp(clbls, path_effects=[pe.withStroke(linewidth=1, foreground="w")])

    # the line M3 = M1 + M2
    ax.plot([1, 124], [1 + 125.09, 124 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$BR(h_{3}\to h_{1} \ h_{2})$',
                                     xlims=(-3, 127), ylims=(117, 510),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP2, 'mH1', 'mH3',
                                            f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    ax.legend(title='BP2:\n$h_1=S$, $h_2=H$, $h_3=X$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP2', 'BP2_BR_XSH.pdf'))
    plt.close()

    del x, y, z, xi, yi


    # BP2 13 TeV gg -> H3 -> H1 H2 (cross section)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP2['mH1'],
                                            ScannerS_BP2['mH3'],
                                            [i/normCrossSec for i in 
                                                ScannerS_BP2['x_H3_H1H2']])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [i/normCrossSec for i in [0.1, 0.25, 0.5]]
    manualLabelsPositions = [(15, 160), (35, 205), (70, 280)]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower',
                      linewidths=0.75, colors='red')
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelsPositions, fmt='%1.1f')

    # the line M3 = M1 + M2
    ax.plot([1, 124], [1 + 125.09, 124 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D('',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\left.\sigma(gg \to h_{3}\to h_{1} \ h_{2})\right/ \sigma(ref)$',
                                     xlims=(-3, 127), ylims=(117, 510),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP2, 'mH1', 'mH3',
                                            f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    ax.legend(title='BP2:\n$h_1=S$, $h_2=H$, $h_3=X$\n$ref=gg\\to h_{SM}h_{SM}$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP2', 'BP2_XS_XSH.pdf'))
    plt.close()

    del x, y, z, xi, yi


    ## BP3

    ScannerS_BP3 = TRSM.observables(path13_BP3,
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    'valid_BFB', 'valid_Higgs',
                                    'valid_STU', 'valid_Uni',
                                    saveAll=True,
                                    kineticExclude=True)


    # BP3 13 TeV H3 -> H1 H2 (branching ratio)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP3['mH2'],
                                            ScannerS_BP3['mH3'],
                                            ScannerS_BP3['b_H3_H1H2'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0.35, 0.45, 0.5]
    manualLabelsPositions = [(340, 470), (250, 420), (180, 340)]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower',
                      linewidths=0.75, colors='red')
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelsPositions)

    # the line M3 = M1 + M2
    ax.plot([126, 500], [126 + 125.09, 500 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{2}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$BR(h_{3}\to h_{1} \ h_{2})$',
                                     xlims=(115, 510), ylims=(245, 660),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3', f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    ax.legend(title='BP3:\n$h_1=H$, $h_2=S$, $h_3=X$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mpatches.Patch(linewidth=0, fill=None, hatch='//', label='HiggsBounds'),
              mpatches.Patch(linewidth=0, fill=None, hatch='..', label='Unitarity'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP3', 'BP3_BR_XSH.pdf'))
    plt.close()

    del x, y, z, xi, yi


    ## BP3 13 TeV gg -> H3 -> H1 H2 (cross section)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP3['mH2'],
                                            ScannerS_BP3['mH3'],
                                            [i/normCrossSec for i in
                                                ScannerS_BP3['x_H3_H1H2']])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [i/normCrossSec for i in [0.05, 0.1, 0.2, 0.25, 0.3]]
    manualLabelsPositions = [(150, 590), (185, 510),
                             (165, 420), (155, 380), (145, 345),
                             (190, 365)]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower',
                      linewidths=0.75, colors='red')
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelsPositions, fmt='%1.1f')

    # the line M3 = M1 + M2
    ax.plot([126, 500], [126 + 125.09, 500 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{2}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\left.\sigma(gg \to h_{3}\to h_{1} \ h_{2})\right/ \sigma(ref)$',
                                     xlims=(115, 510), ylims=(245, 660),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3', f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    ax.legend(title='BP3:\n$h_1=H$, $h_2=S$, $h_3=X$\n$ref=gg\\to h_{SM}h_{SM}$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mpatches.Patch(linewidth=0, fill=None, hatch='//', label='HiggsBounds'),
              mpatches.Patch(linewidth=0, fill=None, hatch='..', label='Unitarity'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP3', 'BP3_XS_XSH.pdf'))
    plt.close()

    del x, y, z, xi, yi

    # everything below this comment can be ignored (some sanity checks)
    print('Running some sanity checks, this can be ignored...')

    ScannerS_BP2 = TRSM.observables(path13_BP2,
                                         'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                         normSM=1,
                                    saveAll=True,     
                                    kineticExclude=False)

    ScannerS_BP3 = TRSM.observables(path13_BP3,
                                         'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                         normSM=1,
                                    saveAll=True,     
                                    kineticExclude=False)


    ScannerS_BP2_H1H2, ScannerS_BP2_H1H1, ScannerS_BP2_H2H2 = TRSM.ppXNPSM_massfree(path13_BP2,
                                                                                       'mH1', 'mH2', 'mH3', 'bb', 'gamgam',
                                                                                       normalizationSM=1, run3=True)

    ScannerS_BP3_H1H2, ScannerS_BP3_H1H1, ScannerS_BP3_H2H2 = TRSM.ppXNPSM_massfree(path13_BP3,
                                                                                       'mH1', 'mH2', 'mH3', 'bb', 'gamgam',
                                                                                       normalizationSM=1, run3=True)

    TRSM.comparer(ScannerS_BP2, ScannerS_BP2_H1H2)
    TRSM.comparer(ScannerS_BP3, ScannerS_BP3_H1H2)

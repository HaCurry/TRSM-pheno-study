import os
import json

import numpy as np
import scipy.interpolate
import mplhep as hep
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from helpScannerS import functions as TRSM
from helpScannerS import twoDPlotter as twoDPlot

if __name__ == '__main__': 

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to plotting directory
    # E:
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

    contourFontsize = 13

    ## BP2

    ScannerS_BP2 = TRSM.observables(path13_BP2, 
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    'w_H3', 'w_H2', 'w_H1',
                                    'valid_BFB', 'valid_Higgs',
                                    'valid_STU', 'valid_Uni',
                                    kineticExclude=True)


    # BP2 \Gamma(H3)/M3

    NWA_BP2 = [ScannerS_BP2['w_H3'][i]/ScannerS_BP2['mH3'][i]
               for i in range(len(ScannerS_BP2['w_H3']))]

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP2['mH1'],
                                            ScannerS_BP2['mH3'],
                                            NWA_BP2)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0.0015, 0.0045, 0.0075, 0.0105]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower',
                      linewidths=0.75, colors='red')
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize)


    # the line M3 = M1 + M2
    ax.plot([1, 124], [1 + 125.09, 124 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\Gamma(h_{3})~/~M_{3}$',
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
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP2', 'BP2_NWA_H3.pdf'))
    plt.close()

    del x, y, z, xi, yi, NWA_BP2


    # BP2 \Gamma(H2)/M2

    NWA_BP2 = [ScannerS_BP2['w_H2'][i]/ScannerS_BP2['mH2'][i]
               for i in range(len(ScannerS_BP2['w_H2']))]

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP2['mH1'],
                                            ScannerS_BP2['mH3'],
                                            NWA_BP2)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0.5*10**(-7), 2*10**(-7)]
    manualLabelsPositions = [(10, 150), (17, 170), (37.5, 220),
                             (117, 375)]
    cont = ax.contour(xi, yi, zi, origin='lower',
                      linewidths=0.75, colors='red')
    # clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
    #                   manual=manualLabelsPositions )


    # the line M3 = M1 + M2
    ax.plot([1, 124], [1 + 125.09, 124 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\Gamma(h_{2})~/~M_{2}$',
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
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP2', 'BP2_NWA_H2.pdf'))
    plt.close()

    del x, y, z, xi, yi, NWA_BP2


    # BP2 \Gamma(H1)/M1

    NWA_BP2 = [ScannerS_BP2['w_H1'][i]/ScannerS_BP2['mH1'][i]
               for i in range(len(ScannerS_BP2['w_H1']))]

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP2['mH1'],
                                            ScannerS_BP2['mH3'],
                                            NWA_BP2)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0.5*10**(-7), 2*10**(-7)]
    manualLabelsPositions = [(10, 150), (17, 170), (37.5, 220),
                             (117, 375)]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower',
                      linewidths=0.75, colors='red')
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelsPositions )


    # the line M3 = M1 + M2
    ax.plot([1, 124], [1 + 125.09, 124 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\Gamma(h_{1})~/~M_{1}$',
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
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP2', 'BP2_NWA_H1.pdf'))
    plt.close()

    del x, y, z, xi, yi, NWA_BP2


    ## BP3

    ScannerS_BP3 = TRSM.observables(path13_BP3,
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    'w_H3', 'w_H2', 'w_H1',
                                    'valid_BFB', 'valid_Higgs',
                                    'valid_STU', 'valid_Uni',
                                    kineticExclude=True)


    # BP3 \Gamma(H3)/M3

    NWA_BP3 = [ScannerS_BP3['w_H3'][i]/ScannerS_BP3['mH3'][i]
               for i in range(len(ScannerS_BP3['w_H3']))]

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP3['mH2'],
                                            ScannerS_BP3['mH3'],
                                            NWA_BP3)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0.006, 0.018, 0.03, 0.042]
    manualLabelsPositions = [(145, 290), (180, 425),
                             (225, 549), (250, 640)]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower',
                      linewidths=0.75, colors='red')
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelsPositions)

    # the line M3 = M1 + M2
    ax.plot([126, 500], [126 + 125.09, 500 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{2}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\Gamma(h_{3})~/~M_{3}$',
                                     xlims=(115, 510), ylims=(245, 660),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3',
                                            f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    ax.legend(title='BP3:\n$h_1=H$, $h_2=S$, $h_3=X$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mpatches.Patch(linewidth=0, fill=None, hatch='//', label='HiggsBounds'),
              mpatches.Patch(linewidth=0, fill=None, hatch='..', label='Unitarity'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP3', 'BP3_NWA_H3.pdf'))
    plt.close()

    del x, y, z, xi, yi, NWA_BP3


    # BP3 \Gamma(H2)/M2

    NWA_BP3 = [ScannerS_BP3['w_H2'][i]/ScannerS_BP3['mH2'][i]
               for i in range(len(ScannerS_BP3['w_H2']))]

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP3['mH2'],
                                            ScannerS_BP3['mH3'],
                                            NWA_BP3)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0.0005, 0.0015, 0.0025,]
    manualLabelsPositions = [(270, 440), (380, 540),
                             (465, 630)]
    cont = ax.contour(xi, yi, zi, levels=levels, origin='lower',
                      linewidths=0.75, colors='red')
    clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
                      manual=manualLabelsPositions)

    # the line M3 = M1 + M2
    ax.plot([126, 500], [126 + 125.09, 500 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{2}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\Gamma(h_{2})~/~M_{2}$',
                                     xlims=(115, 510), ylims=(245, 660),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3',
                                            f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    ax.legend(title='BP3:\n$h_1=H$, $h_2=S$, $h_3=X$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mpatches.Patch(linewidth=0, fill=None, hatch='//', label='HiggsBounds'),
              mpatches.Patch(linewidth=0, fill=None, hatch='..', label='Unitarity'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP3', 'BP3_NWA_H2.pdf'))
    plt.close()

    del x, y, z, xi, yi, NWA_BP3


    # BP3 \Gamma(H1)/M1

    NWA_BP3 = [ScannerS_BP3['w_H1'][i]/ScannerS_BP3['mH1'][i]
               for i in range(len(ScannerS_BP3['w_H1']))]

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP3['mH2'],
                                            ScannerS_BP3['mH3'],
                                            NWA_BP3)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()

    # color plot
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # contour plot
    levels = [0.0005, 0.0015, 0.0025,]
    manualLabelsPositions = [(270, 440), (380, 540),
                             (465, 630)]
    cont = ax.contour(xi, yi, zi, origin='lower',
                      linewidths=0.75, colors='red')
    # clbls = ax.clabel(cont, inline=True, fontsize=contourFontsize,
    #                   manual=manualLabelsPositions)

    # the line M3 = M1 + M2
    ax.plot([126, 500], [126 + 125.09, 500 + 125.09],
            ls='dashed', color='k', linewidth=2)

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{2}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\Gamma(h_{1})~/~M_{1}$',
                                     xlims=(115, 510), ylims=(245, 660),
                                     fig=fig, ax=ax, im=im)

    # plot the constraints according to the patterns below below
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3',
                                            f'valid_{key}',
                                            ax, constraints[key])

    # custom legends for the constrained regions
    ax.legend(title='BP3:\n$h_1=H$, $h_2=S$, $h_3=X$',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mpatches.Patch(linewidth=0, fill=None, hatch='//', label='HiggsBounds'),
              mpatches.Patch(linewidth=0, fill=None, hatch='..', label='Unitarity'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$')
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP3', 'BP3_NWA_H1.pdf'))
    plt.close()

    del x, y, z, xi, yi, NWA_BP3

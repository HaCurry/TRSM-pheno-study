
from helpScannerS import functions as TRSM
from helpScannerS import twoDPlotter as twoDPlot

import os

import numpy as np
import pandas
import scipy.interpolate
from scipy.interpolate import CubicSpline

import mplhep as hep
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as mpe

if __name__ == '__main__': 

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to plotting directory
    # E:
    pathPlots = '/eos/user/i/ihaque/SusHiPlots' 

    # create directories inside plotting directory for saving figures
    os.makedirs(pathPlots, exist_ok=True)
    os.makedirs(os.path.join(pathPlots, '14TeV'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, '14TeV', 'BP2'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, '14TeV', 'BP3'), exist_ok=True)

    # path to 14 TeV gg > h_{SM} ScannerS cross sections
    path14 = os.path.join(pathRepo, 'testing', 'SusHi_HiggsCrossSections',
                          '14TeV_YR4CrossSections.tsv')

    # path to 13 TeV TRSM ScannerS cross sections with BP2 settings
    # path13_BP2 = os.path.join(pathRepo, 'plots2D', 'BP2_BR_XSH', 'output_BP2_BR_XSH.tsv')
    path13_BP2 = os.path.join(pathRepo, 'Benchmarkplanes', 'BPs_noconstraints',
                              'BP2', 'output_BP2_noconstraints.tsv')
    
    # path to 13 TeV TRSM ScannerS cross sections with BP3 settings
    # path13_BP3 = os.path.join(pathRepo, 'plots2D', 'BP3_BR_XSH', 'output_BP3_BR_XSH.tsv')
    path13_BP3 = os.path.join(pathRepo, 'Benchmarkplanes', 'BPs_noconstraints',
                              'BP3', 'output_BP3_noconstraints.tsv')

    # plotting style
    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19

    ## BP2

    # calculate the cross sections of gg -> H3 -> H1(bb)H2(gamgam) at 14 TeV with BP2 settings.
    # This is done by using the NWA where the branching ratio H3 -> H1 H2, H1(bb)H2(gamgam) is 
    # generated by the ScannerS TRSM executable (path13_BP2, path13_BP3) and the gg -> H3
    # cross section is generated elsewhere at 14 TeV (see twoD_ScannerSCrossSections.py)

    # normSM set to the HH cross section at 14 TeV according to
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH
    # and the bb gamgam branching ratio
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR?sortcol=0;table=1;up=0#sorted_table
    ScannerS_BP2_14 = TRSM.observables(path13_BP2,
                                       'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                       normSM=36.69 * 10**(-3) * 0.002637,
                                       kineticExclude=True,
                                       pathRun3Data=path14,
                                       keyMassRun3='mass',
                                       keyCrossSecRun3='SMCrossSec')

    # BP2 14 TeV gg -> H3 -> H1(bb) H2(gamgam)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP2_14['mH1'],
                                            ScannerS_BP2_14['mH3'],
                                            ScannerS_BP2_14['x_H3_H1_bb_H2_gamgam'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots()
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    cont = ax.contour(xi, yi, zi, origin='lower', linewidths=0.75, colors='k')
    manualLabelPositions = [(7, 150), (17.5, 160), (22.5, 165), (27.5, 175), 
                            (35, 190), (50, 210), (75, 250), (110, 290)]
    ax.clabel(cont, inline=True, fontsize=10,
              manual=manualLabelPositions)
    # cbar = fig.colorbar(im, ax=ax)
    # cbar = fig.colorbar(cont, ax=ax)

    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # contf = plt.contourf(xi, yi, zi, extent=[x.min(), x.max(), y.min(), y.max()])
    twoDPlot.plotAuxTitleAndBounds2D(r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$ at 14 TeV',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$',
                                     xlims=(1, 124), ylims=(126, 500), fig=fig, ax=ax, im=im)


    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '14TeV', 'BP2',
                '14TeV_BP2_XS_XSH_bbgamgam_1.pdf'))
    plt.close()

    del x, y, z, xi, yi


    # BP2 14 TeV gg -> H3 -> H1(gamgam) H2(bb)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP2_14['mH1'],
                                            ScannerS_BP2_14['mH3'],
                                            ScannerS_BP2_14['x_H3_H1_gamgam_H2_bb'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # # contf = plt.contourf(xi, yi, zi, extent=[x.min(), x.max(), y.min(), y.max()])
    # twoDPlot.plotAuxTitleAndBounds2D(r'$\left.\sigma(gg\to h_{3} \to h_{1}(\gamma\gaa) h_{2}(b\bar{b}))$ a\rightt 14 TeV',
    #                                  r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
    #                                  r'$\left.\sigma(gg\to h_{3} \to h_{1}(\gamma\gaa) h_{2}(b\bar{b}))$',\right
    #                                  xlims=(1, 124), ylims=(126, 500))
    fig, ax = plt.subplots()
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    cont = ax.contour(xi, yi, zi, origin='lower', linewidths=0.75, colors='k')
    manualLabelsPositions = [(40, 250), (50, 250), (65, 250), (75, 250),
                             (85, 250), (95, 250), (105, 250)]
    ax.clabel(cont, inline=True, fontsize=10,
              manual=manualLabelsPositions)

    twoDPlot.plotAuxTitleAndBounds2D(r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$ at 14 TeV',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$',
                                     xlims=(1, 124), ylims=(126, 500), fig=fig, ax=ax, im=im)

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '14TeV', 'BP2',
                '14TeV_BP2_XS_XSH_bbgamgam_2.pdf'))
    plt.close()

    del x, y, z, xi, yi


    ## BP3

    # normSM set to the HH cross section at 14 TeV according to
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH
    # and the bb gamgam branching ratio
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR?sortcol=0;table=1;up=0#sorted_table
    ScannerS_BP3_14 = TRSM.observables(path13_BP3,
                                       'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                       normSM=36.69 * 10**(-3) * 0.002637,
                                       kineticExclude=True,
                                       pathRun3Data=path14,
                                       keyMassRun3='mass',
                                       keyCrossSecRun3='SMCrossSec')
                                         # normSM=1

    # BP3 14 TeV gg -> H3 -> H1(bb) H2(gamgam)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP3_14['mH2'],
                                            ScannerS_BP3_14['mH3'],
                                            ScannerS_BP3_14['x_H3_H1_bb_H2_gamgam'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # # contf = plt.contourf(xi, yi, zi, extent=[x.min(), x.max(), y.min(), y.max()])
    # twoDPlot.plotAuxTitleAndBounds2D(r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$ at 14 TeV',
    #                                  r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
    #                                  r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$',
                                     # xlims=(126, 500), ylims=(255, 650), fig=fig, ax=ax, im=im)

    fig, ax = plt.subplots()
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    cont = ax.contour(xi, yi, zi, origin='lower', linewidths=0.75, colors='k')
    ax.clabel(cont, inline=True, fontsize=10)

    twoDPlot.plotAuxTitleAndBounds2D(r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$ at 14 TeV',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$',
                                     xlims=(126, 500), ylims=(255, 650), fig=fig, ax=ax, im=im)


    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '14TeV', 'BP3',
                '14TeV_BP3_XS_XSH_bbgamgam_1.pdf'))
    plt.close()

    del x, y, z, xi, yi


    ## BP3 14 TeV gg -> H3 -> H1(gamgam) H2(bb)
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP3_14['mH2'],
                                            ScannerS_BP3_14['mH3'],
                                            ScannerS_BP3_14['x_H3_H1_gamgam_H2_bb'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # # contf = plt.contourf(xi, yi, zi, extent=[x.min(), x.max(), y.min(), y.max()])
    # twoDPlot.plotAuxTitleAndBounds2D(r'$\left.\sigma(gg\to h_{3} \to h_{1}(\gamma\gaa) h_{2}(b\bar{b}))$ a\rightt 14 TeV',
    #                                  r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
    #                                  r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$',
                                     # xlims=(126, 500), ylims=(255, 650), fig=fig, ax=ax, im=im)

    fig, ax = plt.subplots()
    im = ax.imshow(zi, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    cont = ax.contour(xi, yi, zi, origin='lower', linewidths=0.75, colors='k')
    ax.clabel(cont, inline=True, fontsize=10)

    twoDPlot.plotAuxTitleAndBounds2D(r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$ at 14 TeV',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'$\left.\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma)) \right/ \sigma(SM)$',
                                     xlims=(126, 500), ylims=(255, 650), fig=fig, ax=ax, im=im)


    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '14TeV', 'BP3',
                '14TeV_BP3_XS_XSH_bbgamgam_2.pdf'))
    plt.close()

    del x, y, z, xi, yi

    # everything below this comment can be ignored (some sanity checks)
    print('Running some sanity checks, this can be ignored...')

    ScannerS_BP2_14 = TRSM.observables(path13_BP2,
                                         'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                         normSM=1,
                                         kineticExclude=False,
                                         pathRun3Data=path14,
                                         keyMassRun3='mass',
                                         keyCrossSecRun3='SMCrossSec')

    ScannerS_BP3_14 = TRSM.observables(path13_BP3,
                                         'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                         normSM=1,
                                         kineticExclude=False,
                                         pathRun3Data=path14,
                                         keyMassRun3='mass',
                                         keyCrossSecRun3='SMCrossSec')


    ScannerS_BP2_H1H2_14, ScannerS_BP2_H1H1_14, ScannerS_BP2_H2H2_14 = TRSM.ppXNPSM_massfree(path13_BP2,
                                                                                       'mH1', 'mH2', 'mH3', 'bb', 'gamgam',
                                                                                       normalizationSM=1, run3=True,
                                                                                       pathRun3Data=path14,
                                                                                       keyMassRun3='mass',
                                                                                       keyCrossSecRun3='SMCrossSec')

    ScannerS_BP3_H1H2_14, ScannerS_BP3_H1H1_14, ScannerS_BP3_H2H2_14 = TRSM.ppXNPSM_massfree(path13_BP3,
                                                                                       'mH1', 'mH2', 'mH3', 'bb', 'gamgam',
                                                                                       normalizationSM=1, run3=True,
                                                                                       pathRun3Data=path14,
                                                                                       keyMassRun3='mass',
                                                                                       keyCrossSecRun3='SMCrossSec')

    TRSM.comparer(ScannerS_BP2_14, ScannerS_BP2_H1H2_14)
    TRSM.comparer(ScannerS_BP3_14, ScannerS_BP3_H1H2_14)

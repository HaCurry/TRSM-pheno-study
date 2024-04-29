import os
import json
import scipy.interpolate as interp

import numpy as np
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import mplhep as hep

if __name__ == '__main__':

    # !! OBS: '13 TeV ScannerS' implies the SM ggF Higgs cross section, not !!
    # !! TRSM. Figures which were NOT included in the thesis might labeled  !!
    # !! or titled wrong, to be sure what the figures (which are NOT        !!
    # !! included in the thesis) are plotting check the variable names!     !!

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to plotting directory
    # E:
    pathPlots = '/eos/user/i/ihaque/SusHiPlots'

    # create plotting directory if it already does not exist
    os.makedirs(pathPlots, exist_ok=True)
    os.makedirs(os.path.join(pathPlots, 'plots1D'), exist_ok=True)
    # os.makedirs(os.path.join(pathPlots, '13TeV'), exist_ok=True)
    # os.makedirs(os.path.join(pathPlots, '13TeV/compareScannerSandSusHi'), exist_ok=True)
    # os.makedirs(os.path.join(pathPlots, '13_6TeV'), exist_ok=True)

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


    ## read in cross sections

    # If not specified it is NNLO otherwise N3LO

    dfScannerS_13 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                      'SusHi_HiggsCrossSections',
                                      '13TeV_ScannerSCrossSections.tsv'))

    dfSusHi_13 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                   'SusHi_HiggsCrossSections',
                                   '13TeV_SusHiCrossSections.tsv'))

    dfSusHi_N3LO_13 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                        'SusHi_HiggsCrossSections',
                                        '13TeV_N3LO_SusHiCrossSections.tsv'))

    dfSusHi_13_6 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                     'SusHi_HiggsCrossSections',
                                     '13_6TeV_SusHiCrossSections.tsv'))

    dfSusHiImpr_13_6 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                         'SusHi_HiggsCrossSections',
                                         '13_6TeV_SusHiImprCrossSections.tsv'))

    dfYR4_14 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                 'SusHi_HiggsCrossSections',
                                 '14TeV_YR4CrossSections.tsv'))

    # quick sanity check that the length of the dataframe
    # and the number of mass points are equal
    if (len(dfScannerS_13) == len(dfSusHi_13) and
        len(dfScannerS_13) == len(dfSusHi_N3LO_13) and
        len(dfScannerS_13['mass']) == len(dfSusHi_13['mass']) and
        len(dfScannerS_13['mass']) == len(dfSusHi_N3LO_13['mass']) and
        len(dfScannerS_13['SMCrossSec']) == len(dfSusHi_13['SMCrossSec']) and
        len(dfScannerS_13['SMCrossSec']) == len(dfSusHi_13_6['SMCrossSec']) and
        len(dfScannerS_13['SMCrossSec']) == len(dfSusHi_N3LO_13['SMCrossSec'])):
        pass

    else:
        raise Exception('Cross sections are not of equal length') 

    # XSScannerS = np.array(dfScannerS['SMCrossSec'])
    # XSSusHi = np.array(dfSusHi['crossSec'])
    # XSSusHi_N3LO = np.array(dfSusHi_N3LO['crossSec'])

    ratio = np.array(dfSusHi_13['SMCrossSec'])/np.array(dfScannerS_13['SMCrossSec'])
    mass = np.array(dfScannerS_13['mass'])
    print(f'NNLO:') 
    [print(f'mass: {mass[i]} ratio: {ratio[i]}') for i in range(len(mass))]

    ratio_N3LO = np.array(dfSusHi_N3LO_13['SMCrossSec'])/np.array(dfScannerS_13['SMCrossSec'])
    print(f'N3LO:') 
    [print(f'mass: {mass[i]} ratio: {ratio_N3LO[i]}') for i in range(len(mass))]

    ## 13 TeV SusHi and 13 TeV ScannerS cross sections (ratio)

    # 0 - 100 GeV

    fig, axRatioMinusOne = plt.subplots()

    axRatioMinusOne.plot(mass, [abs(i - 1) for i in ratio])
    axRatioMinusOne.axhline(0.05, color='grey', linestyle='dashed')

    axRatioMinusOne.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    axRatioMinusOne.set_ylabel(r'$\left|\frac{\sigma^{SusHi}(gg\to h_{SM})}{\sigma^{ScannerS}(gg\to h_{SM})}-1\right|$')
    axRatioMinusOne.set_ylim(0, 0.20)
    axRatioMinusOne.set_xlim(0, 100)

    axRatioMinusOne.legend(title='ggF @ $13$ TeV\nSusHi: NNLO\nScannerS: NNLO + NNLL')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13TeV_ScannerSSusHiCrossSectionsRatio_1.pdf'))
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13TeV_ScannerSSusHiCrossSectionsRatio_1.png'))
    plt.close()

    # 100 - 1000 GeV

    fig, axRatioMinusOne = plt.subplots()

    axRatioMinusOne.plot(mass, [abs(i - 1) for i in ratio])
    axRatioMinusOne.axhline(0.05, color='grey', linestyle='dashed')

    axRatioMinusOne.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    axRatioMinusOne.set_ylabel(r'$\left|\frac{\sigma^{SusHi}(gg\to h_{SM})}{\sigma^{ScannerS}(gg\to h_{SM})}-1\right|$')
    axRatioMinusOne.set_ylim(0, 0.20)
    axRatioMinusOne.set_xlim(100, 1000)

    axRatioMinusOne.legend(title='ggF @ $13$ TeV\nSusHi: NNLO\nScannerS: NNLO + NNLL')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13TeV_ScannerSSusHiCrossSectionsRatio_2.pdf'))
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13TeV_ScannerSSusHiCrossSectionsRatio_2.png'))
    plt.close()


    ## 13 TeV SusHi at N3LO and 13 TeV ScannerS cross sections (ratio)

    fig, (axRatio_N3LO, axRatioMinusOne_N3LO) = plt.subplots(1, 2)
    fig.supxlabel(r'$M _{h_{{SM}}}$ [GeV]')

    axRatio_N3LO.plot(mass, ratio_N3LO)
    axRatio_N3LO.set_title(r'$\frac{\sigma^{SusHi~N3LO}_{13~TeV}}{\sigma^{ScannerS~NNLO+NNLL}_{13TeV}}$')
    axRatio_N3LO.axvline(100, color='grey', linestyle='dashed')
    axRatio_N3LO.axvline(300, color='grey', linestyle='dashed')
    # axRatio_N3LO.set_xlim(100,300)
    # axRatio_N3LO.set_ylim(0.98, 1.20)

    axRatioMinusOne_N3LO.plot(mass, [abs(i - 1) for i in ratio_N3LO])
    axRatioMinusOne.axhline(0.05, color='grey', linestyle='dashed')
    axRatioMinusOne_N3LO.set_title(r'$\left|\frac{\sigma^{SusHi~N3LO}_{13~TeV}}{\sigma^{ScannerS~NNLO+NNLL}_{13TeV}}-1\right|$')
    axRatioMinusOne_N3LO.set_xlim(100,300)
    axRatioMinusOne_N3LO.set_ylim(0, 0.20)

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13TeV_N3LO_ScannerSSusHiCrossSectionsRatio.pdf'))
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13TeV_N3LO_ScannerSSusHiCrossSectionsRatio.png'))
    plt.close()


    ## 13 TeV SusHi and 13 TeV ScannerS cross sections (side-by-side)

    plt.plot(mass, np.array(dfScannerS_13['SMCrossSec']), label='ScannerS')
    plt.plot(mass, np.array(dfSusHi_13['SMCrossSec']), label='SusHi')
    plt.legend(loc='upper right')
    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma(gg\to h_{SM})$ [pb]' )
    plt.title(r'SusHi and ScannerS cross sections at 13 TeV')
    plt.yscale('log')
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13TeV_ScannerSSusHiCrossSections.pdf'))
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13TeV_ScannerSSusHiCrossSections.png'))
    plt.close()


    ## 13 TeV SusHi, 13 TeV ScannerS and 13.6 TeV SusHi cross sections (side-by-side)

    plt.plot(mass, np.array(dfScannerS_13['SMCrossSec']), label='ScannerS 13 TeV')
    plt.plot(mass, np.array(dfSusHi_13['SMCrossSec']), label='SusHi 13 TeV')
    plt.plot(mass, np.array(dfSusHi_13_6['SMCrossSec']), label='SusHi 13.6 TeV')
    plt.legend(loc='upper right')
    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma(gg\to h_{SM})$ [pb]' )
    plt.title(r'SusHi cross sections at  13 TeV and 13.6')
    plt.yscale('log')
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_13TeV_SusHiCrossSections.pdf'))
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_13TeV_SusHiCrossSections.png'))
    plt.close()


    ## 14 TeV YR4 and 13 TeV ScannerS cross sections (ratio) and
    ## 13.6 TeV SusHi and 13 TeV SusHi cross sections (ratio)

    ratio13_6TeV_13TeV = np.array(dfSusHi_13_6['SMCrossSec'])/np.array(dfSusHi_13['SMCrossSec'])
    YR4interp = interp.CubicSpline(np.array(dfYR4_14['mass']), np.array(dfYR4_14['SMCrossSec']))
    ratio14TeV_13TeV = YR4interp(dfScannerS_13['mass'])/np.array(dfScannerS_13['SMCrossSec'])

    plt.plot(mass, ratio13_6TeV_13TeV,
             label='$\sigma^{13.6~TeV}_{SusHi}/\sigma^{13~TeV}_{SusHi}$')
    plt.plot(mass, ratio14TeV_13TeV, 
             label='$\sigma^{14~TeV}_{LHCHWG}/\sigma^{13~TeV}_{LHCHWG~(ScannerS)}$',
             color='grey', linestyle='dashed')
    #[plt.annotate(f'{y:.3f}', (x, y), rotation=45) for (x, y) in list(zip(mass[::55],ratio13_6[::55])) ]

    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'Ratio')

    plt.legend(title='Ratios of SM ggF Higgs cross sections', alignment='left')

    plt.xlim(0,1000)
    plt.ylim(10**(0), 1.4 * 10**(0))
    plt.yscale('log')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_13TeV_SusHiCrossSectionsRatio.pdf'))
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_13TeV_SusHiCrossSectionsRatio.png'))
    plt.close()


    ## 13.6 TeV SusHi improved cross sections

    fig, axes = plt.subplots(1, 2)
    fig.suptitle('13.6 TeV ScannerS')
    fig.supylabel(r'$\sigma$ [pb]')
    fig.supxlabel(r'$M_{h_{SM}}$ [GeV]')

    # 0 - 500 GeV

    axes[0].plot(np.array(dfSusHiImpr_13_6['mass']), np.array(dfSusHiImpr_13_6['SMCrossSec']))
    axes[0].set_xlim(0, 500)
    axes[0].set_ylim(10**(0), 10**(4))
    axes[0].set_yscale('log')

    # 500 - 1000 GeV

    axes[1].plot(np.array(dfSusHiImpr_13_6['mass']), np.array(dfSusHiImpr_13_6['SMCrossSec']))
    axes[1].set_xlim(500, 1000)
    axes[1].set_ylim(10**(0), 10**(1))
    axes[1].set_yscale('log')

    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_SusHiImprCrossSections.pdf'))
    plt.close()


    ## 13.6 TeV SusHi, 13 TeV ScannerS and 14 TeV YR4 cross sections

    fig, ax = plt.subplots()

    # 0 - 100 GeV

    ax.plot(np.array(dfScannerS_13['mass']), np.array(dfScannerS_13['SMCrossSec']),
            color='C0', linewidth=0.5)
    ax.plot(np.array(dfSusHi_13_6['mass']), np.array(dfSusHi_13_6['SMCrossSec']),
            color='C1', linewidth=0.5)
    ax.plot(np.array(dfYR4_14['mass']), np.array(dfYR4_14['SMCrossSec']),
            color='C2', linewidth=0.5)

    ax.set_xlim(0, 100)
    ax.set_ylim(5 * 10**(1), 10**(4))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_13TeV_14TeV_ScannerSSusHiYR4CrossSections_1.pdf'))
    plt.close()

    # 100 - 500 GeV

    fig, ax = plt.subplots()

    ax.plot(np.array(dfScannerS_13['mass']), np.array(dfScannerS_13['SMCrossSec']),
            color='C0', linewidth=0.5)
    ax.plot(np.array(dfSusHi_13_6['mass']), np.array(dfSusHi_13_6['SMCrossSec']),
            color='C1', linewidth=0.5)
    ax.plot(np.array(dfYR4_14['mass']), np.array(dfYR4_14['SMCrossSec']),
            color='C2', linewidth=0.5)
    ax.set_xlim(100, 500)
    ax.set_ylim(4 * 10**(0), 7 * 10**(1))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_13TeV_14TeV_ScannerSSusHiYR4CrossSections_2.pdf'))
    plt.close()

    # 500 - 1000 GeV

    fig, ax = plt.subplots()

    ax.plot(np.array(dfScannerS_13['mass']), np.array(dfScannerS_13['SMCrossSec']),
            color='C0', linewidth=0.5)
    ax.plot(np.array(dfSusHi_13_6['mass']), np.array(dfSusHi_13_6['SMCrossSec']),
            color='C1', linewidth=0.5)
    ax.plot(np.array(dfYR4_14['mass']), np.array(dfYR4_14['SMCrossSec']),
            color='C2', linewidth=0.5)
    ax.set_xlim(500, 1000)
    ax.set_ylim(10**(-1), 6 * 10**(0))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_13TeV_14TeV_ScannerSSusHiYR4CrossSections_3.pdf'))
    plt.close()


    ## 13.6 TeV SusHi improved, 13 TeV ScannerS and 14 TeV YR4

    fig, ax = plt.subplots()

    # 0 - 100 GeV

    ax.plot(np.array(dfScannerS_13['mass']), np.array(dfScannerS_13['SMCrossSec']),
            color='C0', linewidth=0.5)
    ax.plot(np.array(dfSusHiImpr_13_6['mass']), np.array(dfSusHiImpr_13_6['SMCrossSec']),
            color='C1', linewidth=0.5)
    ax.plot(np.array(dfYR4_14['mass']), np.array(dfYR4_14['SMCrossSec']),
            color='C2', linewidth=0.5)
    ax.set_xlim(0, 100)
    ax.set_ylim(5 * 10**(1), 10**(4))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1 (improved)'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_13TeV_14TeV_ScannerSSusHiImprYR4CrossSections_1.pdf'))
    plt.close()

    fig, ax = plt.subplots()

    # 100 - 500 GeV

    ax.plot(np.array(dfScannerS_13['mass']), np.array(dfScannerS_13['SMCrossSec']),
            color='C0', linewidth=0.5)
    ax.plot(np.array(dfSusHiImpr_13_6['mass']), np.array(dfSusHiImpr_13_6['SMCrossSec']),
            color='C1', linewidth=0.5)
    ax.plot(np.array(dfYR4_14['mass']), np.array(dfYR4_14['SMCrossSec']),
            color='C2', linewidth=0.5)
    ax.set_xlim(100, 500)
    ax.set_ylim(4 * 10**(0), 7 * 10**(1))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1 (improved)'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_13TeV_14TeV_ScannerSSusHiImprYR4CrossSections_2.pdf'))
    plt.close()

    fig, ax = plt.subplots()

    # 500 - 1000 GeV

    ax.plot(np.array(dfScannerS_13['mass']), np.array(dfScannerS_13['SMCrossSec']),
            color='C0', linewidth=0.5)
    ax.plot(np.array(dfSusHiImpr_13_6['mass']), np.array(dfSusHiImpr_13_6['SMCrossSec']),
            color='C1', linewidth=0.5)
    ax.plot(np.array(dfYR4_14['mass']), np.array(dfYR4_14['SMCrossSec']),
            color='C2', linewidth=0.5)
    ax.set_xlim(500, 1000)
    ax.set_ylim(10**(-1), 6 * 10**(0))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1 (improved)'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'plots1D',
                '13_6TeV_13TeV_14TeV_ScannerSSusHiImprYR4CrossSections_3.pdf'))
    plt.close()


    # print the cross section for comparison
    SM14TeV = interp.CubicSpline(dfYR4_14['mass'], dfYR4_14['SMCrossSec'])
    print('mass, 13 TeV ScannerS, 13.6 TeV ScannerS, 14 TeV YR4 cross sections')
    [print(dfScannerS_13['mass'][i], dfScannerS_13['SMCrossSec'][i],
           dfSusHiImpr_13_6['SMCrossSec'][i], SM14TeV(dfScannerS_13['mass'][i]))
     for i in range(len(dfScannerS_13))]

    # print the ratios of the cross sections for comparison
    print('mass, (13.6 TeV ScannerS)/(13 TeV ScannerS),\
(14 TeV YR4)/(13.6 TeV ScannerS) ratios of cross sections')
    [print(dfScannerS_13['mass'][i], dfSusHiImpr_13_6['SMCrossSec'][i]/dfScannerS_13['SMCrossSec'][i],
           SM14TeV(dfScannerS_13['mass'][i])/dfSusHiImpr_13_6['SMCrossSec'][i])
     for i in range(len(dfScannerS_13))]

import configurer as config
import functions as TRSM

import os
from scipy.interpolate import CubicSpline

import numpy as np
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep

if __name__ == '__main__':

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to plotting directory
    # E:
    pathPlots = '/eos/user/i/ihaque/SusHiPlots'

    # create plotting directory if it already does not exist
    os.makedirs(pathPlots, exist_ok=True)
    os.makedirs(os.path.join(pathPlots, '13TeV'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, '13TeV/compareScannerSandSusHi'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, '13_6TeV'), exist_ok=True)
    
    # plot style
    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19

    ### 13 TeV cross sections 

    ## If not specified it is NNLO otherwise N3LO

    dfScannerS = pandas.read_table(os.path.join(pathRepo, 
                                                'testing/SusHi_HiggsCrossSections/13TeV_ScannerSCrossSections.tsv'))
    dfSusHi = pandas.read_table(os.path.join(pathRepo, 
                                             'testing/SusHi_HiggsCrossSections/13TeV_SusHiCrossSections.tsv'))
    dfSusHi_N3LO = pandas.read_table(os.path.join(pathRepo, 
                                                  'testing/SusHi_HiggsCrossSections/13TeV_N3LO_SusHiCrossSections.tsv'))

    # quick sanity check that the length of the dataframe
    # and the number of mass points are equal
    if (len(dfScannerS) == len(dfSusHi) and
        len(dfScannerS) == len(dfSusHi_N3LO) and
        len(dfScannerS['mass']) == len(dfSusHi['mass']) and
        len(dfScannerS['mass']) == len(dfSusHi_N3LO['mass']) and
        len(dfScannerS['SMCrossSec']) == len(dfSusHi['crossSec']) and
        len(dfScannerS['SMCrossSec']) == len(dfSusHi_N3LO['crossSec'])):
        pass

    else:
        raise Exception('Cross sections are not of equal length') 

    mass = np.array(dfScannerS['mass'])
    XSScannerS = np.array(dfScannerS['SMCrossSec'])
    XSSusHi = np.array(dfSusHi['crossSec'])
    XSSusHi_N3LO = np.array(dfSusHi_N3LO['crossSec'])

    ratio = XSSusHi/XSScannerS 
    print(f'NNLO:') 
    [print(f'mass: {mass[i]} ratio: {ratio[i]}') for i in range(len(mass))]
    # print(ratio)

    ratio_N3LO = XSSusHi_N3LO/XSScannerS 
    print(f'N3LO:') 
    [print(f'mass: {mass[i]} ratio: {ratio_N3LO[i]}') for i in range(len(mass))]

    ## 13 TeV SusHi and ScannerS cross sections (ratio)

    # fig, (axRatio, axRatioMinusOne) = plt.subplots(1, 2)
    fig, axRatioMinusOne = plt.subplots()

    # axRatio.plot(mass, ratio)
    # axRatio.set_title(r'$\frac{\sigma^{SusHi~NNLO}}{\sigma^{ScannerS~NNLO+NNLL}}$')
    # axRatio.set_yscale('log')
    # axRatio.set_ylim(0.9, 1.20)

    axRatioMinusOne.plot(mass, [abs(i - 1) for i in ratio])
    axRatioMinusOne.axhline(0.05, color='grey', linestyle='dashed')

    axRatioMinusOne.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    axRatioMinusOne.set_ylabel(r'$\left|\frac{\sigma^{SusHi}(gg\to h_{SM})}{\sigma^{ScannerS}(gg\to h_{SM})}-1\right|$')
    axRatioMinusOne.set_ylim(0, 0.20)
    axRatioMinusOne.set_xlim(0, 100)

    axRatioMinusOne.legend(title='ggF @ $13$ TeV\nSusHi: NNLO\nScannerS: NNLO + NNLL')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 
                '13TeV/compareScannerSandSusHi/13TeV_ScannerSSusHiCrossSectionsRatio_1.pdf'))
    plt.savefig(os.path.join(pathPlots, 
                '13TeV/compareScannerSandSusHi/13TeV_ScannerSSusHiCrossSectionsRatio_1.png'))
    plt.close()

    fig, axRatioMinusOne = plt.subplots()

    axRatioMinusOne.plot(mass, [abs(i - 1) for i in ratio])
    axRatioMinusOne.axhline(0.05, color='grey', linestyle='dashed')

    axRatioMinusOne.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    axRatioMinusOne.set_ylabel(r'$\left|\frac{\sigma^{SusHi}(gg\to h_{SM})}{\sigma^{ScannerS}(gg\to h_{SM})}-1\right|$')
    axRatioMinusOne.set_ylim(0, 0.20)
    axRatioMinusOne.set_xlim(100, 1000)

    axRatioMinusOne.legend(title='ggF @ $13$ TeV\nSusHi: NNLO\nScannerS: NNLO + NNLL')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 
                '13TeV/compareScannerSandSusHi/13TeV_ScannerSSusHiCrossSectionsRatio_2.pdf'))
    plt.savefig(os.path.join(pathPlots, 
                '13TeV/compareScannerSandSusHi/13TeV_ScannerSSusHiCrossSectionsRatio_2.png'))
    plt.close()

    ## 13 TeV SusHi at N3LO and ScannerS cross sections (ratio)

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
    plt.savefig(os.path.join(pathPlots,
                '13TeV/compareScannerSandSusHi/13TeV_N3LO_ScannerSSusHiCrossSectionsRatio.pdf'))
    plt.savefig(os.path.join(pathPlots,
                '13TeV/compareScannerSandSusHi/13TeV_N3LO_ScannerSSusHiCrossSectionsRatio.png'))
    plt.close()
    
    ## 13 TeV SusHi and ScannerS cross sections (side-by-side)

    plt.plot(mass, XSScannerS, label='ScannerS')
    plt.plot(mass, XSSusHi, label='SusHi')
    plt.legend(loc='upper right')
    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma(gg\to h_{SM})$ [pb]' )
    plt.title(r'SusHi and ScannerS cross sections at 13 TeV')
    plt.yscale('log')
    plt.savefig(os.path.join(pathPlots,
                '13TeV/compareScannerSandSusHi/13TeV_ScannerSSusHiCrossSections.pdf'))
    plt.savefig(os.path.join(pathPlots,
                '13TeV/compareScannerSandSusHi/13TeV_ScannerSSusHiCrossSections.png'))
    plt.close()

    ### 13.6 TeV SusHi cross sections 

    dfSusHi13_6 = pandas.read_table(os.path.join(pathRepo,
                                    'testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections.tsv'))

    mass = np.array(dfSusHi13_6['mass'])
    XSSusHi13_6 = np.array(dfSusHi13_6['crossSec'])

    ## 13 TeV and 13.6 TeV SusHi cross sections (side-by-side)

    plt.plot(mass, XSScannerS, label='ScannerS 13 TeV')
    plt.plot(mass, XSSusHi, label='SusHi 13 TeV')
    plt.plot(mass, XSSusHi13_6, label='SusHi 13.6 TeV')
    plt.legend(loc='upper right')
    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma(gg\to h_{SM})$ [pb]' )
    plt.title(r'SusHi cross sections at  13 TeV and 13.6')
    plt.yscale('log')
    plt.savefig(os.path.join(pathPlots, '13_6TeV/13_6TeV_13TeV_SusHiCrossSections.pdf'))
    plt.savefig(os.path.join(pathPlots, '13_6TeV/13_6TeV_13TeV_SusHiCrossSections.png'))
    plt.close()

    ## 13 TeV and 13.6 TeV SusHi cross sections (ratio)
    
    df14 = pandas.read_table(os.path.join(pathRepo, 'testing/SusHi_HiggsCrossSections/14TeV_YR4CrossSections.tsv'))

    ratio13_6TeV_13TeV = XSSusHi13_6/XSSusHi
    import scipy.interpolate as interp 
    YR4 = CubicSpline(np.array(df14['mass']),np.array(df14['SMCrossSec']))
    ratio14TeV_13TeV = YR4(dfScannerS['mass'])/XSScannerS

    plt.plot(mass, ratio13_6TeV_13TeV, label='$\sigma^{13.6~TeV}_{SusHi}/\sigma^{13~TeV}_{SusHi}$')
    plt.plot(mass, ratio14TeV_13TeV, label='$\sigma^{14~TeV}_{LHCHWG}/\sigma^{13~TeV}_{LHCHWG~(ScannerS)}$', marker='.')
    dfTest = pandas.read_table('test.tsv')
    plt.plot(np.array(dfTest['mass']), np.array(dfTest['SMCrossSec']), color='grey')
    #[plt.annotate(f'{y:.3f}', (x, y), rotation=45) for (x, y) in list(zip(mass[::55],ratio13_6[::55])) ]

    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma^{X~TeV}/\sigma^{Y~TeV}$')

    plt.legend(title='ratios of SM ggF Higgs cross sections', alignment='left')
    
    plt.xlim(0,1000)
    plt.ylim(10**(0), 1.3* 10**(0))
    plt.yscale('log')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '13_6TeV/13_6TeV_13TeV_SusHiCrossSectionsRatio.pdf'))
    plt.savefig(os.path.join(pathPlots, '13_6TeV/13_6TeV_13TeV_SusHiCrossSectionsRatio.png'))
    plt.close()


import configurer as config
import functions as TRSM

import os

import numpy as np
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep

if __name__ == '__main__':
    
    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19

    ### 13 TeV cross sections ###

    dfScannerS = pandas.read_table('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/13TeV_ScannerSCrossSections.tsv')
    dfSusHi = pandas.read_table('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/13TeV_SusHiCrossSections.tsv')

    if (len(dfScannerS) == len(dfSusHi) and len(dfScannerS['mass']) == len(dfSusHi['mass']) and 
len(dfScannerS['SMCrossSec']) == len(dfSusHi['crossSec'])):
        pass

    else:
        raise Exception('Cross sections are not of equal length') 

    mass = np.array(dfScannerS['mass'])
    XSScannerS = np.array(dfScannerS['SMCrossSec'])
    XSSusHi = np.array(dfSusHi['crossSec'])

    ratio = XSSusHi/XSScannerS  
    [print(f'mass: {mass[i]} ratio: {ratio[i]}') for i in range(len(mass))]
    # print(ratio)
    

    ## 13 TeV SusHi and ScannerS cross sections (ratio) ##

    plt.plot(mass, ratio)
    plt.xlabel(r'$M _{h_{{SM}}}$ [GeV]')
    plt.ylabel(r'$\sigma^{{SusHi}}/\sigma^{{ScannerS}}$')
    plt.title(r'Ratio of SusHi and ScannerS cross sections at 13 TeV')
    plt.yscale('log')
    plt.ylim(0.9, 1.20)
    plt.tight_layout()

    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_ScannerSSusHiCrossSectionsRatio.pdf')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_ScannerSSusHiCrossSectionsRatio.png')
    plt.close()

    ## 13 TeV SusHi and ScannerS cross sections (side-by-side) ##

    plt.plot(mass, XSScannerS, label='ScannerS')
    plt.plot(mass, XSSusHi, label='SusHi')
    plt.legend(loc='upper right')
    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma(gg\to h_{SM})$ [pb]' )
    plt.title(r'SusHi and ScannerS cross sections at 13 TeV')
    plt.yscale('log')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_ScannerSSusHiCrossSections.pdf')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_ScannerSSusHiCrossSections.png')
    plt.close()

    ### 13.6 TeV SusHi cross sections ###

    dfSusHi13_6 = pandas.read_table('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections.tsv')

    mass = np.array(dfSusHi13_6['mass'])
    XSSusHi13_6 = np.array(dfSusHi13_6['crossSec'])
   
    ## 13 TeV and 13.6 TeV SusHi cross sections (side-by-side) ##    
 
    plt.plot(mass, XSScannerS, label='ScannerS 13 TeV')
    plt.plot(mass, XSSusHi, label='SusHi 13 TeV')
    plt.plot(mass, XSSusHi13_6, label='SusHi 13.6 TeV')
    plt.legend(loc='upper right')
    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma(gg\to h_{SM})$ [pb]' )
    plt.title(r'SusHi cross sections at  13 TeV and 13.6')
    plt.yscale('log')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13_6TeV/13_6TeV_SusHiCrossSections.pdf')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13_6TeV/13_6TeV_SusHiCrossSections.png')
    plt.close()

    ## 13 TeV and 13.6 TeV SusHi cross sections (ratio) ##

    ratio13_6 = XSSusHi13_6/XSSusHi

    plt.plot(mass, ratio13_6)
    [plt.annotate(f'{y:.3f}', (x, y), rotation=45) for (x, y) in list(zip(mass[::55],ratio13_6[::55])) ]

    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma^{{SusHi}}_{\mathrm{13.6~TeV}}/\sigma^{SusHi}_{\mathrm{13~TeV}}$')
    plt.title(r'ratio of 13.6 TeV and 13 TeV SusHi cross sections')
    plt.yscale('log')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13_6TeV/13_6TeV_13TeV_SusHiCrossSectionsRatio.pdf')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13_6TeV/13_6TeV_13TeV_SusHiCrossSectionsRatio.png')
    plt.close()

    # from scipy.interpolate import CubicSpline
    # keyMassRun3 = 'mass'
    # keyCrossSecRun3 = 'crossSec'
    # df = pandas.read_table('TRSMOutputsTemp/temp_output.tsv')
    # mH3_H1H2 = df['mH3']
    # run3_x_HSM_gg = CubicSpline(np.array(dfSusHi[keyMassRun3]), np.array(dfSusHi[keyCrossSecRun3]))
    # x_H3_gg_H1H2 = [(df['R31'][i]**2) * run3_x_HSM_gg(mH3_H1H2[i]) for i in range(len(mH3_H1H2))]

    # plt.plot(mass, XSScannerS)
    # # plt.plot(mass, XSSusHi)
    # plt.plot(mass, run3_x_HSM_gg(mass))
    # plt.yscale('log')
    # plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_Temp2.pdf')
    # plt.close()
   

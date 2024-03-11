import configurer as config
import functions as TRSM

import os

import numpy as np
import pandas
import matplotlib
import matplotlib.pyplot as plt

if __name__ == '__main__':
    dfScannerS = pandas.read_table('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/ScannerSCrossSections.tsv')
    dfSusHi = pandas.read_table('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/13TeV_SusHiCrossSections2.tsv')

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

    plt.plot(mass, ratio)
    plt.yscale('log')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_ScannerSSusHiCrossSectionsRatio2.pdf')
    plt.close()

    plt.plot(mass, XSScannerS)
    plt.plot(mass, XSSusHi)
    plt.yscale('log')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_ScannerSSusHiCrossSections2.pdf')
    plt.close()

    from scipy.interpolate import CubicSpline
    keyMassRun3 = 'mass'
    keyCrossSecRun3 = 'crossSec'
    df = pandas.read_table('TRSMOutputsTemp/temp_output.tsv')
    mH3_H1H2 = df['mH3']
    run3_x_HSM_gg = CubicSpline(np.array(dfSusHi[keyMassRun3]), np.array(dfSusHi[keyCrossSecRun3]))
    x_H3_gg_H1H2 = [(df['R31'][i]**2) * run3_x_HSM_gg(mH3_H1H2[i]) for i in range(len(mH3_H1H2))]

    plt.plot(mass, XSScannerS)
    # plt.plot(mass, XSSusHi)
    plt.plot(mass, run3_x_HSM_gg(mass))
    plt.yscale('log')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_Temp2.pdf')
    plt.close()
   

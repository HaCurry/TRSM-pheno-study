import configurer as config
import functions as TRSM

import os

import numpy as np
import pandas
import matplotlib
import matplotlib.pyplot as plt

if __name__ == '__main__':
    dfScannerS = pandas.read_table('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/ScannerSCrossSections.tsv')
    dfSusHi = pandas.read_table('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/SusHiCrossSections.tsv')

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
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_ScannerSSusHiCrossSectionsRatio.pdf')
    plt.close()

    plt.plot(mass, XSScannerS)
    plt.plot(mass, XSSusHi)
    plt.yscale('log')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_ScannerSSusHiCrossSections.pdf')
    plt.close()

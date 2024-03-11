import configurer as config
import functions as TRSM

import numpy as np
import pandas
from scipy.interpolate import CubicSpline

import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    # configDict = {'mH1_lb': 1,      'mH1_ub': 124,    'mH1Points': 100,
    #               'mH2_lb': 125.09, 'mH2_ub': 125.09,
    #               'mH3_lb': 126,    'mH3_ub': 500,    'mH3Points': 100,
    #               'thetahS_lb': 1.352,  'thetahS_ub': 1.352,
    #               'thetahX_lb': 1.175,  'thetahX_ub': 1.175,
    #               'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407,
    #               'vs_lb': 120, 'vs_ub': 120,
    #               'vx_lb': 890, 'vx_ub': 1000, 'vxPoints': 890}
    
    
    ScannerS_H1H2, ScannerS_H1H1, ScannerS_H2H2 = TRSM.ppXNPSM_massfree('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 
                                             'mH1', 'mH2', 'mH3', 'bb', 'gamgam', normalizationSM=(31.02 * 10**(-3)) * 0.0026)

    ScannerS_13_mH1 = ScannerS_H1H2[0]
    ScannerS_13_mH3 = ScannerS_H1H2[2]
    ScannerS_13_b_H1_bb_H2_gamgam = ScannerS_H1H2[4]
    
    SusHi_H1H2, SusHi_H1H1, SusHi_H2H2 = TRSM.ppXNPSM_massfree('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 
                                             'mH1', 'mH2', 'mH3', 'bb', 'gamgam', normalizationSM = (31.02 * 10**(-3)) * 0.0026,
                                             run3=True, pathRun3Data='13TeV_SusHiCrossSections.tsv')

    SusHi_13_mH1 = SusHi_H1H2[0]
    SusHi_13_mH3 = SusHi_H1H2[2]
    SusHi_13_b_H1_bb_H2_gamgam = SusHi_H1H2[4]
    
    #[print(f'{SusHi_13_b_H1_bb_H2_gamgam[i]}, {ScannerS_13_b_H1_bb_H2_gamgam[i]}') for i in range(len(ScannerS_13_b_H1_bb_H2_gamgam[::10]))]

    plt.scatter(SusHi_13_mH1, SusHi_13_mH3, c=ScannerS_13_b_H1_bb_H2_gamgam)
    plt.colorbar()
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_BP2ScannerS.pdf')
    plt.close()

    plt.scatter(SusHi_13_mH1, SusHi_13_mH3, c=SusHi_13_b_H1_bb_H2_gamgam)
    plt.colorbar()
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_BP2SusHi.pdf')
    plt.close()

    
    ratio = SusHi_13_b_H1_bb_H2_gamgam/ScannerS_13_b_H1_bb_H2_gamgam  

    plt.scatter(SusHi_13_mH1, SusHi_13_mH3, c=ratio)
    plt.colorbar()
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_BP2ScannerSSusHiRatio.pdf')
    plt.close()
    
    toPrint = list(zip(ScannerS_13_mH1, ScannerS_13_mH3, SusHi_13_b_H1_bb_H2_gamgam, ScannerS_13_b_H1_bb_H2_gamgam, ratio))

    for mH1, mH3, SusHi, ScannerS, ratio in toPrint:
        print(f'mH1: {mH1}, mH3: {mH3}, SusHi: {SusHi:.3e}, ScannerS: {ScannerS:.3e}, ratio: {ratio}\n')

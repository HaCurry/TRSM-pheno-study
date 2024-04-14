import configurer as config
import functions as TRSM

import numpy as np
import pandas
from scipy.interpolate import CubicSpline

import matplotlib.pyplot as plt

if __name__ == '__main__': 

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to plotting directory
    pathPlots ='/eos/user/i/ihaque/SusHiPlots' 
    
    ### The 13 TeV plots below are only for validating SusHi ###
 
    ### 13 TeV cross sections ###
 
    ScannerS_H1H2, ScannerS_H1H1, ScannerS_H2H2 = TRSM.ppXNPSM_massfree('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 
                                             'mH1', 'mH2', 'mH3', 'bb', 'gamgam', normalizationSM=1)#(31.02 * 10**(-3)) * 0.0026)

    ScannerS_13_mH1 = ScannerS_H1H2[0]
    ScannerS_13_mH3 = ScannerS_H1H2[2]
    ScannerS_13_b_H1_bb_H2_gamgam = ScannerS_H1H2[4]
    
    SusHi_H1H2, SusHi_H1H1, SusHi_H2H2 = TRSM.ppXNPSM_massfree('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 
                                             'mH1', 'mH2', 'mH3', 'bb', 'gamgam', normalizationSM=1,#(31.02 * 10**(-3)) * 0.0026,
                                             run3=True, pathRun3Data='13TeV_SusHiCrossSections.tsv')

    SusHi_13_mH1 = SusHi_H1H2[0]
    SusHi_13_mH3 = SusHi_H1H2[2]
    SusHi_13_b_H1_bb_H2_gamgam = SusHi_H1H2[4]
    
    #[print(f'{SusHi_13_b_H1_bb_H2_gamgam[i]}, {ScannerS_13_b_H1_bb_H2_gamgam[i]}') for i in range(len(ScannerS_13_b_H1_bb_H2_gamgam[::10]))]

    ## 13 TeV BP2 ScannerS cross sections ##

    plt.scatter(SusHi_13_mH1, SusHi_13_mH3, c=ScannerS_13_b_H1_bb_H2_gamgam)
    plt.colorbar()
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/BP2/13TeV_BP2ScannerS.pdf')
    plt.close()

    ## 13 TeV BP2 SusHi cross sections ##

    plt.scatter(SusHi_13_mH1, SusHi_13_mH3, c=SusHi_13_b_H1_bb_H2_gamgam)
    plt.colorbar()
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/BP2/13TeV_BP2SusHi.pdf')
    plt.close()

    ## 13 TeV BP2 SusHi/ScannerS (ratio) cross sections ##
    
    ratio = SusHi_13_b_H1_bb_H2_gamgam/ScannerS_13_b_H1_bb_H2_gamgam  

    plt.scatter(SusHi_13_mH1, SusHi_13_mH3, c=ratio)
    plt.colorbar()
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/BP2/13TeV_BP2ScannerSSusHiRatio.pdf')
    plt.close()
    
    toPrint = list(zip(ScannerS_13_mH1, ScannerS_13_mH3, SusHi_13_b_H1_bb_H2_gamgam, ScannerS_13_b_H1_bb_H2_gamgam, ratio))

    # for mH1, mH3, SusHi, ScannerS, ratio in toPrint:
    #     print(f'mH1: {mH1}, mH3: {mH3}, SusHi: {SusHi:.3e}, ScannerS: {ScannerS:.3e}, ratio: {ratio}\n')


    ## 13.6 TeV BP2 cross sections ##

    SusHi_H1H2, SusHi_H1H1, SusHi_H2H2 = TRSM.ppXNPSM_massfree('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 
                                             'mH1', 'mH2', 'mH3', 'bb', 'gamgam', normalizationSM=1,#(31.02 * 10**(-3)) * 0.0026,
                                             run3=True, pathRun3Data='13_6TeV_SusHiCrossSections.tsv')

    SusHi_13_6_mH1 = SusHi_H1H2[0]
    SusHi_13_6_mH3 = SusHi_H1H2[2]
    SusHi_13_6_b_H1_bb_H2_gamgam = SusHi_H1H2[4]

    plt.scatter(SusHi_13_6_mH1, SusHi_13_6_mH3, c=SusHi_13_6_b_H1_bb_H2_gamgam)
    plt.colorbar()
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13_6TeV/BP2/13_6TeV_BP2SusHi.pdf')
    plt.close()

    ## 13.6 TeV BP3 cross sections ##    

    SusHi_H1H2, SusHi_H1H1, SusHi_H2H2 = TRSM.ppXNPSM_massfree('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/plots2D/BP3_BR_XSH/output_BP3_BR_XSH.tsv', 
                                             'mH1', 'mH2', 'mH3', 'bb', 'gamgam', normalizationSM=1,#(31.02 * 10**(-3)) * 0.0026,
                                             run3=True, pathRun3Data='13_6TeV_SusHiCrossSections.tsv')

    SusHi_13_6_mH1 = SusHi_H1H2[0]
    SusHi_13_6_mH3 = SusHi_H1H2[2]
    SusHi_13_6_b_H2_bb_H1_gamgam = SusHi_H1H2[5]

    plt.scatter(SusHi_13_6_mH1, SusHi_13_6_mH3, c=SusHi_13_6_b_H2_bb_H1_gamgam)
    plt.colorbar()
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13_6TeV/BP3/13_6TeV_BP3SusHi.pdf')
    plt.close()


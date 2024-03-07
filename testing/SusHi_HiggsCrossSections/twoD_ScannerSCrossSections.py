import configurer as config
import functions as TRSM

import subprocess
import os

import numpy as np
import pandas
import matplotlib
import matplotlib.pyplot as plt

if __name__ == '__main__':

    with open('ggH_bbH.dat') as f:
        first_line = f.readline()
    
    masses = ([float(i) for i in first_line.split()])
    crossSec = []    
    
    BFB, Uni, STU, Higgs = 0, 0, 0, 0
    pathTemp = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/TRSMOutputsTemp'
    pathExecutionConfig = os.path.join(pathTemp, 'temp_config.tsv')
    pathExecutionOutput = os.path.join(pathTemp, 'temp_output.tsv')
    pathTRSM = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken'

    for mass in masses:
        
        dictModelParams = {'mH1_lb': 1, 'mH1_ub': 1,
                           'mH2_lb': 2, 'mH2_ub': 2,
                           'mH3_lb': mass, 'mH3_ub': mass,
                           'thetahS_lb': 1.352,  'thetahS_ub': 1.352,
                           'thetahX_lb': 1.175,  'thetahX_ub': 1.175,
                           'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407,
                           'vs_lb': 120, 'vs_ub': 120,
                           'vx_lb': 890, 'vx_ub': 890}

        # creates contents of pathExecutionConfig
        config.checkCreatorNew(pathExecutionConfig, dictModelParams)

        # for subprocesses.run below
        runTRSM = [pathTRSM, '--BFB', str(BFB), '--Uni', str(Uni), '--STU', str(STU), '--Higgs', str(Higgs), pathExecutionOutput, 'check', pathExecutionConfig]

        # run the executable
        shell_output = subprocess.run(runTRSM, cwd=pathTemp)

        df = pandas.read_table(pathExecutionOutput)
        TRSMCrossSec = df['x_H3_gg'][0]
        SMCrossSec = df['x_H3_gg'][0]/(df['R31'][0]**2)
        
        crossSec.append((mass, TRSMCrossSec, SMCrossSec))
    # add also in dataframe a column with the kappa_3**2 divided for easier comparison with SusHi!  
    dfOut = pandas.DataFrame(crossSec, columns=['mass', 'TRSMCrossSec', 'SMCrossSec'])
    print(dfOut)
    dfOut.to_csv('13TeV_ScannerSCrossSections.tsv', sep='\t')

    plt.plot(np.array(dfOut['mass']), np.array(dfOut['TRSMCrossSec']), marker='o')
    plt.yscale('log')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_ScannerSTRSMCrossSections.pdf')
    plt.close()

    plt.plot(np.array(dfOut['mass']), np.array(dfOut['SMCrossSec']), marker='o')
    plt.yscale('log')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/13TeV/13TeV_ScannerSSMCrossSections.pdf')
    plt.close()

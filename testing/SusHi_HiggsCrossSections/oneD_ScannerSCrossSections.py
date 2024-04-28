import configurer as config

import subprocess
import os
import json

import numpy as np
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import matplotlib.lines as mlines

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/'

    # path to plotting directory
    # E:
    pathPlots = '/eos/user/i/ihaque/SusHiPlots'

    # path to ScannerS TRSM executable
    # E:
    pathTRSM = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken'

    # create plotting directory if they do not already exist
    os.makedirs(os.path.join(pathPlots), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, '13TeV'), exist_ok=True)

    # create directories which ScannerS will store output and input
    # if they do not already exist
    pathTemp = os.path.join(pathRepo,
                            'testing/SusHi_HiggsCrossSections/TRSMOutputsTemp')
    os.makedirs(pathTemp, exist_ok=True)

    with open(os.path.join(pathRepo,
              'testing/SusHi_HiggsCrossSections/ggH_bbH.dat')) as f:
        first_line = f.readline()

    # create dictionary where all output from ScannerS will be stored
    massesAndCrossSec = {}
    massesAndCrossSec['mass'] = []
    massesAndCrossSec['TRSMCrossSec'] = []
    massesAndCrossSec['SMCrossSec'] = []

    # masses which ScannerS will generate cross sections for
    masses = ([float(i) for i in first_line.split()])

    # disable all ScannerS TRSM constraints
    BFB, Uni, STU, Higgs = 0, 0, 0, 0

    # path to where the output and input of ScannerS is stored
    pathTemp = os.path.join(pathRepo,
                            'testing/SusHi_HiggsCrossSections/TRSMOutputsTemp')
    pathExecutionConfig = os.path.join(pathTemp, 'temp_config.tsv')
    pathExecutionOutput = os.path.join(pathTemp, 'temp_output.tsv')

    for mass in masses:

        dictModelParams = {'mH1_lb': 1, 'mH1_ub': 1,
                           'mH2_lb': 2, 'mH2_ub': 2,
                           'mH3_lb': mass, 'mH3_ub': mass,
                           'thetahS_lb': 1.352,  'thetahS_ub': 1.352,
                           'thetahX_lb': 1.175,  'thetahX_ub': 1.175,
                           'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407,
                           'vs_lb': 120, 'vs_ub': 120,
                           'vx_lb': 890, 'vx_ub': 890}

        # creates a .tsv file with model parameters in pathExecutionConfig
        # given by dictModelParams, the TRSM executable will take this as
        # input
        config.checkCreatorNew(pathExecutionConfig, dictModelParams)

        # command line arguments required when running the ScannerS
        # TRSM executable
        runTRSM = [pathTRSM, '--BFB', str(BFB), '--Uni', str(Uni),
                   '--STU', str(STU), '--Higgs', str(Higgs), 
                   pathExecutionOutput, 'check', pathExecutionConfig]

        # run the ScannerS TRSM executable
        shell_output = subprocess.run(runTRSM, cwd=pathTemp)

        df = pandas.read_table(pathExecutionOutput)
        TRSMCrossSec = df['x_H3_gg'][0]
        SMCrossSec = df['x_H3_gg'][0]/(df['R31'][0]**2)

        # crossSec.append((mass, TRSMCrossSec, SMCrossSec))
        massesAndCrossSec['mass'].append(mass)
        massesAndCrossSec['SMCrossSec'].append(SMCrossSec)
        massesAndCrossSec['TRSMCrossSec'].append(TRSMCrossSec)

    dfScannerS_13 = pandas.DataFrame(massesAndCrossSec)
    print(dfScannerS_13)
    dfScannerS_13.to_csv('13TeV_ScannerSCrossSections.tsv', sep='\t')

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

    # plot the TRSM cross sections
    plt.plot(np.array(dfScannerS_13['mass']), np.array(dfScannerS_13['TRSMCrossSec']),
             marker='o')
    plt.yscale('log')
    plt.savefig(os.path.join(pathPlots, '13TeV',
                '13TeV_ScannerSTRSMCrossSections.pdf'))
    plt.close()

    # plot the SM cross sections
    plt.plot(np.array(dfScannerS_13['mass']), np.array(dfScannerS_13['SMCrossSec']),
             marker='o')
    plt.yscale('log')
    plt.savefig(os.path.join(pathPlots, '13TeV',
                '13TeV_ScannerSSMCrossSections.pdf'))
    plt.close()



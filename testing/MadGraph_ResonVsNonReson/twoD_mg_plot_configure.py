import os
import subprocess

import numpy as np
import pandas
from helpScannerS import configurer as config
from helpScannerS import functions as TRSM

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/'

    # path to condor job output
    # E:
    pathOutputParent = '/eos/user/i/ihaque/MadgraphResonVsNonResonOutput'

    # runName
    # E:
    runName = 'nevents10000_preFINAL2'

    # path to ScannerS TRSM executable
    # E:
    pathTRSM = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken'

    # path to output
    pathMadgraphOutput = os.path.join(pathRepo, 'testing',
                                      'MadGraph_ResonVsNonReson',
                                      'MadgraphResonVsNonReson.tsv')

    ## read in the 2023 Atlas limits
    limitsUntransposed = pandas.read_json(os.path.join(pathRepo,
                                                       'Atlas2023Limits.json'))
    print(limitsUntransposed)
    limits=limitsUntransposed.T
    print(limits)

    ms = [element for element in limits['S']]
    mx = [element for element in limits['X']]

    # save it in pb
    dataIds = [element for element in limits.index]

    # save all madgraph output in a dict
    dictOut = {'mH1': [], 'mH2': [], 'mH3': [],
               'thetahS': [], 'thetahX': [], 'thetaSX': [],
               'vs': [], 'vx': [],
               'ms': [], 'mx': [],
               'pp_eta0h': [], 'pp_iota0_eta0h': [], 
               'ratio': [],
               'x_X_SH_SnS': [],
               'x_X_S_bb_H_gamgam_SnS': []} # x_X_S_bb_H_gamgam is not used
                                            # but can be useful to have

    skipDataIds = ['X190_S15', 'X210_S15', 'X230_S15', 'X250_S15']
    for dataId in dataIds:

        if dataId in skipDataIds:
            continue

        else:
            path = os.path.join(pathOutputParent, dataId, runName,
                                f'output_{dataId}_{runName}.tsv')

            dfMadgraph = pandas.read_table(path)

            dictOut['mH1'].append(dfMadgraph['mH1'][0])
            dictOut['mH2'].append(dfMadgraph['mH2'][0])
            dictOut['mH3'].append(dfMadgraph['mH3'][0])
            dictOut['thetahS'].append(dfMadgraph['thetahS'][0])
            dictOut['thetahX'].append(dfMadgraph['thetahX'][0])
            dictOut['thetaSX'].append(dfMadgraph['thetaSX'][0])
            dictOut['vs'].append(dfMadgraph['vs'][0])
            dictOut['vx'].append(dfMadgraph['vx'][0])

            ## save in ATLAS notation as well
            if abs(dfMadgraph['mH2'][0] - 125.09) < 10**(-6):
                ms = dfMadgraph['mH1'][0]
                mx = dfMadgraph['mH3'][0]
                x_X_S_bb_H_gamgam = 'x_H3_H1_bb_H2_gamgam'


            elif abs(dfMadgraph['mH1'][0] - 125.09) < 10**(-6):
                ms = dfMadgraph['mH2'][0]
                mx = dfMadgraph['mH3'][0]
                x_X_S_bb_H_gamgam = 'x_H3_H1_gamgam_H2_bb'

            x_X_SH = 'x_H3_H1H2'

            dictOut['ms'].append(ms)
            dictOut['mx'].append(mx)

            dictOut['pp_iota0_eta0h'].append(dfMadgraph['pp_iota0_eta0h'][0])
            dictOut['pp_eta0h'].append(dfMadgraph['pp_eta0h'][0])
            dictOut['ratio'].append(dfMadgraph['ratio'][0])

            ScannerSConfig = {'mH1_lb': dfMadgraph['mH1'][0], 'mH1_ub': dfMadgraph['mH1'][0],
                              'mH2_lb': dfMadgraph['mH2'][0], 'mH2_ub': dfMadgraph['mH2'][0],
                              'mH3_lb': dfMadgraph['mH3'][0], 'mH3_ub': dfMadgraph['mH3'][0],
                              'thetahS_lb': dfMadgraph['thetahS'][0], 'thetahS_ub': dfMadgraph['thetahS'][0],
                              'thetahX_lb': dfMadgraph['thetahX'][0], 'thetahX_ub': dfMadgraph['thetahX'][0],
                              'thetaSX_lb': dfMadgraph['thetaSX'][0], 'thetaSX_ub': dfMadgraph['thetaSX'][0],
                              'vs_lb': dfMadgraph['vs'][0], 'vs_ub': dfMadgraph['vs'][0],
                              'vx_lb': dfMadgraph['vx'][0], 'vx_ub': dfMadgraph['vx'][0]}

            pathScannerSWorkingDir = os.path.join(pathRepo, 'testing', 
                                                  'MadGraph_ResonVsNonReson', 
                                                  'ScannerSTemp',)

            pathScannerSConfig = os.path.join(pathScannerSWorkingDir,
                                              f'config_X{mx}_S{ms}.tsv')

            pathScannerSOutput = os.path.join(pathScannerSWorkingDir,
                                              f'output_X{mx}_S{ms}.tsv')

            config.checkCreatorNew(pathScannerSConfig, ScannerSConfig)

            constraints = ['--BFB', '0', '--Uni', '0', '--STU', '0', '--Higgs',
                           '0']
            shellPrompt = [pathTRSM, *constraints, pathScannerSOutput, 'check',
                           pathScannerSConfig]
            subprocess.run(shellPrompt, cwd=pathScannerSWorkingDir)

            obs = TRSM.observables(pathScannerSOutput, 'bb', 'gamgam',
                                   normSM=1, saveAll=True)

            # sanity check
            if (len(obs[x_X_S_bb_H_gamgam]) == 1 or
                len(obs['x_H3_H1_bb_H2_gamgam']) == 1):
                pass
            else:
                raise Exception('something went wrong in the TRSM output file...')

            dictOut['x_X_SH_SnS'].append(obs[x_X_SH][0])

            # this is not really used, but can be useful to have
            dictOut['x_X_S_bb_H_gamgam_SnS'].append(obs[x_X_S_bb_H_gamgam][0])

    df = pandas.DataFrame(dictOut)
    df.to_csv(pathMadgraphOutput, sep='\t')


import os

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
    pathOutputParent = '/eos/user/i/ihaque/AtlasLimitsGridSearchOutput' 
   
    ## read in the 2023 Atlas limits
    limitsUntransposed = pandas.read_json(os.path.join(pathRepo, 'Atlas2023Limits.json'))
    print(limitsUntransposed)
    limits=limitsUntransposed.T
    print(limits)

    ms = [element for element in limits['S']]
    mx = [element for element in limits['X']]

    # save it in pb
    XS = [element for element in 10**(-3) *limits['ObservedLimit']]
    dataIds = [element for element in limits.index]

    # dataId below will be the name of the folder containing all
    # the output (i.e cross sections and madgraph output) from execution
    # of the corresponding model parameters in listModelTuples
    listModelTuples = []
    for i in range(len(dataIds)):

        if 125.09 < ms[i]:
            listModelTuples.append((125.09, ms[i], mx[i], XS[i], dataIds[i], ms[i], mx[i]))

        elif ms[i] < 125.09:
            listModelTuples.append((ms[i], 125.09, mx[i], XS[i], dataIds[i], ms[i], mx[i]))

        else:
            raise Exception('Something went wrong')

    dictMax = {'mH1': [],
               'mH2': [], 
               'mH3': [],
               'thetahS': [],
               'thetahX': [], 
               'thetaSX': [],
               'vs': [], 
               'vx': [],
               'x_X_S_bb_H_gamgam_max': [],
               'ObsLimExclusions': [],
               'ScannerSExclusions': [],
               'ObsLim': [],
               'dataId': [],
               'ms': [],
               'mx': []}

    keys = ['mH1', 'mH2',  'mH3', 'thetahS', 'thetahX',  'thetaSX', 'vs',  'vx']

    for (mH1, mH2, mH3, XS, dataId, msElement, mxElement) in listModelTuples:
        pathOutput = os.path.join(pathOutputParent, dataId, f'output_{dataId}.tsv')
        obs = TRSM.observables(pathOutput, 'bb', 'gamgam', 
                               *keys,
                               normSM=1)

        dfObs = pandas.read_table(pathOutput)

        # quick sanity check
        if (mH1 == obs['mH1'][0]) and (mH2 == obs['mH2'][0]) and (mH3 == obs['mH3'][0]):
            pass

        else:
            raise Exception('Something went wrong in one of the sanity checks\n\
                            please check your code')

        # key for X -> S(bb) H(gamgam)

        # BP2
        if abs(mH2 - 125.09) < 10**(-6):
            x_X_S_bb_H_gamgam = 'x_H3_H1_bb_H2_gamgam'

        # BP3
        elif abs(mH1 - 125.09) < 10**(-6):
            x_X_S_bb_H_gamgam = 'x_H3_H1_gamgam_H2_bb'

        else:
            raise Exception('Something went wrong...')

        # find the (index with) model paramaters that give the maximum
        # cross section x_X_S_bb_H_gamgam in the ScannerS output file
        # pathOutput
        index = np.nanargmax(obs[x_X_S_bb_H_gamgam])

        # if there are nans in obs then the maximum using np.argmax
        # will be a np.nan (as opposed to using np.nanargmax which avoids
        # np.nans). Good sanity check to check if there are any np.nans.
        indexNan = np.argmax(obs[x_X_S_bb_H_gamgam])

        if index == indexNan:
            pass

        else:
            print(f'np.nanargmax and np.argmax giving different indices\n\
                  probably np.nans in\n\
                  {pathOutput}')

        dictMax['x_X_S_bb_H_gamgam_max'].append(obs[x_X_S_bb_H_gamgam][index])

        # append the model parameters which give maximum cross section
        for key in keys:
            dictMax[key].append(obs[key][index])

        # sanity check
        numOfModels = len(dfObs)
        if numOfModels == len(obs[x_X_S_bb_H_gamgam]):
            pass

        else:
            raise Exception('Something went wrong in one of the sanity checks\n\
                            please check your code')

        # check how many models are excluded by the Atlas limit
        numOfObsLimExclusions = 0
        for i in range(numOfModels):
            if XS/obs[x_X_S_bb_H_gamgam][i] < 1:
                numOfObsLimExclusions = numOfObsLimExclusions + 1 

            else:
                pass

        # save the number of models excluded by the Atlas limit
        dictMax['ObsLimExclusions'].append(numOfObsLimExclusions)

        # check how many are excluded by ScannerS constraints
        # (it is just the number of rows in the ScannerS input
        # subtracted by the number of rows in the ScannerS 
        # output)
        numOfScannerSExclusions = 100000 - numOfModels

        # save the number of ScannerS exclusions
        dictMax['ScannerSExclusions'].append(numOfScannerSExclusions)

        # save the observed limit
        dictMax['ObsLim'].append(XS)

        # save the dataId
        dictMax['dataId'].append(dataId)

        # save the Atlas notation of the masses
        dictMax['ms'].append(msElement)
        dictMax['mx'].append(mxElement)

    dfOut = pandas.DataFrame(dictMax)

    dfOut.to_csv(os.path.join(pathRepo, 'AtlasLimitsGridSearch', 'AtlasLimitsGridSearchMax.tsv'),
                 sep='\t')

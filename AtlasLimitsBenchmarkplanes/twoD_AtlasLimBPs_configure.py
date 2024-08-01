import os
import glob
import subprocess

import numpy as np
import pandas
from helpScannerS import configurer as config

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/'

    # path to output
    # E:
    pathOutputParent = '/eos/user/i/ihaque/AtlasLimitsBenchmarkplaneOutput' 

    # path to ScannerS TRSM executable
    # E:
    pathTRSM = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken'

    # constraints
    # E: (or you can leave as is)
    BFB, Uni, STU, Higgs = 0, 0, 0, 0 

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
            listModelTuples.append((125.09, ms[i], mx[i], XS[i], dataIds[i]))

        elif ms[i] < 125.09:
            listModelTuples.append((ms[i], 125.09, mx[i], XS[i], dataIds[i]))

        else:
            raise Exception('Something went wrong')

    print(f"\nms: {len(ms)}", f"mx: {len(mx)}", f"XS: {len(XS)}", f"listModelTuples: {len(listModelTuples)}\n")

    # create the model parameters for each mass point in the ATLAS limits
    listModelParams = []
    for (mH1, mH2, mH3, XS, dataId) in listModelTuples:
        # BP2
        if abs(mH2 - 125.09) < 10**(-6):
            listModelParams.append({'mH1_lb': mH1, 'mH1_ub': mH1,
                                    'mH2_lb': mH2, 'mH2_ub': mH2,
                                    'mH3_lb': mH3, 'mH3_ub': mH3,
                                    'thetahS_lb': 1.352,  'thetahS_ub': 1.352,  'thetahSPoints':1,
                                    'thetahX_lb': 1.175,  'thetahX_ub': 1.175,  'thetahXPoints':1,
                                    'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407, 'thetaSXPoints':1,
                                    'vs_lb': 120, 'vs_ub': 120, 'vsPoints': 1,
                                    'vx_lb': 890, 'vx_ub': 890, 'vxPoints': 1,
                                    'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} })

        # BP3
        elif abs(mH1 - 125.09) < 10**(-6):
            listModelParams.append({'mH1_lb': mH1, 'mH1_ub': mH1,
                                    'mH2_lb': mH2, 'mH2_ub': mH2,
                                    'mH3_lb': mH3, 'mH3_ub': mH3,
                                    'thetahS_lb': -0.129,  'thetahS_ub': -0.129,  'thetahSPoints':1,
                                    'thetahX_lb': 0.226,  'thetahX_ub': 0.226,  'thetahXPoints':1,
                                    'thetaSX_lb': -0.899, 'thetaSX_ub': -0.899, 'thetaSXPoints':1,
                                    'vs_lb': 140, 'vs_ub': 140, 'vsPoints': 1,
                                    'vx_lb': 100, 'vx_ub': 100, 'vxPoints': 1,
                                    'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} })

        else:
            raise Exception('something went wrong')

    # this file is actually not necessary for this script
    pathDataIds = os.path.join(pathOutputParent, 'dataIds.txt')

    # create the directory structure
    config.configureDirs(listModelParams, pathOutputParent, pathDataIds)

    paths = glob.glob(os.path.join(pathOutputParent, 'X*_S*'))

    # sanity check to make sure all dataIds are found in pathOutputParent
    if len(paths) == len(limits):
        pass

    else:
        raise Exception(f'dataIds missing in {pathOutputParent}')

    constraints = ['--BFB', str(BFB), '--Uni', str(Uni), '--STU', str(STU), '--Higgs', str(Higgs)]

    frames = []

    for modelParam in listModelParams:
        dataId = modelParam['extra']['dataId']
        ObsLim = modelParam['extra']['ObservedLimit']
        configPath = os.path.join(pathOutputParent, dataId, f'config_{dataId}.tsv')
        outputPath = os.path.join(pathOutputParent, dataId, f'output_{dataId}.tsv')
        cwd = os.path.join(pathOutputParent, dataId)
        runTRSM = [pathTRSM, *constraints, outputPath, 'check', configPath]
        subprocess.run(runTRSM, cwd=cwd)
        dfModelParam = pandas.read_table(outputPath, index_col=0)
        dfModelParam['dataId'] = dataId
        dfModelParam['ObsLim'] = ObsLim
        frames.append(dfModelParam)

    df = pandas.concat(frames, ignore_index=True)
    df.to_csv(os.path.join(pathRepo, 'AtlasLimitsBenchmarkplanes', 'AtlasLimitsBenchmarkplanes.tsv'),
              sep='\t')


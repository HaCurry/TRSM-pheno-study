import numpy as np
import pandas
import configurer as config
import os


if __name__ == '__main__':
    
    # THIS IS WRITTEN SO THIS SCRIPT IS NOT ACCIDENTALLY RUN!

    limitsUntransposed = pandas.read_json('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/Atlas2023Limits.json')
    print(limitsUntransposed)
    limits=limitsUntransposed.T
    print(limits)

    ms = [element for element in limits['S']]
    mx = [element for element in limits['X']]
    # save it in pb
    XS = [element for element in 10**(-3) *limits['ObservedLimit']]
    indices = [element for element in limits.index]

    listModelTuples = []
    for i in range(len(indices)):

        if 125.09 < ms[i]:
            listModelTuples.append((125.09, ms[i], mx[i], XS[i], indices[i]))

        elif ms[i] < 125.09:
            listModelTuples.append((ms[i], 125.09, mx[i], XS[i], indices[i]))

        else:
            raise Exception('Something went wrong')

    print(f"\nms: {len(ms)}", f"mx: {len(mx)}", f"XS: {len(XS)}", f"listModelTuples: {len(listModelTuples)}\n")

    # print(listModelTuples[0:5])

    listModelParams = []
    for (mH1, mH2, mH3, XS, dataId) in listModelTuples:

        # BP2
        if abs(mH2 - 125.09) < 10**(-10):
            listModelParams.append({'mH1_lb': mH1, 'mH1_ub': mH1,
                                    'mH2_lb': mH2, 'mH2_ub': mH2,
                                    'mH3_lb': mH3, 'mH3_ub': mH3,
                                    'thetahS_lb': 1.352,  'thetahS_ub': 1.352,  'thetahSPoints':1,
                                    'thetahX_lb': 1.175,  'thetahX_ub': 1.175,  'thetahXPoints':1,
                                    'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407, 'thetaSXPoints':1,
                                    'vs_lb': 120, 'vs_ub': 120, 'vsPoints': 1,
                                    'vx_lb': 890, 'vx_ub': 890, 'vxPoints': 1,
                                    'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} })

        elif abs(mH1 - 125.09) < 10**(-10):
            listModelParams.append({'mH1_lb': mH1, 'mH1_ub': mH1,
                                    'mH2_lb': mH2, 'mH2_ub': mH2,
                                    'mH3_lb': mH3, 'mH3_ub': mH3,
                                    'thetahS_lb': -0.129, 'thetahS_ub': -0.129, 'thetahSPoints':1,
                                    'thetahX_lb': 0.226,  'thetahX_ub': 0.226,  'thetahXPoints':1,
                                    'thetaSX_lb': -0.899, 'thetaSX_ub': -0.899, 'thetaSXPoints':1,
                                    'vs_lb': 140, 'vs_ub': 140, 'vsPoints': 1,
                                    'vx_lb': 100, 'vx_ub': 100, 'vxPoints': 1,
                                    'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} })

        else: raise Exception('something went wrong...')

    # submission path
    afsPath ='/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_ScriptTesting/AtlasLimitsMaxCondor_ScriptTesting/AtlasLimitsMax_configure_ScriptTesting' 
    # input and output path
    eosPath = '/eos/user/i/ihaque/testing/AtlasLimitsMax_ScriptTesting/AtlasLimitsMax_configure_ScriptTesting' 
 
    config.configureDirs(listModelParams, '/eos/user/i/ihaque/testing/AtlasLimitsMax_ScriptTesting/AtlasLimitsMax_configure_ScriptTesting',
                         os.path.join(afsPath ,'dataIds.txt'))

    config.condorScriptCreator(eosPath, 
                               os.path.join(afsPath, 'scannerS.sh'), 
                               os.path.join(afsPath, 'scannerS.sub'), 
                               os.path.join(afsPath, 'dataIds.txt'), 
                               JobFlavour='testmatch')

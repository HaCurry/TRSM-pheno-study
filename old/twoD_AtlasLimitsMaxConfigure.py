import numpy as np
import pandas
import configurer as config
from os.path import abspath


if __name__ == '__main__':
    
    # THIS IS WRITTEN SO THIS SCRIPT IS NOT ACCIDENTALLY RUN!

    limitsUntransposed = pandas.read_json('Atlas2023Limits.json')
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

    listModelParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
                        'mH2_lb': mH2, 'mH2_ub': mH2,
                        'mH3_lb': mH3, 'mH3_ub': mH3,
                        'thetahS_lb': 0.95 * (-np.pi/2), 'thetahS_ub': 0.95 * (np.pi/2), 'thetahSPoints':10,
                        'thetahX_lb': 0.95 * (-np.pi/2), 'thetahX_ub': 0.95 * (np.pi/2), 'thetahXPoints':10,
                        'thetaSX_lb': 0.95 * (-np.pi/2), 'thetaSX_ub': 0.95 * (np.pi/2), 'thetaSXPoints':10,
                        'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 10,
                        'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 10,
                        'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} } for (mH1, mH2, mH3, XS, dataId) in listModelTuples]
    
    config.configureDirs(listModelParams, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4',
                         '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/AtlasLimitsMaxCondor/AtlasLimitsMax_configure4/dataIds.txt')

    config.condorScriptCreator('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure4', 
                               '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/AtlasLimitsMaxCondor/AtlasLimitsMax_configure4/scannerS.sh', 
                               '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/AtlasLimitsMaxCondor/AtlasLimitsMax_configure4/scannerS.sub', 
                               '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/AtlasLimitsMaxCondor/AtlasLimitsMax_configure4/dataIds.txt', 
                               JobFlavour='workday')

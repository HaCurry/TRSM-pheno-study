import numpy as np
import pandas
import configurer as config
from os.path import abspath


if __name__ == '__main__':
    
    #THIS IS WRITTEN SO THIS SCRIPT IS NOT ACCIDENTALLY RUN!
    df = pandas.read_table('AtlasLimitsMax_OnlySingles.tsv')
    print(df)
    ms = [element for element in df['ms']]
    mx = [element for element in df['mx']]

    mH1 = [element for element in df['mH1']]
    mH2 = [element for element in df['mH2']]
    mH3 = [element for element in df['mH3']]
    thetahS = [element for element in df['thetahS']]
    thetahX = [element for element in df['thetahX']]
    thetaSX = [element for element in df['thetaSX']]
    vs = [element for element in df['vs']]
    vx = [element for element in df['vx']]
    ObsLim = [element for element in df['Observed Limit']]
    dataId = [f'X{mx[i]:.0f}_S{ms[i]:.0f}' for i in range(len(mx))]

    listModelTuples  = tuple(zip(mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, dataId, ObsLim))
    listModelParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
                        'mH2_lb': mH2, 'mH2_ub': mH2,
                        'mH3_lb': mH3, 'mH3_ub': mH3,
                        'thetahS_lb': thetahS, 'thetahS_ub': thetahS + 0.2, 'thetahSPoints': 5,
                        'thetahX_lb': thetahX, 'thetahX_ub': thetahX + 0.2, 'thetahXPoints': 5,
                        'thetaSX_lb': thetaSX, 'thetaSX_ub': thetaSX + 0.2, 'thetaSXPoints': 5,
                        'vs_lb': vs, 'vs_ub': vs + 0.2, 'vsPoints': 5,
                        'vx_lb': vx, 'vx_ub': vx + 0.2, 'vxPoints': 5,
                        'extra': {'dataId': f'{dataId}', 'ObservedLimit': ObsLim} } for (mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, dataId, ObsLim) in listModelTuples] 

    config.configureDirs(listModelParams, '/eos/user/i/ihaque/testing/AtlasLimitsMax_OnlySingles/AtlasLimitsMax_configure_OnlySingles',
                         '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_OnlySingles/AtlasLimitsMaxCondorTesting/AtlasLimitsMax_configure_testing/dataIds.txt')

    config.condorScriptCreator('/eos/user/i/ihaque/testing/AtlasLimitsMax_OnlySingles/AtlasLimitsMax_configure_OnlySingles',
                               '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_OnlySingles/AtlasLimitsMaxCondorTesting/AtlasLimitsMax_configure_testing/scannerS.sh',
                               '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_OnlySingles/AtlasLimitsMaxCondorTesting/AtlasLimitsMax_configure_testing/scannerS.sub',
                               '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_OnlySingles/AtlasLimitsMaxCondorTesting/AtlasLimitsMax_configure_testing/dataIds.txt',
                               JobFlavour='longlunch')


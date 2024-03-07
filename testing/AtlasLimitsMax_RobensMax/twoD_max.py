import numpy as np
import pandas

import json

import configurer as config
import functions as TRSM

if __name__ == '__main__':
    H1H2, H1H1, H2H2 = TRSM.ppXNPSM_massfree('TRSMBroken.tsv', 'mH1', 'mH2', 'mH3', 'bb', 'gamgam', normalizationSM = 1) 
    
    mode = 4
    crossSec = H1H2[mode]
    maximum = (np.max(crossSec))

    with open('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_RobensMax/condor.err') as f:
        errors = f.read()

    dictOut = {'mH1': H1H2[0][0], 'mH2': H1H2[1][0], 'mH3': H1H2[2][0], 'max': maximum, 'mode': mode, 'points': len(crossSec), 'errors': errors}
    print(dictOut)
    with open("/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_RobensMax/robensOutput.json", "a") as outfile: 
        json.dump(dictOut, outfile, indent=4)


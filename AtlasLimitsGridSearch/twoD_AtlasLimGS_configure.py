import os
import glob
import subprocess

import numpy as np
import pandas
from helpScannerS import configurer as config

def condorScriptCreator(pathExecutable,
                        pathExecOutputParent,
                        pathExecTRSM,
                        TRSMBFB,
                        TRSMUni,
                        TRSMSTU,
                        TRSMHiggs,
                        pathSubmit,
                        JobFlavour,
                        pathDataIds):

    '''
    OBS!: do NOT append slashes '/' at the end of the paths in the input
          arguments.

    Input arguments with ...Exec... refer to the condor executable.

    Remaining input arguments refer to the submit file (pathSubmit, 
    JobFlavour, pathDataIds).

    pathExecutable: string
        path to where the condor executable will be written.

    pathExecOutputParent: string 
        path to the directory where all the output from
        the condor jobs will be output (i.e the cross
        sections).

    pathExecTRSM: string
        path to the ScannerS TRSM executable the condor executable
        executes.

    TRSMBFB: int
        ScannerS TRSM constraint BFB (bounded from below).

    TRSMUni: int
        ScannerS TRSM constraint Uni (unitarity).

    TRSMSTU: int
        ScannerS TRSM constraint STU (STU).

    TRSMHiggs: int
        ScannerS TRSM constraint Higgs (Higgs bounds and Higgs signals
        constraint)

    pathSubmit: string
        path to where the condor submit file will be written.

    JobFlavour: string
        The maximal run time for a condor job (see
        https://batchdocs.web.cern.ch/tutorial/exercise6b.html for more
        information).

    pathDataIds: string
        names of the directories where output from the condor jobs
        will be output (i.e cross sections). 

    returns: None
    '''

    condorExecutable = f'''#!/bin/bash
# condor executable

pathCondorJobOutput={pathExecOutputParent}/${{1}}
pathExecTRSM={pathExecTRSM}

cd $pathCondorJobOutput
${{pathExecTRSM}} --BFB {TRSMBFB} --Uni {TRSMUni} --STU {TRSMSTU} --Higgs {TRSMHiggs} ${{pathCondorJobOutput}}/output_${{1}}.tsv check ${{pathCondorJobOutput}}/config_${{1}}.tsv

'''

    with open(pathExecutable, 'w') as executableFile:
        executableFile.write(condorExecutable)

    condorSubmit = f''' # condor submit file
executable              = {pathExecutable}

getenv                  = True
log                     = $(dataId).log
output                  = $(dataId).out
error                   = $(dataId).err
arguments               = $(dataId)
    
# longlunch = 2 hrs
+JobFlavour             = "{JobFlavour}"

queue dataId from {pathDataIds}'''

    with open(pathSubmit, 'w') as submitFile:
        submitFile.write(condorSubmit)

    print('+------------------------------+')
    print(f'creating condor executable {pathExecutable}')
    print('+------------------------------+')
    print(condorExecutable)
    print('\n')
    print('+------------------------------+')
    print(f'creating condor submit file {pathSubmit}')
    print('+------------------------------+')
    print(condorSubmit)


if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/'

    # path to condor job output
    # E:
    pathOutputParent = '/eos/user/i/ihaque/AtlasLimitsGridSearchOutput' 

    # path to ScannerS TRSM executable
    # E:
    pathTRSM = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken'

    # path to directory containing condor submit file and executable
    pathCondorSubmitAndExecute = os.path.join(pathRepo, 'AtlasLimitsGridSearch', 'AtlasLimitsGridSearchCondor')

    os.makedirs(pathCondorSubmitAndExecute, exist_ok=True)

    # constraints
    # E: (or you can leave as is)
    BFB, Uni, STU, Higgs = 1, 1, 1, 1 

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
    listModelParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
                        'mH2_lb': mH2, 'mH2_ub': mH2,
                        'mH3_lb': mH3, 'mH3_ub': mH3,
                        'thetahS_lb': 0.95 * (-np.pi/2), 'thetahS_ub': 0.95 * (np.pi/2), 'thetahSPoints':10,
                        'thetahX_lb': 0.95 * (-np.pi/2), 'thetahX_ub': 0.95 * (np.pi/2), 'thetahXPoints':10,
                        'thetaSX_lb': 0.95 * (-np.pi/2), 'thetaSX_ub': 0.95 * (np.pi/2), 'thetaSXPoints':10,
                        'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 10,
                        'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 10,
                        'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} } for (mH1, mH2, mH3, XS, dataId) in listModelTuples]

    # this file is actually not necessary for this script
    pathDataIds = os.path.join(pathCondorSubmitAndExecute, 'dataIds.txt')

    # create the directory structure
    config.configureDirs(listModelParams, pathOutputParent, pathDataIds)


    # sanity check to make sure all dataIds are found in pathOutputParent
    paths = glob.glob(os.path.join(pathOutputParent, 'X*_S*'))
    if len(paths) == len(limits):
        pass

    else:
        raise Exceptions(f'dataIds missing in {pathOutputParent}')

    # path to condor executable
    pathExecutable = os.path.join(pathCondorSubmitAndExecute, 'condorExecutable.sh')

    # path to condor submit file
    pathSubmit = os.path.join(pathCondorSubmitAndExecute, 'condorSubmit.sub')
    
    # create condor executable and submit file 
    condorScriptCreator(pathExecutable,
                        pathOutputParent,
                        pathTRSM,
                        BFB,
                        Uni,
                        STU,
                        Higgs,
                        pathSubmit,
                        'longlunch',
                        pathDataIds)

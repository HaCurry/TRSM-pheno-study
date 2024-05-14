import os
import glob
import subprocess

import numpy as np
import pandas
from helpScannerS import configurer as config

def condorScriptCreator(pathExecutable, pathExecOutputParent, pathExecTRSM, pathSubmit, JobFlavour, pathDataIds):

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

cd $pathCondorJobOutput/nofree
${{pathExecTRSM}} --BFB 0 --Uni 0 --STU 0 --Higgs 0 ${{pathCondorJobOutput}}/nofree/output_${{1}}_nofree.tsv check ${{pathCondorJobOutput}}/nofree/config_${{1}}_nofree.tsv

cd $pathCondorJobOutput/thetahS
${{pathExecTRSM}} --BFB 0 --Uni 0 --STU 0 --Higgs 0 ${{pathCondorJobOutput}}/thetahS/output_${{1}}_thetahS.tsv check ${{pathCondorJobOutput}}/thetahS/config_${{1}}_thetahS.tsv

cd $pathCondorJobOutput/thetahX
${{pathExecTRSM}} --BFB 0 --Uni 0 --STU 0 --Higgs 0 ${{pathCondorJobOutput}}/thetahX/output_${{1}}_thetahX.tsv check ${{pathCondorJobOutput}}/thetahX/config_${{1}}_thetahX.tsv

cd $pathCondorJobOutput/thetaSX
${{pathExecTRSM}} --BFB 0 --Uni 0 --STU 0 --Higgs 0 ${{pathCondorJobOutput}}/thetaSX/output_${{1}}_thetaSX.tsv check ${{pathCondorJobOutput}}/thetaSX/config_${{1}}_thetaSX.tsv

cd $pathCondorJobOutput/vs
${{pathExecTRSM}} --BFB 0 --Uni 0 --STU 0 --Higgs 0 ${{pathCondorJobOutput}}/vs/output_${{1}}_vs.tsv check ${{pathCondorJobOutput}}/vs/config_${{1}}_vs.tsv

cd $pathCondorJobOutput/vx
${{pathExecTRSM}} --BFB 0 --Uni 0 --STU 0 --Higgs 0 ${{pathCondorJobOutput}}/vx/output_${{1}}_vx.tsv check ${{pathCondorJobOutput}}/vx/config_${{1}}_vx.tsv'''

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
        raise Exceptions(f'dataIds missing in {pathOutputParent}')

    constraints = ['--BFB', str(BFB), '--Uni', str(Uni), '--STU', str(STU), '--Higgs', str(Higgs)]

    frames = []

    for modelParam in listModelParams:
        dataId = modelParam['extra']['dataId']
        configPath = os.path.join(pathOutputParent, dataId, f'config_{dataId}.tsv')
        outputPath = os.path.join(pathOutputParent, dataId, f'output_{dataId}.tsv')
        cwd = os.path.join(pathOutputParent, dataId)
        runTRSM = [pathTRSM, *constraints, outputPath, 'check', configPath]
        subprocess.run(runTRSM, cwd=cwd)
        frames.append(pandas.DataFrame(outputPath))

    df = pandas.concat(frames, ignore_index=True)
    df.to_csv(os.path.join(pathRepo, 'AtlasLimitsBenchmarkplanes', 'AtlasLimitsBenchmarkplanes.tsv'))


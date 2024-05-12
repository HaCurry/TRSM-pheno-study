import os
import copy

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
    pathOutputParent = '/eos/user/i/ihaque/parameter1DPlots' 

    # path to ScannerS TRSM executable
    # E:
    pathTRSM = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken'

    # path to param1D directory
    pathParam1D = os.path.join(pathRepo, 'parameter1D')

    freeParams = {'thetahS': [-np.pi/2, +np.pi/2],
                  'thetahX': [-np.pi/2, +np.pi/2], 
                  'thetaSX': [-np.pi/2, +np.pi/2], 
                  'vs': [1, 1000],
                  'vx': [1, 1000]}

    points = 100

    for regionX in ['region1', 'region2']:

        for BPX in ['BP2', 'BP3']:

            path_BPX_regionX = os.path.join(pathRepo, 'parameter1D', 'grids', f'{BPX}_{regionX}.tsv')
            df = pandas.read_table(path_BPX_regionX)

            # create template model parameters from which each free parameter can
            # be varied
            if BPX == 'BP2':
                modelParams = [{'mH1_lb': df['mH1'][i], 'mH1_ub': df['mH1'][i], 'mH1Points': 1,
                                'mH2_lb': df['mH2'][i], 'mH2_ub': df['mH2'][i], 'mH2Points': 1,
                                'mH3_lb': df['mH3'][i], 'mH3_ub': df['mH3'][i], 'mH3Points': 1,
                                'thetahS_lb': 1.352,  'thetahS_ub': 1.352,  'thetahSPoints': 1,
                                'thetahX_lb': 1.175,  'thetahX_ub': 1.175,  'thetahXPoints': 1,
                                'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407, 'thetaSXPoints': 1,
                                'vs_lb': 120, 'vs_ub': 120, 'vsPoints': 1,
                                'vx_lb': 890, 'vx_ub': 890, 'vxPoints': 1,
                                'extra': {'dataId': f'X{df["mH3"][i]}_S{df["mH1"][i]}'}} for i in range(len(df))]

            if BPX == 'BP3':
                modelParams = [{'mH1_lb': df['mH1'][i], 'mH1_ub': df['mH1'][i], 'mH1Points': 1,
                                'mH2_lb': df['mH2'][i], 'mH2_ub': df['mH2'][i], 'mH2Points': 1,
                                'mH3_lb': df['mH3'][i], 'mH3_ub': df['mH3'][i], 'mH3Points': 1,
                                'thetahS_lb': -0.129, 'thetahS_ub': -0.129, 'thetahSPoints': 1,
                                'thetahX_lb': 0.226,  'thetahX_ub': 0.226,  'thetahXPoints': 1,
                                'thetaSX_lb': -0.899, 'thetaSX_ub': -0.899, 'thetaSXPoints': 1,
                                'vs_lb': 140, 'vs_ub': 140, 'vsPoints': 1,
                                'vx_lb': 100, 'vx_ub': 100, 'vxPoints': 1,
                                'extra': {'dataId': f'X{df["mH3"][i]}_S{df["mH2"][i]}'}} for i in range(len(df))]

            # path to condor output for BPX and regionX
            pathOutput_BPX_regionX = os.path.join(pathOutputParent, BPX, regionX)

            # path to where the condor scripts are written
            pathCondorScriptsOutput_BPX_regionX = os.path.join(pathRepo, 'parameter1D', 'param1DCondor', BPX, regionX) 

            # create the directory specified by pathCondorScriptsOutput_BPX_regionX if it already does not exists
            os.makedirs(pathCondorScriptsOutput_BPX_regionX, exist_ok=True)
            
            # path to file with dataIds. The condor submit executable will use this as input for each job
            pathOutputDataIds_BPX_regionX = os.path.join(pathCondorScriptsOutput_BPX_regionX, 'dataIds.txt')

            # create condor submit file and executable
            condorScriptCreator(os.path.join(pathCondorScriptsOutput_BPX_regionX, 'condorExecutable.sh'), 
                                os.path.join(pathOutputParent, BPX, regionX),
                                pathTRSM,
                                os.path.join(pathCondorScriptsOutput_BPX_regionX, 'condorSubmit.sub'),
                                'workday',
                                pathOutputDataIds_BPX_regionX)

            # create models where all parameters are fixed
            print(pathOutput_BPX_regionX)
            config.configureDirs(modelParams, pathOutput_BPX_regionX, pathOutputDataIds_BPX_regionX,
                                 childrenDirs='nofree')

            for key in freeParams:
                newModelParams = []
                
                # create models where we vary each parameter
                for element in modelParams:
                    newElement = copy.deepcopy(element)
                    newElement[f'{key}_lb'] = freeParams[key][0] 
                    newElement[f'{key}_ub'] = freeParams[key][1] 
                    newElement[f'{key}Points'] = points
                    newModelParams.append(newElement)

                config.configureDirs(newModelParams, pathOutput_BPX_regionX, pathOutputDataIds_BPX_regionX,
                                     childrenDirs=key)
                

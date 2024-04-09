import os
import numpy as np
import pandas
from helpScannerS import configurer as config


def condorScriptCreator(runNameExec,
                        pathExecutable,
                        pathExecPythonDir,
                        pathExecOutputParent,
                        neventsExec,
                        pathSubmit,
                        JobFlavour,
                        pathDataIds):
    '''
    OBS!: do NOT append slashes '/' at the end of the paths in the input
          arguments.

    Input arguments with ...Exec... refer to the condor executable.

    Remaining input arguments refer to the submit file (pathSubmit, 
    JobFlavour, pathDataIds).

    runNameExec: the string runName will be appended to the file and directory
                 names of the output from Madgraph and the python script below,
                 this is useful when multiple runs are executed in the same 
                 directory leading to conflicting names of output from Madgraph
                 and twoD_mgCrossSections.py.
    pathExecutable: path to where the condor executable will be written.
    pathExecPython: path to the directory where the python script 
                    twoD_mgCrossSections.py which the condor executable will
                    execute (OBS! not the path to twoD_mgCrossSection.py
                    just the path to the directory containing it).
    pathExecOutputParent: path to the directory where all the output from
                    the condor jobs will be output (i.e the cross
                    sections).
    neventsExec: number of events in the Madgraph calculations.
    pathSubmit: path to where the condor submit file will be written.
    JobFlavour: The maximal run time for a condor job (see
                https://batchdocs.web.cern.ch/tutorial/exercise6b.html for more
                information).
    pathDataIds: names of the directories where output from the condor jobs
                 will be output (i.e cross sections). See __main__ in 
                 twoD_mgConfigure.py and configure.configureDirs for more
                 information.
    '''
    # create directories for the condor jobs. Each directory name can be found in dataIds.txt
    # where the dataIds are defined in listModelParams
    
    submit = f'''# submit file for Madgraph jobs
executable              = {pathExecutable}

getenv                  = True
log                     = $(dataId).$(ClusterId).$(ProcId).condor.log
output                  = $(dataId).$(ClusterId).$(ProcId).condor.out
error                   = $(dataId).$(ClusterId).$(ProcId).condor.err
arguments               = $(dataId)

# longlunch = 2 hrs
+JobFlavour             = "{JobFlavour}"

queue dataId from {pathDataIds}'''

    with open(pathSubmit, 'w') as submitFile:
        submitFile.write(submit)

    executable = f'''#!/bin/bash
# executable for Madgraph jobs

# Required packages for generating run_card in twoD_mgCrossSections.py
pip3 install scipy==1.6.2
pip3 install numpy==1.22.4
pip3 install pandas==2.2.0

# the string runName will be appended to the file and directory names of the
# output from Madgraph and the python script below
runName={runNameExec}

# job output path
pathExecOutputJob={pathExecOutputParent}/${{1}}/${{runName}}

# path to directory containing Madgraph exec and model
pathExecMadgraphAndModel={pathExecOutputParent}/${{1}}

# path to Madgraph executable
pathExecMadgraph=${{pathExecMadgraphAndModel}}/MG5_aMC_v3_5_3/bin/mg5_aMC

# path to TRSM model
pathExecModel=${{pathExecMadgraphAndModel}}/twosinglet-master

# Madgraph events
neventsExec={neventsExec:.0f}

# path to tsv file containing TRSM model parameters for madgraph
pathExecConfig=${{pathExecOutputJob}}/config_${{1}}_${{runName}}.tsv

# Enter directory and run python script which runs Madgraph 
cd {os.path.dirname(pathExecPython)}
echo "running twoD_mgCrossSections.py (Madgraph)..."
time python3 twoD_mgCrossSections.py ${{runName}} ${{pathExecMadgraph}} ${{pathExecConfig}} ${{pathExecOutputJob}} ${{pathExecModel}} ${{neventsExec}}'''

    with open(pathExecutable, 'w') as executableFile:
        executableFile.write(executable)

    print('+------------------------------+')
    print(f'creating condor executable {pathExecutable}')
    print('+------------------------------+')
    print(executable)
    print('\n')
    print('+------------------------------+')
    print(f'creating condor submit file {pathSubmit}')
    print('+------------------------------+')
    print(submit)

if __name__ == '__main__':

    limitsUntransposed = pandas.read_json('../../Atlas2023Limits.json')
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

    # for (mH1, mH2, mH3, XS, dataId) in listModelTuples:
    #     # BP2
    #     if abs(mH2 - 125.09) < 10**(-6):
    #         listModelParams.append({'mH1_lb': 125.09, 'mH1_ub': 125.09,
    #                                 'mH2_lb': 200, 'mH2_ub': 200,
    #                                 'mH3_lb': 400, 'mH3_ub': 400,
    #                                 'thetahS_lb': -0.129,  'thetahS_ub': -0.129,  'thetahSPoints':1,
    #                                 'thetahX_lb': 0.226,  'thetahX_ub': 0.226,  'thetahXPoints':1,
    #                                 'thetaSX_lb': -0.899, 'thetaSX_ub': -0.899, 'thetaSXPoints':1,
    #                                 'vs_lb': 140, 'vs_ub': 140, 'vsPoints': 1,
    #                                 'vx_lb': 100, 'vx_ub': 100, 'vxPoints': 1,
    #                                 'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} })

    #     # BP3
    #     elif abs(mH1 - 125.09) < 10**(-6):
    #         listModelParams.append({'mH1_lb': 125.09, 'mH1_ub': 125.09,
    #                                 'mH2_lb': 200, 'mH2_ub': 200,
    #                                 'mH3_lb': 400, 'mH3_ub': 400,
    #                                 'thetahS_lb': -0.129,  'thetahS_ub': -0.129,  'thetahSPoints':1,
    #                                 'thetahX_lb': 0.226,  'thetahX_ub': 0.226,  'thetahXPoints':1,
    #                                 'thetaSX_lb': -0.899, 'thetaSX_ub': -0.899, 'thetaSXPoints':1,
    #                                 'vs_lb': 140, 'vs_ub': 140, 'vsPoints': 1,
    #                                 'vx_lb': 100, 'vx_ub': 100, 'vxPoints': 1,
    #                                 'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} })

    #     else:
    #         raise Exception('something went wrong') 

    newListModelParams = []
    desiredPoints = ['X170_S30', 'X210_S70', 'X325_S110',
                     'X375_S125', 'X400_S200', 'X450_S70', 'X500_S125',
                     'X550_S300', 'X750_S50', 'X850_S125', 'X900_S400', 
                     'X375_S70', 'X240_S100', 'X300_S150', 'X500_S325',
                     'X550_S185', 'X525_S250', 'X475_S170']

    for element in listModelParams:
        if element['extra']['dataId'] in desiredPoints:
            newListModelParams.append(element)
        else:
            continue

    if len(newListModelParams) != len(desiredPoints):
        print([element['extra']['dataId'] for element in newListModelParams])
        raise Exception('Not all desired points were found')

    listModelParams = newListModelParams

    [print(f'{element["mH1_lb"]:.0f}, {element["mH2_lb"]:.0f}, {element["mH3_lb"]:.0f}') for element in listModelParams]

    # path to parent directory containing all the mass points (dataId)
    # each mass point corresponds to a condor job
    pathExecOutputParent = '/eos/user/i/ihaque/MadgraphResonVsNonReson/MadgraphResonVsNonReson'

    # runNameExec will be created as a directory inside each mass point (dataId) 
    # the condor job output i.e the cross sections will be found there
    runNameExec = 'nevents10000_v3'

    # path to file listing mass points (dataIds)
    pathDataIds = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents10000_v3/dataIds.txt'

    # create the above directory structure
    config.configureDirs(listModelParams, pathExecOutputParent, pathDataIds,
                         childrenDirs=runNameExec)

    # path to condor executable
    pathExecutable = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents10000_v3/condorExecutable.sh'

    # path to condor submit file
    pathSubmit = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents10000_v3/condorSubmit.sub'
    
    # path to the directory containing the python script which the condor executable executes
    pathExecPython = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/twosinglet_scalarcouplings/twoD_mgCrossSections.py'

    # number of Madgraph events
    neventsExec = 10000

    # condor maximum runtime for each job (see condor docs for more info)
    JobFlavour = 'workday'

    # create the condor submit file and condor executable
    condorScriptCreator(runNameExec,
                        pathExecutable,
                        pathExecPython,
                        pathExecOutputParent,
                        neventsExec,
                        pathSubmit,
                        JobFlavour,
                        pathDataIds)


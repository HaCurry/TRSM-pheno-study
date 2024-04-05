import os
import numpy as np
import pandas
from helpScannerS import configurer as config


def condorScriptCreatorOpt(runNameExec,
                           pathExecutable,
                           pathExecPythonDir,
                           pathExecOutputParent,
                           neventsExec,
                           init_pointsOpt,
                           n_iterOpt,
                           pathSubmit,
                           JobFlavour,
                           pathDataIds):
    '''
    OBS!: do NOT append slashes '/' at the end of the paths in the input
          arguments.

    Input arguments with ...Exec... refer to the condor executable.

    Input arguments with ...Opt refer to parameters for the Bayesian
    optimization. Please see the bayesian optimization examples section
    for more information:  
    https://github.com/bayesian-optimization/BayesianOptimization/blob/master/examples/basic-tour.ipynb
    
    Remaining input arguments refer to the submit file (pathSubmit, 
    JobFlavour, pathDataIds).
    
    pathExecutable: path to where the condor executable will be written.
    pathExecPython: path to the directory where the python script 
                    twoD_mgCrossSections.py which the condor executable will
                    execute (OBS! not the path to twoD_mgCrossSection.py
                    just the path to the directory containing it).
    pathExecMadgraph: path to the madgraph executable.
    pathExecOutputParent: path to the directory where all the output from
                    the condor jobs will be output (i.e the cross
                    sections).
    pathExecModel: path to the TRSM model https://gitlab.com/apapaefs/twosinglet
    neventsExec: number of events in the Madgraph calculations.
    n_iterOpt: number of iterations in the Bayesian optimization.
    init_pointsOpt: number of initial points for the Bayesian optimization 
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

# required packages for generating run_card in twoD_mgCrossSectionsOpt.py
pip3 install scipy==1.6.2
pip3 install numpy==1.22.4
pip3 install pandas==2.2.0
    
# install Bayesian optimization python package
pip3 install bayesian-optimization==1.4.3
    
# Bayesian optimization parameters
init_pointsOpt={init_pointsOpt:.0f}
n_iterOpt={n_iterOpt:.0f}

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
time python3 twoD_mgCrossSectionsOpt.py ${{runName}} ${{pathExecMadgraph}} ${{pathExecConfig}} ${{pathExecOutputJob}} ${{pathExecModel}} ${{neventsExec}} ${{init_pointsOpt}} ${{n_iterOpt}}'''

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


    # Only the masses are fixed, Bayesian optimization will try to find the
    # optimal values on the angles and vevs so that the ratio of 
    # resonant and non-resonant cross section is maximized. 

    # The angles and vevs are set to an arbitrary value only so that 
    # config.configureDirs works, otherwise an error is raised
    listModelParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
                        'mH2_lb': mH2, 'mH2_ub': mH2,
                        'mH3_lb': mH3, 'mH3_ub': mH3,
                        'thetahS_lb': 0, 'thetahS_ub': 0, # these parameters we do not care about
                        'thetahX_lb': 0, 'thetahX_ub': 0, # these parameters we do not care about
                        'thetaSX_lb': 0, 'thetaSX_ub': 0, # these parameters we do not care about
                        'vs_lb': 0, 'vs_ub': 0, # these parameters we do not care about
                        'vx_lb': 0, 'vx_ub': 0, # these parameters we do not care about
                        'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} } for (mH1, mH2, mH3, XS, dataId) in listModelTuples]

    newListModelParams = []
    desiredPoints = ['X170_S30', 'X210_S70', 'X325_S110',
                     'X375_S125', 'X400_S200', 'X450_S70', 'X500_S125',
                     'X550_S300', 'X750_S50', 'X850_S125', 'X900_S400']
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
    runNameExec = 'nevents100_bayOpt1'

    # path to file listing mass points (dataIds)
    pathDataIds = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents100_bayOpt1/dataIds.txt'

    # create the above directory structure
    config.configureDirs(listModelParams, pathExecOutputParent, pathDataIds,
                         childrenDirs=runNameExec)

    # path to condor executable
    pathExecutable = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents100_bayOpt1/condorExecutableOpt.sh'

    # path to condor submit file
    pathSubmit = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents100_bayOpt1/condorSubmitOpt.sub'

    # path to the directory containing the python script which the condor executable executes
    pathExecPython = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/twosinglet_scalarcouplings/twoD_mgCrossSections.py'

    # number of Madgraph events
    neventsExec = 100

    # number of initial bayesian optimization points
    init_pointsOpt = 0

    # number of bayesian optimization iterations
    n_iterOpt = 2

    # condor maximum runtime for each job (see condor docs for more info)
    JobFlavour = 'tomorrow'

    # create the condor submit file and condor executable
    condorScriptCreatorOpt(runNameExec,
                           pathExecutable,
                           pathExecPython,
                           pathExecOutputParent,
                           neventsExec,
                           init_pointsOpt,
                           n_iterOpt,
                           pathSubmit,
                           JobFlavour,
                           pathDataIds)


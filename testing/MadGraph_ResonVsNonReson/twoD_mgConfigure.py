import os
import numpy as np
import pandas
from helpScannerS import configurer as config


def condorScriptCreator(pathExecutable,
                        pathExecPythonDir,
                        pathExecMadgraphAndTRSM,
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

# job output path
pathExecOutputJob={pathExecOutputParent}/${{1}}
    
# copy tarball (containing Madgraph and model) to job output path
echo "copying tarball into job output path"
time cp {pathExecMadgraphAndTRSM} ${{pathExecOutputJob}}

# cd to job output path and extract tarball
cd ${{pathExecOutputJob}}
echo "extracting tarball in job output path"
time tar -xf ${{pathExecOutputJob}}/{os.path.basename(pathExecMadgraphAndTRSM)}

# path to Madgraph executable
pathExecMadgraph=${{pathExecOutputJob}}/MG5_aMC_v3_5_3/bin/mg5_aMC

# path to TRSM model is now
pathExecModel=${{pathExecOutputJob}}/twosinglet

# Madgraph events
neventsExec={neventsExec:.0f}

# path to tsv file containgin TRSM model parameters for madgraph
pathExecConfig=${{pathExecOutputJob}}/config_${{1}}.tsv

# Enter directory and run python script which runs Madgraph 
cd {pathExecPython}
echo "running Madgraph..."
time python3 twoD_mgCrossSections.py ${{pathExecMadgraph}} ${{pathExecConfig}} ${{pathExecOutputJob}} ${{pathExecModel}} ${{neventsExec}}'''

    with open(pathExecutable, 'w') as executableFile:
        executableFile.write(executable)

    print('+------------------------------+')
    print(f'creating executable {pathExecutable}')
    print('+------------------------------+')
    print(executable)
    print('\n')
    print('+------------------------------+')
    print(f'creating submit file {pathSubmit}')
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

    # listModelParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
    #                     'mH2_lb': mH2, 'mH2_ub': mH2,
    #                     'mH3_lb': mH3, 'mH3_ub': mH3,
    #                     'thetahS_lb': 1.352,  'thetahS_ub': 1.352,  'thetahSPoints':1,
    #                     'thetahX_lb': 1.175,  'thetahX_ub': 1.175,  'thetahXPoints':1,
    #                     'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407, 'thetaSXPoints':1,
    #                     'vs_lb': 120, 'vs_ub': 120, 'vsPoints': 1,
    #                     'vx_lb': 890, 'vx_ub': 890, 'vxPoints': 1,
    #                     'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} } for (mH1, mH2, mH3, XS, dataId) in listModelTuples]

    listModelParams = []
    for (mH1, mH2, mH3, XS, dataId) in listModelTuples:
        # BP2
        if abs(mH1 - 125.09) < 10**(-6):
            listModelParams.append({'mH1_lb': mH1, 'mH1_ub': mH1,
                                    'mH2_lb': mH2, 'mH2_ub': mH2,
                                    'mH3_lb': mH3, 'mH3_ub': mH3,
                                    'thetahS_lb': -0.129,  'thetahS_ub': -0.129,  'thetahSPoints':1,
                                    'thetahX_lb': 0.226,  'thetahX_ub': 0.226,  'thetahXPoints':1,
                                    'thetaSX_lb': -0.899, 'thetaSX_ub': -0.899, 'thetaSXPoints':1,
                                    'vs_lb': 140, 'vs_ub': 140, 'vsPoints': 1,
                                    'vx_lb': 100, 'vx_ub': 100, 'vxPoints': 1,
                                    'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} })
        # BP3
        elif abs(mH2 - 125.09) < 10**(-6):
            listModelParams.append({'mH1_lb': mH1, 'mH1_ub': mH1,
                                    'mH2_lb': mH2, 'mH2_ub': mH2,
                                    'mH3_lb': mH3, 'mH3_ub': mH3,
                                    'thetahS_lb': 1.352,  'thetahS_ub': 1.352,  'thetahSPoints':1,
                                    'thetahX_lb': 1.175,  'thetahX_ub': 1.175,  'thetahXPoints':1,
                                    'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407, 'thetaSXPoints':1,
                                    'vs_lb': 120, 'vs_ub': 120, 'vsPoints': 1,
                                    'vx_lb': 890, 'vx_ub': 890, 'vxPoints': 1,
                                    'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} })

        else:
            raise Exception('something went wrong') 

    listModelParams = listModelParams[0:10]

    [print(f'{element["mH1_lb"]:.0f}, {element["mH2_lb"]:.0f}, {element["mH3_lb"]:.0f}') for element in listModelParams]

    # create directories for the condor jobs. Each directory name can be found in dataIds.txt
    # where the dataIds are defined in listModelParams
    config.configureDirs(listModelParams, '/eos/user/i/ihaque/MadgraphResonVsNonReson/MadgraphResonVsNonReson_nevents100_5',
                         '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents100_5/dataIds.txt')

    # path to condor executable
    pathExecutable = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents100_5/condorExecutable.sh'

    # path to the directory containing the python script which the condor executable executes
    pathExecPython = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/twosinglet_scalarcouplings'

    # path to tarball containing Madgraph and TRSM model
    pathExecMadgraphAndTRSM = '/eos/user/i/ihaque/MadgraphAndModelTarball/MadgraphAndTRSM.tar.gz'

    # path where the output from condor jobs are stored (i.e cross sections)
    pathExecOutputParent = '/eos/user/i/ihaque/MadgraphResonVsNonReson/MadgraphResonVsNonReson_nevents100_5'

    # number of Madgraph events
    neventsExec = 100

    # path to condor submit file
    pathSubmit = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents100_5/condorSubmit.sub'

    # condor maximum runtime for each job (see condor docs for more info)
    JobFlavour = 'tomorrow'

    # names of the directories where output from the condor jobs will be output
    # (i.e cross sections)
    pathDataIds = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents100_5/dataIds.txt'

    # create the condor submit file and condor executable
    condorScriptCreator(pathExecutable,
                        pathExecPython,
                        pathExecMadgraphAndTRSM,
                        pathExecOutputParent,
                        neventsExec,
                        pathSubmit,
                        JobFlavour,
                        pathDataIds)


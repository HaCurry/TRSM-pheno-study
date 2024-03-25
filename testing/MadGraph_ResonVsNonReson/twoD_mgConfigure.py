import os
import numpy as np
import pandas
from helpScannerS import configurer as config


def condorScriptCreator(pathExecutable, pathExecPythonDir, pathExecMadgraph, pathExecOutputParent, pathExecModel, neventsExec,
                        pathSubmit, JobFlavour, pathDataIds):
    '''
    OBS!: do NOT append slashes '/' at the end of the paths in the input
          arguments.

    Input arguments with ...Exec... refer to the condor executable,
    remaining input arguments refer to the submit file.
    
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

# copy TRSM model to job output path
pathExecOutputJob={pathExecOutputParent}/${{1}}
cp -r {pathExecModel} ${{pathExecOutputJob}}

# new path to TRSM model is now
pathExecModelNew=${{pathExecOutputJob}}/{os.path.basename(pathExecModel)}

# Enter directory and run python script which runs Madgraph 
cd {pathExecPython}

pathExecMadgraph={pathExecMadgraph}
pathExecConfig=${{pathExecOutputJob}}/config_${{1}}.tsv

time python3 twoD_mgCrossSections.py ${{pathExecMadgraph}} ${{pathExecConfig}} ${{pathExecOutputJob}} ${{pathExecModelNew}} {neventsExec}'''

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

    # listModelParams =  {'mH1_lb': mH1, 'mH1_ub': mH1,
    #                     'mH2_lb': mH2, 'mH2_ub': mH2,
    #                     'mH3_lb': mH3, 'mH3_ub': mH3,
    #                     'thetahS_lb': 0.95 * (-np.pi/2), 'thetahS_ub': 0.95 * (np.pi/2), 'thetahSPoints':1,
    #                     'thetahX_lb': 0.95 * (-np.pi/2), 'thetahX_ub': 0.95 * (np.pi/2), 'thetahXPoints':1,
    #                     'thetaSX_lb': 0.95 * (-np.pi/2), 'thetaSX_ub': 0.95 * (np.pi/2), 'thetaSXPoints':1,
    #                     'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 1,
    #                     'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 1,]
    # listModelParams =  {'mH1_lb': 90, 'mH1_ub': 90,
    #                     'mH2_lb': 125.09, 'mH2_ub': 125.09,
    #                     'mH3_lb': 400, 'mH3_ub': 400,
    #                     'thetahS_lb': 1.352, 'thetahS_ub': 1.4, 'thetahSPoints':2,
    #                     'thetahX_lb': 0.9, 'thetahX_ub': 1.175, 'thetahXPoints':2,
    #                     'thetaSX_lb': -0.407, 'thetaSX_ub': 0.407, 'thetaSXPoints':2,
    #                     'vs_lb': 120, 'vs_ub': 120, 'vsPoints': 1,
    #                     'vx_lb': 890, 'vx_ub': 890, 'vxPoints': 1}

    # config.checkCreatorNew('/eos/user/i/ihaque/resonanceTesting/config.tsv', listModelParams)
    # THIS IS WRITTEN SO THIS SCRIPT IS NOT ACCIDENTALLY RUN!

    limitsUntransposed = pandas.read_json('../../Atlas2023Limits.json')
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

    # dataId below will be the name of the folder containing all
    # the output (i.e cross sections and madgraph out) from execution
    # of the corresponding model parameters
    # listModelParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
    #                     'mH2_lb': mH2, 'mH2_ub': mH2,
    #                     'mH3_lb': mH3, 'mH3_ub': mH3,
    #                     'thetahS_lb': 0.95 * (-np.pi/2), 'thetahS_ub': 0.95 * (np.pi/2), 'thetahSPoints':1,
    #                     'thetahX_lb': 0.95 * (-np.pi/2), 'thetahX_ub': 0.95 * (np.pi/2), 'thetahXPoints':1,
    #                     'thetaSX_lb': 0.95 * (-np.pi/2), 'thetaSX_ub': 0.95 * (np.pi/2), 'thetaSXPoints':1,
    #                     'vs_lb': 500, 'vs_ub': 500, 'vsPoints': 1,
    #                     'vx_lb': 500, 'vx_ub': 500, 'vxPoints': 1,
    #                     'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} } for (mH1, mH2, mH3, XS, dataId) in listModelTuples]

    listModelParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
                        'mH2_lb': mH2, 'mH2_ub': mH2,
                        'mH3_lb': mH3, 'mH3_ub': mH3,
                        'thetahS_lb': 1.352,  'thetahS_ub': 1.352,  'thetahSPoints':1,
                        'thetahX_lb': 1.175,  'thetahX_ub': 1.175,  'thetahXPoints':1,
                        'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407, 'thetaSXPoints':1,
                        'vs_lb': 120, 'vs_ub': 120, 'vsPoints': 1,
                        'vx_lb': 890, 'vx_ub': 890, 'vxPoints': 1,
                        'extra': {'dataId': f'{dataId}', 'ObservedLimit': XS} } for (mH1, mH2, mH3, XS, dataId) in listModelTuples]

    listModelParams = listModelParams[:5]
    [print(f'{element["mH1_lb"]:.0f}, {element["mH2_lb"]:.0f}, {element["mH3_lb"]:.0f}') for element in listModelParams]

    # path to condor executable
    pathExecutable = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents10k/condorExecutable.sh'

    # path to python script which the condor executable executes
    pathExecPython = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/twosinglet_scalarcouplings'

    # path to madgraph executable
    pathExecMadgraph = '/eos/user/i/ihaque/madgraphTRSMTesting2/MG5_aMC_v3_5_3/bin/mg5_aMC'

    # path where the output from condor jobs are stored (i.e cross sections)
    pathExecOutputParent = '/eos/user/i/ihaque/MadgraphResonVsNonReson/MadgraphResonVsNonReson_nevents10k'

    # path to TRSM model
    pathExecModel = '/eos/user/i/ihaque/madgraphTRSMTesting2/MG5_aMC_v3_5_3/twosinglet'

    # number of Madgraph events
    neventsExe0c = 10000

    # path to condor submit file
    pathSubmit = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents10k/condorSubmit.sub'

    # condor maximum runtime for each job (see condor docs for more info)
    JobFlavour = 'tomorrow'

    # names of the directories where output from the condor jobs will be output
    # (i.e cross sections)
    pathDataIds = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents10k/dataIds.txt'

    # create the condor submit file and condor executable
    condorScriptCreator(pathExecutable, pathExecPython, pathExecMadgraph, pathExecOutputParent, pathExecModel, neventsExe0c,
                        pathSubmit, JobFlavour, pathDataIds)

    # create directories for the condor jobs. Each directory name can be found in dataIds.txt
    # where the dataIds are defined in listModelParams
    config.configureDirs(listModelParams, '/eos/user/i/ihaque/MadgraphResonVsNonReson/MadgraphResonVsNonReson_nevents10k',
                         '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_nevents10k/dataIds.txt')

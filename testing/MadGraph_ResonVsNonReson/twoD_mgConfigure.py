import os
import numpy as np
import pandas
from helpScannerS import configurer as config


def condorScriptCreator(runNameExec,
                        pathExecutable,
                        pathExecPython,
                        pathExecOutputParent,
                        eosPathExec,
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

    runNameExec: string 
        the string runName will be appended to the file and directory
        names of the output from Madgraph and the python script below,
        this is useful when multiple runs are executed in the same 
        directory leading to conflicting names of output from Madgraph
        and twoD_mgCrossSections.py.

    pathExecutable: string
        path to where the condor executable will be written.

    pathExecPython: string 
        path to the directory where the python script 
        twoD_mgCrossSections.py which the condor executable will
        execute (OBS! not the path to twoD_mgCrossSection.py
        just the path to the directory containing it).

    pathExecOutputParent: string 
        path to the directory where all the output from
        the condor jobs will be output (i.e the cross
        sections).

    eosPathExec: string
        due to the limited storage space in AFS, the output from Madgraph is moved
        to a specified directory in EOS.

    neventsExec: int
        number of events in the Madgraph calculations.

    pathSubmit: string
        path to where the condor submit file will be written.

    JobFlavour: string
        The maximal run time for a condor job (see
        https://batchdocs.web.cern.ch/tutorial/exercise6b.html for more
        information).

    pathDataIds: string
        names of the directories where output from the condor jobs
        will be output (i.e cross sections). See __main__ in 
        twoD_mgConfigure.py and configure.configureDirs for more
        information.

    returns: None
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

# set os
requirements = (OpSysAndVer =?= "AlmaLinux9")

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

# load lcg package so that you can use the ATLAS distribution of madgraph
source /cvmfs/sft.cern.ch/lcg/views/LCG_104c_ATLAS_5/x86_64-el9-gcc13-opt/setup.sh
lhapdf-config --incdir
lhapdf-config --libdir

# the string runName will be appended to the file and directory names of the
# output from Madgraph and the python script below
runName={runNameExec}

# job output path
pathExecOutputParentTmp=/tmp/ihaque/MadgraphResonVsNonReson
pathExecOutputJob=${{pathExecOutputParentTmp}}/${{1}}/${{runName}}
mkdir -p ${{pathExecOutputJob}}

# enter job output path
cd ${{pathExecOutputJob}}

# path to the ATLAS distribution of Madgraph executable
pathExecMadgraph=/cvmfs/sft.cern.ch/lcg/views/LCG_104c_ATLAS_5/x86_64-el9-gcc13-opt/bin/mg5_aMC

# copy model (TRSM: https://gitlab.com/apapaefs/twosinglet) to job output path
cp -r {pathExecOutputParent}/twosinglet-master ${{pathExecOutputParentTmp}}/${{1}}/

# path to the TRSM package
pathExecModel=${{pathExecOutputParentTmp}}/${{1}}/twosinglet-master

# Madgraph events
neventsExec={neventsExec:.0f}

# path to tsv file containing TRSM model parameters for madgraph
pathExecConfig={pathExecOutputParent}/${{1}}/${{runName}}/config_${{1}}_${{runName}}.tsv

# path to json file containing some additional data (not used, but can be useful)
pathExecSettings={pathExecOutputParent}/${{1}}/${{runName}}/settings_${{1}}_${{runName}}.json

# Enter directory and run python script which runs Madgraph 
cd {os.path.dirname(pathExecPython)}
echo "running twoD_mgCrossSections.py (Madgraph)..."
time python3 twoD_mgCrossSections.py ${{runName}} ${{pathExecMadgraph}} ${{pathExecConfig}} ${{pathExecOutputJob}} ${{pathExecModel}} ${{neventsExec}}

# delete the model
rm -r ${{pathExecModel}}

# path to Madraph output directory in EOS
eosOutputDir={eosPathExec}

# create the Madgraph output directory in EOS if it already does not exist
mkdir -p ${{eosOutputDir}}/${{1}}/

# Move the Madgraph output directory to EOS
mv ${{pathExecOutputParentTmp}}/${{1}}/${{runName}} ${{eosOutputDir}}/${{1}}/

# move config files to EOS as well
mv ${{pathExecConfig}} ${{eosOutputDir}}/${{1}}/${{runName}}/
mv ${{pathExecSettings}} ${{eosOutputDir}}/${{1}}/${{runName}}/
'''

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

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to parent directory containing all the mass points (dataId)
    # each mass point corresponds to a condor job
    # E:
    pathExecOutputParent = '/afs/cern.ch/user/i/ihaque/MadgraphResonVsNonReson'

    # runNameExec will be created as a directory inside each mass point (dataId) 
    # the condor job output i.e the cross sections will be found there
    # E: (or you can leave as is)
    runNameExec = 'nevents10000_preFINAL2'

    # Madgraph needs to be run and output its content on AFS, however after all the output
    # from Madgraph is output it is moved to a directory in EOS due to the limited storage
    # space in AFS
    # E:
    eosPathExec = '/eos/user/i/ihaque/MadgraphResonVsNonResonOutput'

    # number of Madgraph events
    # E: (or you can leave as is)
    neventsExec = 10000

    # condor maximum runtime for each job (see condor docs for more info or
    # batchdocs: https://batchdocs.web.cern.ch/tutorial/exercise6b.html )
    # E: (or you can leave as is)
    JobFlavour = 'longlunch'

    # path to where the condor submit files and executable will be
    # E:
    pathCondorSubAndExec = os.path.join(pathRepo, f'testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/{runNameExec}')

    # tries to create the directory
    try:
        os.makedirs(pathCondorSubAndExec)

    # if the directory already exists, warn the user
    except FileExistsError:
        print(f'The directory\n{pathCondorSubAndExec}\nalready exists, do you want to continue?')
        ans = input('y/n')

        if ans == 'y':
            pass

        elif ans =='n':
            raise Exception('user abort')

        else:
            raise Exception('invalid input, aborting')

    # path to file listing mass points (dataIds)
    pathDataIds = os.path.join(pathRepo, pathCondorSubAndExec, 'dataIds.txt')

    # path to condor executable
    pathExecutable = os.path.join(pathCondorSubAndExec, 'condorExecutable.sh')

    # path to condor submit file
    pathSubmit = os.path.join(pathCondorSubAndExec, 'condorSubmit.sub')
    
    # path to the directory containing the python script which the condor executable executes
    pathExecPython = os.path.join(pathRepo, 'testing/MadGraph_ResonVsNonReson/twosinglet_scalarcouplings/twoD_mgCrossSections.py')

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

    # pick the points you want to test
    # newListModelParams = []
    # desiredPoints = ['X170_S30', 'X210_S70', 'X325_S110',
    #                  'X375_S125', 'X400_S200', 'X450_S70', 'X500_S125',
    #                  'X550_S300', 'X750_S50', 'X850_S125', 'X900_S400', 
    #                  'X375_S70', 'X240_S100', 'X300_S150', 'X500_S325',
    #                  'X550_S185', 'X525_S250', 'X475_S170']

    # for element in listModelParams:
    #     if element['extra']['dataId'] in desiredPoints:
    #         newListModelParams.append(element)
    #     else:
    #         continue

    # if len(newListModelParams) != len(desiredPoints):
    #     print([element['extra']['dataId'] for element in newListModelParams])
    #     raise Exception('Not all desired points were found')

    # listModelParams = newListModelParams

    # [print(f'{element["mH1_lb"]:.0f}, {element["mH2_lb"]:.0f}, {element["mH3_lb"]:.0f}') for element in listModelParams]

    # create the directory structure for the condor output
    # for each point in listModelParams (see above) a separate directory
    # is created in pathExecOutputParent, in each directory another
    # directory called runNameExec is created (this is so that multiple runs
    # can be run in the same directory)
    config.configureDirs(listModelParams, pathExecOutputParent, pathDataIds,
                         childrenDirs=runNameExec)

    # create the condor submit file and condor executable
    condorScriptCreator(runNameExec,
                        pathExecutable,
                        pathExecPython,
                        pathExecOutputParent,
                        eosPathExec,
                        neventsExec,
                        pathSubmit,
                        JobFlavour,
                        pathDataIds)


import pandas
import numpy as np

import os
# REMOVE THESE COMMENTED LINES
# from os import makedirs
# from os.path import dirname
# from os.path import join

import functions as TRSM


def configureDirs(listModelParams, pathDir, **kwargs):

    ############################# kwargs #############################

    if 'existOk' in kwargs:
        existOk = kwargs['existOk']

    else: existOk = True

    ##################################################################

    # checks so that all ranges of the model parameters are given
    for element in listModelParams:

        if ('mH1_lb' in element and 'mH2_lb' in element and 'mH3_lb' in element 
            and  'mH1_ub' in element and 'mH2_ub' in element and 'mH3_ub' in element 
            and 'thetahS_lb' in element and 'thetahX_lb' in element and 'thetaSX_lb' in element 
            and 'thetahS_ub' in element and 'thetahX_ub' in element and 'thetaSX_ub' in element 
            and 'vs_lb' in element and 'vx_lb' in element 
            and 'vs_ub' in element and 'vx_ub' in element):
            pass
        else: raise Exception('The ranges of all model parameters are not defined') 

    os.makedirs(pathDir, exist_ok=existOk)
    mainModParFile = 'dataIds.txt'
    pathMainModParFile = pathDir + '/' + mainModParFile

    # clear contents of old ModelParams.txt
    open(pathMainModParFile, 'w').close()

    for element in listModelParams:

        # name of each directory where each set of model parameter configs are stored
        dataId = (element['extra'])['dataId']

        os.makedirs(pathDir + '/' + dataId, exist_ok=existOk)

        # create the configuration file (grid of all parameter combinations specified by element)
        twoDPlot.checkCreatorNew(pathDir + '/' + dataId + '/' + 'config_' + dataId + '.tsv', element)

        # store element in a JSON file in the directory (dataId)
        parameterData.createJSON(element, pathDir + '/' + dataId, 'settings_' + dataId + '.json')

        # store the name of the directory (dataId) in a txt file for later reference
        with open(pathMainModParFile, 'a') as myfile:
            myfile.write(dataId + '\n')



def condorScriptCreator(pathStartDir, pathExecutable, pathSubmit, **kwargs):

    ############################# kwargs #############################

    if 'pathScannerS' in kwargs:
        pathScannerS = kwargs['pathScannerS']

    else: 
        pathScannerS = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken'

    if 'JobFlavour' in kwargs:
        JobFlavour = kwargs['JobFlavour']
        
    else:
        JobFlavour = 'longlunch'

    ##################################################################

    # check correct file extions of pathExecutable, pathSubmit
    if pathExecutable.endswith('.sh'):
        pass
    
    else:
        raise Exception('File extension in pathExecutable need to be .sh')

    if pathSubmit.endswith('.sub'):
        pass

    else:
        raise Exception('File extension in pathSubmit need to be .sub')
           
    # create executable (docstrings does not work properly with fstrings)
    executable = ('#!/bin/bash\n'+
'# condor executable\n'+
'\n'+
'echo "trying to run scannerS on HTcondor..."\n'+
'\n'+
'# default values\n'+
'startDir=$(pwd)\n'+
'pathScannerS=/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken\n'+
'\n'+
'# user input values\n'+
'# from https://www.redhat.com/sysadmin/arguments-options-bash-scripts\n'+
'while getopts ":d:o:s:" option; do\n'+
'  case $option in\n'+
'    d) # starting directory path\n'+
'      startDir=$OPTARG;;\n'+
'    o) # ouput directory path\n'+
'      pathOutput=$OPTARG;;\n'+
'    s) # scannerS executable path\n'+
'      pathScannerS=$OPTARG;;\n'+
'    \?) # Invalid option\n'+
'      echo "Error: Invalid option"\n'+
'      exit;;\n'+
'  esac\n'+
'done\n'+
'\n'+
'# user needs to give path to output directory\n'+
'# from https://unix.stackexchange.com/a/621007/590852\n'+
': ${pathOutput:?Missing -o, please specify path to output directory}\n'+
'\n'+
'# cd into pathOutput\n'+
'echo "Entering $pathOutput"\n'+
'cd ${startDir}/${pathOutput}\n'+
'\n'+
'# execute ScannerS TRSM executable\n'+
'${pathScannerS} ${startDir}/${pathOutput}/output_${pathOutput}.tsv check ${startDir}/${pathOutput}/config_${pathOutput}.tsv\n'+
'echo "Finished job in $pathOutput"')        

    with open(pathExecutable, 'w') as executableFile:
        executableFile.write(executable)

    # create submit file for condor
    submit = '# sleep.sub -- simple sleep job\n\
executable              = scannerS.sh\n\
getenv                  = True\n\n\
log                     = $(inputDirectory)/scannerS.log\n\
output                  = $(inputDirectory)/scannerS.out\n\
error                   = $(inputDirectory)/scannerS.err\n\n\
arguments               = -o $(inputDirectory) -d {pathStartDir} -s {pathScannerS}\n\n\
# longlunch = 2 hrs\n\
+JobFlavour             = \"{JobFlavour}\"\n\n\
queue inputDirectory from dataIds.txt'.format(pathStartDir=pathStartDir, pathScannerS=pathScannerS, JobFlavour=JobFlavour)

    with open(pathSubmit, 'w') as submitFile:
        submitFile.write(submit)

    print('creating script {pathExecutable}'.format(pathExecutable=pathExecutable))
    print('+------------------------------+')
    print(executable)
    print('\n')
    print('creating script {pathSubmit}'.format(pathSubmit=pathSubmit))
    print('+------------------------------+')
    print(submit)


def calculator(pathsInput, SM1, SM2, **kwargs):

    ############################# kwargs #############################

    if 'normalizationSM' in kwargs:
        normalizationSM = kwargs['normalizationSM']

    else: normalizationSM = 1
    
    ##################################################################

    for path in pathsInput:

        if 'pathOutput' in kwargs:
            pathOutput = kwargs['pathOutput']

        else:
            pathOutputDirectory = os.path.dirname(path)

        H1H2, H1H1, H2H2 = TRSM.ppXNPSM_massfree(path, 'mH1', 'mH2', 'mH3',  SM1, SM2,  normalizationSM=1)
        modelParams = pandas.read_table(path, index_col=0)

        calculationsDict = {}
        
        calculationsDict['mH1'] = H1H2[0]
        calculationsDict['mH2'] = H1H2[1]
        calculationsDict['mH3'] = H1H2[2]

        calculationsDict['thetahS'] = modelParams['thetahS']
        calculationsDict['thetahX'] = modelParams['thetahX']
        calculationsDict['thetaSX'] = modelParams['thetaSX']
        calculationsDict['vs'] = modelParams['vs']
        calculationsDict['vx'] = modelParams['vx']
        
        calculationsDict[f'pp_X_H1H2_{SM1}{SM2}'] = H1H2[3]
        calculationsDict[f'pp_X_H1_{SM1}_H2_{SM2}'] = H1H2[4] 
        calculationsDict[f'pp_X_H1_{SM2}_H2_{SM1}'] = H1H2[5]

        calculationsDict[f'pp_X_H1H1_{SM1}{SM2}'] = H1H1[3]
        calculationsDict[f'pp_X_H2H2_{SM1}{SM2}'] = H2H2[3]

        pathOutput = os.path.join(pathOutputDirectory, f'{os.path.basename(pathOutputDirectory)}_calculation.tsv')

        df = pandas.DataFrame(data=calculationsDict)
        df.to_csv(pathOutput, sep="\t")

        


        
        
        
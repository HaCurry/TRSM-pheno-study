import pandas
import numpy as np

import os
# REMOVE THESE COMMENTED LINES
# from os import makedirs
# from os.path import dirname
# from os.path import join
from itertools import product
from glob import glob
from json import load

from helpScannerS import functions as TRSM
from helpScannerS import parameterData


def checkCreatorNew(locOutputData, configDict, **kwargs):

    ############################# kwargs #############################

    if 'modelParams' in kwargs:
        modelParams = kwargs['modelParams']

    # default TRSM
    else: modelParams = ['mH1', 'mH2', 'mH3', 'thetahS', 'thetahX', 'thetaSX', 'vs', 'vx']

    if 'forcePoints' in kwargs:
        forcePoints = kwargs['forcePoints']

    else: pass

    # OBS: additional kwargs can be found below

    ##################################################################

    configTuples = [(param + '_lb', param + '_ub', param) for param in modelParams]

    linspaceDict = {}

    for (param_lb, param_ub, param) in configTuples:
        
        if param + 'Points' in configDict:
            linspaceDict[param] = np.linspace(configDict[param_lb], configDict[param_ub], configDict[param + 'Points'])

        elif abs(configDict[param_lb] - configDict[param_ub]) < 10**(-8):
            linspaceDict[param] = np.linspace(configDict[param_lb], configDict[param_ub], 1)

        else:
            print('No points given for model parameter ' + param + 'using default np.linspace values.')
            linspaceDict[param] = np.linspace(configDict[param_lb], configDict[param_ub])
    
    # can be used when lower bounds and upper bounds are equal and user desires
    # to save the same set of model params kwargs['forcePoint'] number of times.
    # can also be used to check if scannerS does not produce any bugs when 
    # generating the same point.
    if 'forcePoints' in kwargs:
        forceList = list(zip(*[linspaceDict[param] for param in modelParams]))
        temp = []

        for i in range(kwargs['forcePoints']):
            temp.append(forceList[0])
        
        outputTuples = temp

    # otherwise perform the cartesian product of all the lists in linspaceDict
    else:
        outputTuples = list(product(*[linspaceDict[param] for param in modelParams]))

    # some additional kwargs applied on the tuples

    ############################# kwargs #############################

    # in the case of TRSM if the user wants the constraint mH3 > (mH1 + mH2)
    if 'kineticExcluder' in kwargs:
        if kwargs['kineticExcluder'] == True:

            # the tolerance in upholding the constraint:
            # mH3 - (mH1 + mH2) > eps
            if 'kineticExcluderEps' in kwargs:
                eps = kwargs['kineticExcluderEps']

            else:
                eps = 10**(-10)

            cartProdTuplesTemp = []
            for tupleElement in outputTuples:
                if tupleElement[2] - (tupleElement[0] + tupleElement[1]) > eps:
                    cartProdTuplesTemp.append(tupleElement)

                else: continue

            outputTuples = cartProdTuplesTemp

    # in case of TRSM if the user wants the constraint mH3 > mH2 > mH1
    if 'massOrder' in kwargs:
        if kwargs['massOrder'] == True:

            # the tolerance in upholding the constraint:
            # mH3 - mH2 > eps and mH2 - mH1 > eps
            if 'massOrderEps' in kwargs:
                eps = kwargs['massOrderEps']

            else:
                eps = 10**(-10)

            cartProdTuplesTemp = []
            for tupleElement in outputTuples:

                if (tupleElement[2] - tupleElement[1] > eps and
                    tupleElement[1] - tupleElement[0] > eps):
                    cartProdTuplesTemp.append(tupleElement)

                else: continue

            outputTuples = cartProdTuplesTemp

    # Some other user defined constraint that should be applied on the tuples.
    # The tuples are ordered according to the default modelParams
    if 'filter' in kwargs:
        outputTuples = kwargs['filter'](outputTuples)

    ##################################################################

    df = pandas.DataFrame(outputTuples, columns=modelParams)
            
    df.to_csv(locOutputData, sep="\t")


def configureDirs(listModelParams, pathDir, pathDataIds, **kwargs):

    ############################# kwargs #############################

    if 'existOk' in kwargs:
        existOk = kwargs['existOk']

    else: existOk = True

    # this will create the additional directory
    # pathDir/dataId/childrenDirs
    if 'childrenDirs' in kwargs:
        childrenDirs = kwargs['childrenDirs']

    else: pass

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
    
    # create directories in the path of pathDir if it does not exist
    os.makedirs(pathDir, exist_ok=existOk)

    # clear contents of old ModelParams.txt
    open(pathDataIds, 'w').close()

    for element in listModelParams:

        # name of each directory where each set of model parameter configs are stored
        dataId = (element['extra'])['dataId']

        if 'childrenDirs' in kwargs:
            os.makedirs(pathDir + '/' + dataId + '/' + childrenDirs, exist_ok=existOk)

            # create the configuration file (grid of all parameter combinations specified by element)
            checkCreatorNew(pathDir + '/' + dataId + '/' + childrenDirs + '/' +
                            'config_' + dataId + '_' + os.path.basename(childrenDirs) + '.tsv', element,
                            **kwargs)

            # store element in a JSON file in the directory (dataId)
            parameterData.createJSON(element, pathDir + '/' + dataId + '/' + childrenDirs,
                                     'settings_' + dataId + '_' + os.path.basename(childrenDirs) + '.json')

            # store the name of the directory (dataId) in a txt file for later reference
            with open(pathDataIds, 'a') as myfile:
                myfile.write(dataId + '\n')

        else:
            os.makedirs(pathDir + '/' + dataId, exist_ok=existOk)

            # create the configuration file (grid of all parameter combinations specified by element)
            checkCreatorNew(pathDir + '/' + dataId + '/' + 'config_' + dataId + '.tsv', element,
                            **kwargs)

            # store element in a JSON file in the directory (dataId)
            parameterData.createJSON(element, pathDir + '/' + dataId, 'settings_' + dataId + '.json')

            # store the name of the directory (dataId) in a txt file for later reference
            with open(pathDataIds, 'a') as myfile:
                myfile.write(dataId + '\n')


def condorScriptCreator(pathOutputDirs, pathExecutable, pathSubmit, pathDataIds, **kwargs):

    ############################# kwargs #############################

    if 'pathScannerS' in kwargs:
        pathScannerS = kwargs['pathScannerS']

    else: 
        pathScannerS = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken'

    if 'JobFlavour' in kwargs:
        JobFlavour = kwargs['JobFlavour']
        
    else:
        JobFlavour = 'testmatch'

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
    executable = (f'''#!/bin/bash
# condor executable

echo "trying to run scannerS on HTcondor..."

# default values
# path to where all the directories with config files reside
pathOutputDirs={pathOutputDirs}
# path to ScannerS executable
pathScannerS=/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken

# for debugging purposes except -i which specifies the specific dataId
# from https://www.redhat.com/sysadmin/arguments-options-bash-scripts
while getopts ":o:i:s:" option; do
  case $option in
    o) # starting directory path
      pathOutputDirs=$OPTARG;;
    i) # ouput directory path
      dataId=$OPTARG;;
    s) # scannerS executable path
      pathScannerS=$OPTARG;;
    \?) # Invalid option
      echo "Error: Invalid option"
      exit;;
  esac
done

# condor needs to give path to output directory
# from https://unix.stackexchange.com/a/621007/590852
: ${{dataId:?Missing -i, please specify dataId}}

# cd into pathOutputDirs/dataId
echo "Entering ${{pathOutputDirs}}/${{dataId}}"
cd ${{pathOutputDirs}}/${{dataId}}

# execute ScannerS TRSM executable
${{pathScannerS}} ${{pathOutputDirs}}/${{dataId}}/output_${{dataId}}.tsv check ${{pathOutputDirs}}/${{dataId}}/config_${{dataId}}.tsv
echo "Finished job in ${{pathOutputDirs}}/${{dataId}}"''')

    with open(pathExecutable, 'w') as executableFile:
        executableFile.write(executable)

    # create submit file for condor
    submit = f'''# sleep.sub -- simple sleep job
executable              = {pathExecutable}
getenv                  = True
log                     = $(dataId).$(ClusterId).$(ProcId).scannerS.log
output                  = $(dataId).$(ClusterId).$(ProcId).scannerS.out
error                   = $(dataId).$(ClusterId).$(ProcId).scannerS.err
arguments               = -i $(dataId) -s {pathScannerS}
# longlunch = 2 hrs
+JobFlavour             = \"{JobFlavour}\"
queue dataId from {pathDataIds}'''

    with open(pathSubmit, 'w') as submitFile:
        submitFile.write(submit)

    print(f'creating script {pathExecutable}')
    print('+------------------------------+')
    print(executable)
    print('\n')
    print(f'creating script {pathSubmit}')
    print('+------------------------------+')
    print(submit)


def calculator(pathsInput, SM1, SM2, **kwargs):

    ############################# kwargs #############################

    if 'normalizationSM' in kwargs:
        normalizationSM = kwargs['normalizationSM']

    else: normalizationSM = 1
    
    ##################################################################

    loadingBar = len(pathsInput)
    loadingStep = 0

    for path in pathsInput:
        
        # Fix this if statement, pathOutput and pathOutpudDirectory should be the same...
        if 'pathOutput' in kwargs:
            pathOutput = kwargs['pathOutput']

        else:
            pathOutputDirectory = os.path.dirname(path)
        
        print(f'Calculating: {100 * loadingStep/loadingBar:.0f} %', end='\r', flush=True)
        loadingStep = loadingStep + 1

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
    
    print(f'Calculations finished: 100 %')


def maxCompiler(pathsInput, pathOutput, *keys, **kwargs):

    ############################# kwargs #############################

    # if user wants other model parameters (or some other quantity
    # found in the input files from pathsInput). must be given as a list.
    if 'modelParams' in kwargs:
        modelParams = kwargs['modelParams']

    # default model parameters
    else: modelParams = ['mH1', 'mH2', 'mH3', 'thetahS', 'thetahX', 'thetaSX', 'vs', 'vx']

    # if user wants to compare with observed limits (e.g. Atlas limits)
    if 'limitsKey' in kwargs:
        limitsKey = kwargs['limitsKey']

        if 'limitsGlob' in kwargs:
            limitsGlob = kwargs['limitsGlob']

        else: limitsGlob = 'settings_*'

    else: pass


    ##################################################################
    
    # REORDER HTESE SO IT LOOKS BETTER IN TH DF!
    # maximal cross sections will be saved here and modelParams
    dictOutput = {}

    for param in modelParams:
        dictOutput[param] = []

    if 'limitsKey' in kwargs:
        dictOutput[kwargs['limitsKey']] = []

    for key in keys:
        dictOutput[key] = []

    # if more keys are given a sum key is added where the maximum
    # of the sum of the quantities from the keys are instead inserted
    if len(keys) > 1:
        dictOutput['sum'] = []

    loadingBar = len(pathsInput) 
    loadingStep = 0 

    for path in pathsInput:
        
        # progress bar        
        print(f'loading {pathOutput}: {100 * loadingStep/loadingBar:.0f} %', end='\r', flush=True)
        loadingStep = loadingStep + 1

        df = pandas.read_table(path)

        # if len(key) > 1, the maximum of the sum of the quantities
        # specified by the keys are considered
        sumKeyArray = np.zeros(len(df))
        for key in keys:
            sumKeyArray = sumKeyArray + np.array(df[key])

        # save index to store other keys and modelParam quantities
        # individually
        indexMax = np.nanargmax(sumKeyArray)

        if len(keys) > 1:
            dictOutput['sum'].append(sumKeyArray[indexMax])

        else:
            pass

        for key in keys:
            dictOutput[key].append(np.array(df[key])[indexMax])

        for param in modelParams:
            dictOutput[param].append(np.array(df[param])[indexMax])

        # append limits (e.g. Atlas Observed limits) to dictOutput 
        if 'limitsKey' in kwargs:
            limitsKey = kwargs['limitsKey']

            # limits are specified in the same directory as the input files
            dirContainingLimit = os.path.dirname(path)

            # find the path to the limits, default is path/limitsGlob where
            # limitsGlob is settings_* (JSON file)
            pathLimit = glob(os.path.join(dirContainingLimit, limitsGlob))
            
            # glob returns a list with paths. There should only be one such file with limits 
            # in the directory
            if len(pathLimit) > 1: raise Exception(f'Too many settings files in {path} to pick from')            
            with open(pathLimit[0]) as p:
                contentsJSON = load(p)

            # append limits to dictOutput
            dictOutput[limitsKey].append((contentsJSON['extra'])[limitsKey])

    print(f'Finished loading {pathOutput}: 100 %\n')

    df = pandas.DataFrame(data=dictOutput)

    df.to_csv(pathOutput, sep="\t")

        
        

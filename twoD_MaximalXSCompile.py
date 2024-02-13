
#-*- coding: utf-8 -*-
import csv
import pandas

import numpy as np
# from scipy.interpolate import CubicSpline

# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import scipy.interpolate
# mpl.rcParams.update(mpl.rcParamsDefault)

# import subprocess
# import configparser
from os import makedirs
# import datetime
# import multiprocessing
# import sys
# import json
# import copy
# import glob
# from pathlib import Path
# from itertools import repeat

import functions as TRSM
import parameterData
import twoDPlotter as twoDPlot


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

    makedirs(pathDir, exist_ok=existOk)
    mainModParFile = 'dataIds.txt'
    pathMainModParFile = pathDir + '/' + mainModParFile

    # clear contents of old ModelParams.txt
    open(pathMainModParFile, 'w').close()

    for element in listModelParams:

        # name of each directory where each set of model parameter configs are stored
        dataId = (element['extra'])['dataId']

        makedirs(pathDir + '/' + dataId, exist_ok=existOk)

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


if __name__ == '__main__':

    # testing within 09-0.04
    listModelParams = [(90, 125.09, 450), (100, 125.09, 550), (90, 125.09, 500), (125.09, 140, 500), (100, 125.09, 500)]
    listConfigParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
                         'mH2_lb': mH2, 'mH2_ub': mH2,
                         'mH3_lb': mH3, 'mH3_ub': mH3,
                         'thetahS_lb': -np.pi/2, 'thetahS_ub': np.pi/2, 'thetahSPoints':3,
                         'thetahX_lb': -np.pi/2, 'thetahX_ub': np.pi/2, 'thetahXPoints':3,
                         'thetaSX_lb': -np.pi/2, 'thetaSX_ub': np.pi/2, 'thetaSXPoints':3,
                         'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 3,
                         'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 3,
                         'extra': {'dataId': '{a}-{b}-{c}'.format(a=mH1, b=mH2, c=mH3)}, 'ScannerSmode': 'check'} for (mH1, mH2, mH3) in listModelParams]

    configureDirs(listConfigParams, 'scriptTesting2')
    condorScriptCreator('scriptTesting2/scannerS.sh', 'scriptTesting2/scannerS.sub')
              
    df = pandas.read_table('robens_bbgamgamXS.txt', sep='\s+', usecols=[0,1,2,3], names=['index', 'ms', 'mx', 'xs'])
    df.to_csv('robens_bbgamgamXS.tsv', sep='\t', index=False)
    print(df)

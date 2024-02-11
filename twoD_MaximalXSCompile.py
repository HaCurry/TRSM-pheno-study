
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

if __name__ == '__main__':

    dictPoint = [{'mHa_lb': 90,        'mHa_ub': 90,
                  'mHb_lb': 125.09,    'mHb_ub': 125.09,
                  'mHc_lb': 300,       'mHc_ub': 300,
                  'ths_lb': -np.pi/2,  'ths_ub': np.pi/2,
                  'thx_lb': -np.pi/2,  'thx_ub': np.pi/2,
                  'tsx_lb': -np.pi/2,  'tsx_ub': np.pi/2,
                  'vs_lb': 1,          'vs_ub': 1000,
                  'vx_lb': 1,          'vx_ub': 1000,
                  'extra': {'dataId': 'S{a}-X{b}'.format(a=90, b=300)}}]
    
    # parameterData.parameterMain(dictPoint, 'test', 'scan', points=10, modelParam='Nofree')
    # parameterData.dataCalculatorMain('test', 'testCalc', '/**/settings_*.json', generateH1H2=True,
    #                                  SM1='bb', SM2='gamgam')

    
    # twoDPlot.maxCompiler('/**/settingsCalc_Nofree*.json', 'testCalc', 'testMax2.tsv',
    #                      includeObsLim=False)
    
    # df = pandas.read_table('testCalc/S90-X300/Nofree/outputppXNPSM_H1H2_Nofree_S90-X300.tsv')
    # print(df)

    test = {'mH1_lb': 90,        'mH1_ub': 90,
            'mH2_lb': 125.09,    'mH2_ub': 125.09,
            'mH3_lb': 300,       'mH3_ub': 300,
            'thetahS_lb': -np.pi/2, 'thetahS_ub': np.pi/2, 'thetahSPoints':3,
            'thetahX_lb': -np.pi/2, 'thetahX_ub': np.pi/2, 'thetahXPoints':3,
            'thetaSX_lb': -np.pi/2, 'thetaSX_ub': np.pi/2, 'thetaSXPoints':3,
            'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 3,
            'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 3, } 

    # os.makedirs()

    # twoDPlot.checkCreatorNew('checkcreatorNewtest.tsv', test, massOrdering=True)

    # df = pandas.read_table('checkcreatorNewtest.tsv')
    # print(df)

#40-200  70-400  90-300  90-450


# #    Initial testing
#    listModelParams = [(90, 125.09, 450), (90, 125.09, 300), (40, 125.09, 200), (70, 125.09, 400)]
#    listConfigParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
#                         'mH2_lb': mH2, 'mH2_ub': mH2,
#                         'mH3_lb': mH3, 'mH3_ub': mH3,
#                         'thetahS_lb': -np.pi/2, 'thetahS_ub': np.pi/2, 'thetahSPoints':10,
#                         'thetahX_lb': -np.pi/2, 'thetahX_ub': np.pi/2, 'thetahXPoints':10,
#                         'thetaSX_lb': -np.pi/2, 'thetaSX_ub': np.pi/2, 'thetaSXPoints':10,
#                         'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 10,
#                         'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 10, 
#                         'extra': {'dataId': '{a}-{b}-{c}'.format(a=mH1, b=mH2, c=mH3)} } for (mH1, mH2, mH3) in listModelParams]
#
#    mainDirectory = 'testMax'

 #    testing within 09-0.04
    listModelParams = [(90, 125.09, 450), (100, 125.09, 550), (90, 125.09, 500), (125.09, 140, 500), (100, 125.09, 500)]
    listConfigParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
                         'mH2_lb': mH2, 'mH2_ub': mH2,
                         'mH3_lb': mH3, 'mH3_ub': mH3,
                         'thetahS_lb': -np.pi/2, 'thetahS_ub': np.pi/2, 'thetahSPoints':3,
                         'thetahX_lb': -np.pi/2, 'thetahX_ub': np.pi/2, 'thetahXPoints':3,
                         'thetaSX_lb': -np.pi/2, 'thetaSX_ub': np.pi/2, 'thetaSXPoints':3,
                         'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 3,
                         'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 3,
                         'extra': {'dataId': '{a}-{b}-{c}'.format(a=mH1, b=mH2, c=mH3)} } for (mH1, mH2, mH3) in listModelParams]

    mainDirectory = 'testMaxTryingToFindNaN'


    mainModParFile = 'ModelParams.txt'
    exist_ok = True

    pathMainModParFile = mainDirectory + '/' + mainModParFile

    try:
        # clear contents of old ModelParams.txt
        open(pathMainModParFile, 'w').close()

    except FileNotFoundError:
        print('file not found, not clearing any file')

    for element in listConfigParams:

        makedirs(mainDirectory + '/' + (element['extra'])['dataId'], exist_ok=exist_ok)
        twoDPlot.checkCreatorNew(mainDirectory + '/' + (element['extra'])['dataId'] + '/' + (element['extra'])['dataId'] + '_config.tsv', element)

        with open(pathMainModParFile, 'a') as myfile:
            myfile.write((element['extra'])['dataId'] + '\n')


#     def condorConfigure(listModelParams, pathDir, pathScannerS, **kwargs):

#         if 'existOk' in kwargs:
#             existOk = kwargs['existOk']

#         else: existOk = True

#         if 'condorScripts' in kwargs:
            
        
#         # checks so that all ranges of the model parameters are given
#         for element in listModelParams:
#             if \
#             'mH1_lb' in element and 'mH2_lb' in element and 'mH3_lb' in element and \
#             'mH1_ub' in element and 'mH2_ub' in element and 'mH3_ub' in element and \
#             'thetahS_lb' in element and 'thetahX_lb' in element and 'thetaSX_lb' in element and \
#             'thetahS_ub' in element and 'thetahX_ub' in element and 'thetaSX_ub' in element and \
#             'vs_lb' in element and 'vx_lb' in element \
#             'vs_ub' in element and 'vx_ub' in element:
#                 pass
#             else: raise Exception('The ranges of all model parameters are not defined') 

#         mainModParFile = 'ModelParamsId.txt'
#         pathMainModParFile = mainDirectory + '/' + mainModParFile

#         try:
#             # clear contents of old ModelParams.txt
#             open(pathMainModParFile, 'w').close()

#         except FileNotFoundError:
#             print('file not found, not clearing ModelParamsId.txt {a}'.format(a=pathDir))

#         for element in listModelParams:

#             # name of each directory where each set of model parameter configs are stored
#             dataId = (element['extra'])['dataId']
            
#             makedirs(mainDirectory + '/' + dataId, exist_ok=existOk)

#             # create the configuration file (grid of all parameter combinations specified by element)
#             twoDPlot.checkCreatorNew(mainDirectory + '/' + dataId + '/' + 'config_' + dataId + '.tsv', element)

#             # store element in a JSON file in the directory (dataId)
#             parameterData.createJSON(element, pathDir + '/' + dataId, 'Settings')

#             # store the name of the directory (dataId) in a txt file for later reference
#             with open(pathMainModParFile, 'a') as myfile:
#                 myfile.write(dataId + '\n')

#             # create executable and submit file for condor if condorScripts == True
#             if condorScripts == True:
#                 executable = "#!/bin/bash\n\
#                               echo \"trying to run scannerS on HTcondor...\"\n\
#                               # cd into directory
#                               cd {pathDir}/$1\n\
#                               # run the scannerS TRSM executable with absolute paths to everything
#                               {pathScannerS}\
#                               # output file
#                               {pathDir}/$1/$1_output.tsv \
#                               # input file
#                               check {pathDir}/$1/$1_config.tsv \
#                               echo \"Finishing job in $1\"".format(pathDir=pathDir, pathScannerS=pathScannerS)
# # "#!/bin/bash \
# # echo \"trying to run scannerS on HTcondor...\"\n\
# # # cd into directory
# # cd /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testMax0.9-0.04/$1\n\
# # # run the scannerS TRSM executable with absolute paths to everything
# # /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken \
# # # output file
# # /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testMax0.9-0.04/$1/$1_output.tsv \
# # # input file
# # check /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testMax0.9-0.04/$1/$1_config.tsv \
# # echo \"$1\""
                
                

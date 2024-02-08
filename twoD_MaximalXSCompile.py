
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
            'thetahS_lb': -np.pi/2, 'thetahS_ub': np.pi/2, 'thetahSPoints':2,
            'thetahX_lb': -np.pi/2, 'thetahX_ub': np.pi/2, 'thetahXPoints':2,
            'thetaSX_lb': -np.pi/2, 'thetaSX_ub': np.pi/2, 'thetaSXPoints':2,
            'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 2,
            'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 2, } 

    # os.makedirs()

    # twoDPlot.checkCreatorNew('checkcreatorNewtest.tsv', test, massOrdering=True)

    # df = pandas.read_table('checkcreatorNewtest.tsv')
    # print(df)



    listModelParams = [(90, 125.09, 300), (40, 125.09, 200), (70, 125.09, 400)]
    listConfigParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
                         'mH2_lb': mH2, 'mH2_ub': mH2,
                         'mH3_lb': mH3, 'mH3_ub': mH3,
                         'thetahS_lb': -np.pi/2, 'thetahS_ub': np.pi/2, 'thetahSPoints':2,
                         'thetahX_lb': -np.pi/2, 'thetahX_ub': np.pi/2, 'thetahXPoints':2,
                         'thetaSX_lb': -np.pi/2, 'thetaSX_ub': np.pi/2, 'thetaSXPoints':2,
                         'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 2,
                         'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 2, 
                         'extra': {'dataId': '{a}-{b}'.format(a=mH1, b=mH3)} } for (mH1, mH2, mH3) in listModelParams]

    mainDirectory = 'testMax'
    mainModParFile = 'ModelParams.txt'
    exist_ok = True

    for element in listConfigParams:

        makedirs(mainDirectory + '/' + (element['extra'])['dataId'], exist_ok=exist_ok)
        twoDPlot.checkCreatorNew(mainDirectory + '/' + (element['extra'])['dataId'] + '/' + (element['extra'])['dataId'] + '_config.tsv', element)

        with open(mainDirectory + '/' + mainModParFile, 'a') as myfile:
            myfile.write((element['extra'])['dataId'] + '\n')


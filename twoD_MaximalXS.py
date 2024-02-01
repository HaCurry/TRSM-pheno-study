
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
# import os
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
    
    parameterData.parameterMain(dictPoint, 'test', 'scan', points=10, modelParam='Nofree')
    parameterData.dataCalculatorMain('test', 'testCalc', '/**/settings_*.json', generateH1H2=True,
                                     SM1='bb', SM2='gamgam')

    
    twoDPlot.maxCompiler('/**/settingsCalc_Nofree*.json', 'testCalc', 'testMax2.tsv',
                         includeObsLim=False)
    
    # df = pandas.read_table('testCalc/S90-X300/Nofree/outputppXNPSM_H1H2_Nofree_S90-X300.tsv')
    # print(df)

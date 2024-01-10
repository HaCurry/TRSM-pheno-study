#-*- coding: utf-8 -*-
import csv
import pandas

import numpy as np
from scipy.interpolate import CubicSpline

import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.interpolate
mpl.rcParams.update(mpl.rcParamsDefault)

import subprocess
import configparser
import os
import datetime
import multiprocessing
import sys
import json
import copy
import glob
from pathlib import Path
from itertools import repeat

import functions as TRSM
import parameterData

if __name__ == '__main__':

    dfBP2_r1 = pandas.read_table('ownGridRegion1BP2.tsv', index_col=0)

    ms_BP2 = dfBP2_r1['ms']
    mx_BP2 = dfBP2_r1['mx']

    BP2_dictPointlistOwnGridRegion1 = [{
                               'mHa_lb': ms_BP2[i], 'mHa_ub': ms_BP2[i],
                               'mHb_lb': 125.09,    'mHb_ub': 125.09,
                               'mHc_lb': mx_BP2[i], 'mHc_ub': mx_BP2[i], 
                               'extra': {
                                         'dataId': 'S' + str(ms_BP2[i]) + '-' + 'X' + str(mx_BP2[i]) 
                                        } 
                              } for i in  range(len(ms_BP2))]

    del ms_BP2, mx_BP2

    dfBP2_r2 = pandas.read_table('ownGridRegion2BP2.tsv', index_col=0)

    ms_BP2 = dfBP2_r2['ms']
    mx_BP2 = dfBP2_r2['mx']

    BP2_dictPointlistOwnGridRegion2 = [{
                               'mHa_lb': ms_BP2[i], 'mHa_ub': ms_BP2[i],
                               'mHb_lb': 125.09,    'mHb_ub': 125.09,
                               'mHc_lb': mx_BP2[i], 'mHc_ub': mx_BP2[i], 
                               'extra': {
                                         'dataId': 'S' + str(ms_BP2[i]) + '-' + 'X' + str(mx_BP2[i]) 
                                        } 
                              } for i in  range(len(ms_BP2))]

    del ms_BP2, mx_BP2

    dfBP3_r1 = pandas.read_table('ownGridRegion1BP3.tsv', index_col=0)

    ms_BP3 = dfBP3_r1['ms']
    mx_BP3 = dfBP3_r1['mx']

    BP3_dictPointlistOwnGridRegion1 = [{
                               'mHa_lb': 125.09,    'mHa_ub': 125.09,
                               'mHb_lb': ms_BP3[i], 'mHb_ub': ms_BP3[i],
                               'mHc_lb': mx_BP3[i], 'mHc_ub': mx_BP3[i], 
                               'extra': {
                                         'dataId': 'S' + str(ms_BP3[i]) + '-' + 'X' + str(mx_BP3[i]) 
                                        } 
                              } for i in  range(len(ms_BP3))]
    
    del ms_BP3, mx_BP3

    dfBP3_r2 = pandas.read_table('ownGridRegion2BP3.tsv', index_col=0)

    ms_BP3 = dfBP3_r2['ms']
    mx_BP3 = dfBP3_r2['mx']

    BP3_dictPointlistOwnGridRegion2 = [{
                               'mHa_lb': 125.09,    'mHa_ub': 125.09,
                               'mHb_lb': ms_BP3[i], 'mHb_ub': ms_BP3[i],
                               'mHc_lb': mx_BP3[i], 'mHc_ub': mx_BP3[i], 
                               'extra': {
                                         'dataId': 'S' + str(ms_BP3[i]) + '-' + 'X' + str(mx_BP3[i]) 
                                        } 
                              } for i in  range(len(ms_BP3))]
    
    del ms_BP3, mx_BP3

    
    # 1D parameter plot for own grid

    # parameterData.mProcParameterMain(BP2_dictPointlistOwnGridRegion1,  'BP2', 'ownGridRegion1BP2_check_prel', 50, 'check')
    # parameterData.mProcCalculatorMain('ownGridRegion1BP2_check_prel', 'calc_ownGridRegion1BP2_check_prel_Mproc', '/**/settings_*.json', 
    #                 SM1='bb', SM2='gamgam', generateH1H2=True)

    # parameterData.mProcParameterMain(BP2_dictPointlistOwnGridRegion2,  'BP2', 'ownGridRegion2BP2_check_prel', 50, 'check')
    # parameterData.mProcCalculatorMain('ownGridRegion2BP2_check_prel', 'calc_ownGridRegion2BP2_check_prel_Mproc', '/**/settings_*.json', 
    #                 SM1='bb', SM2='gamgam', generateH1H2=True)

    # parameterData.mProcParameterMain(BP3_dictPointlistOwnGridRegion1,  'BP3', 'ownGridRegion1BP3_check_prel', 50, 'check')
    # parameterData.mProcCalculatorMain('ownGridRegion1BP3_check_prel', 'calc_ownGridRegion1BP3_check_prel_Mproc', '/**/settings_*.json', 
    #                 SM1='bb', SM2='gamgam', generateH1H2=True)

    parameterData.mProcParameterMain(BP3_dictPointlistOwnGridRegion2,  'BP3', 'ownGridRegion2BP3_check_prel', 50, 'check')
    parameterData.mProcCalculatorMain('ownGridRegion2BP3_check_prel', 'calc_ownGridRegion2BP3_check_prel_Mproc', '/**/settings_*.json', 
                    SM1='bb', SM2='gamgam', generateH1H2=True)


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
    # BP2 Observed limits
    df2 = pandas.read_table('Atlas2023Limits_BP2.tsv', index_col = 0)

    ms_BP2 = df2['ms']
    mx_BP2 = df2['mx']
    limit_obs_BP2 = df2['limit_obs']

    BP2_dictPointlistAtlas = [{
                               'mHa_lb': ms_BP2[i], 'mHa_ub': ms_BP2[i],
                               'mHb_lb': 125.09,    'mHb_ub': 125.09,
                               'mHc_lb': mx_BP2[i], 'mHc_ub': mx_BP2[i],
                               'extra': {'ObservedLimit': 10**(-3) * limit_obs_BP2[i], 'dataId': 'S' + str(ms_BP2[i]) + '-' + 'X' + str(mx_BP2[i]) } } for i in  range(len(ms_BP2))]


    # BP3 Observed limits
    df3 = pandas.read_table('Atlas2023Limits_BP3.tsv', index_col = 0)
     
    ms_BP3 = df3['ms']
    mx_BP3 = df3['mx']
    limit_obs_BP3 = df3['limit_obs']

    BP3_dictPointlistAtlas = [{
                               'mHa_lb': 125.09,    'mHa_ub': 125.09,
                               'mHb_lb': ms_BP3[i], 'mHb_ub': ms_BP3[i],
                               'mHc_lb': mx_BP3[i], 'mHc_ub': mx_BP3[i], 
                               'extra': {
                                         'ObservedLimit': 10**(-3) * limit_obs_BP3[i], 
                                         'dataId': 'S' + str(ms_BP3[i]) + '-' + 'X' + str(mx_BP3[i]) 
                                        } 
                              } for i in  range(len(ms_BP3))]


    # BP5 Observed limits
    df3 = pandas.read_table('Atlas2023Limits_BP5.tsv', index_col = 0)
     
    ms_BP5 = df3['ms']
    mx_BP5 = df3['mx']
    limit_obs_BP5 = df3['limit_obs']

    BP5_dictPointlistAtlas = [{
                               'mHa_lb': ms_BP5[i], 'mHa_ub': ms_BP5[i],
                               'mHb_lb': 125.09,    'mHb_ub': 125.09,
                               'mHc_lb': mx_BP5[i], 'mHc_ub': mx_BP5[i], 
                               'extra': {
                                         'ObservedLimit': 10**(-3) * limit_obs_BP5[i], 
                                         'dataId': 'S' + str(ms_BP5[i]) + '-' + 'X' + str(mx_BP5[i]) 
                                        } 
                              } for i in  range(len(ms_BP5))]


    # BP6 Observed limits
    df3 = pandas.read_table('Atlas2023Limits_BP6.tsv', index_col = 0)
     
    ms_BP6 = df3['ms']
    mx_BP6 = df3['mx']
    limit_obs_BP6 = df3['limit_obs']

    BP6_dictPointlistAtlas = [{
                               'mHa_lb': 125.09,    'mHa_ub': 125.09,
                               'mHb_lb': ms_BP6[i], 'mHb_ub': ms_BP6[i],
                               'mHc_lb': mx_BP6[i], 'mHc_ub': mx_BP6[i], 
                               'extra': {
                                         'ObservedLimit': 10**(-3) * limit_obs_BP6[i], 
                                         'dataId': 'S' + str(ms_BP6[i]) + '-' + 'X' + str(mx_BP6[i]) 
                                        } 
                              } for i in  range(len(ms_BP6))]


    # BP2 settings: 
    programParametersDictBP2 = { 
                                "mHa_lb": 80, "mHa_ub": 80, "mHb_lb": 125.09, "mHb_ub": 125.09, "mHc_lb": 375, "mHc_ub": 375, 
                                "ths_lb": 1.352, "ths_ub": 1.352, "thx_lb": 2, "thx_ub": 2, "tsx_lb": -0.407, "tsx_ub": -0.407, 
                                "vs_lb": 120, "vs_ub": 120, "vx_lb": 890, "vx_ub": 890 
                                }

    # BP3 settings:
    programParametersDictBP3 = {'bfb': 'apply', 'uni': 'apply', 'stu': 'apply', 'Higgs': 'apply',
                                "mHa_lb": 125.09, "mHa_ub": 125.09, "mHb_lb": 150, "mHb_ub": 150, "mHc_lb": 300, "mHc_ub": 300, 
                                "ths_lb": -0.129, "ths_ub": -0.129, "thx_lb": 0.226, "thx_ub": 0.226, "tsx_lb": -0.899, "tsx_ub": -0.899, 
                                "vs_lb": 140, "vs_ub": 140, "vx_lb": 100, "vx_ub": 100, 'extra': {'dataId': 'test'}
                                }


    # line below deprecated
    # mProcParameterMain(BP2_dictPointlistAtlas, 'BP2', 'AtlasBP2_check_prel', 50, 'check')

    # line below deprecated
    # dataCalculatorMain('AtlasBP2_check_prel', 'calc_AtlasBP2_check_prel', '/**/settings_*.json', 
                       # SM1='bb', SM2='gamgam', generateH1H2=True)

    # line below deprecated
    # mProcParameterMain(BP3_dictPointlistAtlas, 'BP3', 'AtlasBP3_check_prel', 50, 'check')

    # line below deprecated
    # dataCalculatorMain('AtlasBP3_check_prel', 'calc_AtlasBP3_check_prel', '/**/settings_*.json', 
    #                  SM1='bb', SM2='gamgam', generateH1H2=True)

    # line below deprecated
    # mProcParameterMain(BP5_dictPointlistAtlas, 'BP5', 'AtlasBP5_check_prel', 50, 'check')

    # line below deprecated
    # dataCalculatorMain('AtlasBP5_check_prel', 'calc_AtlasBP5_check_prel', '/**/settings_*.json', 
    #                  SM1='bb', SM2='gamgam', generateH1H2=True)

    # line below deprecated
    # mProcParameterMain(BP6_dictPointlistAtlas, 'BP6', 'AtlasBP6_check_prel', 50, 'check')

    # line below deprecated
    # dataCalculatorMain('AtlasBP6_check_prel', 'calc_AtlasBP6_check_prel', '/**/settings_*.json', 
                     # SM1='bb', SM2='gamgam', generateH1H2=True)


    # 1D parameter plot for Atlas observed limits (This should be depraceted because this is also contraints enabled)
    # (if constraints are not specified they are automatically enabled)
    
    # parameterData.mProcParameterMain(BP2_dictPointlistAtlas, 'BP2', 'AtlasBP2_check_prel', 50, 'check')
    # parameterData.mProcCalculatorMain('AtlasBP2_check_prel', 'calc_AtlasBP2_check_prel_Mproc', '/**/settings_*.json', 
    #                 SM1='bb', SM2='gamgam', generateH1H2=True)

    # parameterData.mProcParameterMain(BP3_dictPointlistAtlas, 'BP3', 'AtlasBP3_check_prel', 50, 'check')
    # parameterData.mProcCalculatorMain('AtlasBP3_check_prel', 'calc_AtlasBP3_check_prel_Mproc', '/**/settings_*.json', 
    #                 SM1='bb', SM2='gamgam', generateH1H2=True)

    # parameterData.mProcParameterMain(BP5_dictPointlistAtlas, 'BP5', 'AtlasBP5_check_prel', 50, 'check')
    # parameterData.mProcCalculatorMain('AtlasBP5_check_prel', 'calc_AtlasBP5_check_prel_Mproc', '/**/settings_*.json', 
    #                 SM1='bb', SM2='gamgam', generateH1H2=True)

    # parameterData.mProcParameterMain(BP6_dictPointlistAtlas, 'BP6', 'AtlasBP6_check_prel', 50, 'check')
    # parameterData.mProcCalculatorMain('AtlasBP6_check_prel', 'calc_AtlasBP6_check_prel_Mproc', '/**/settings_*.json', 
    #                 SM1='bb', SM2='gamgam', generateH1H2=True)


    # 1D parameter plot for Atlas observed limits with constraints enabled

    name = input('Are you sure you want to run oneD_AtlasLimits.py? Otherwise press ctrl + z to quit')

    parameterData.mProcParameterMain(BP2_dictPointlistAtlas, 'BP2', 'AtlasBP2_check_prel_constraint', 50, 'check')
    parameterData.mProcCalculatorMain('AtlasBP2_check_prel_constraint', 'calc_AtlasBP2_check_prel_Mproc_constraint', '/**/settings_*.json', 
                    SM1='bb', SM2='gamgam', generateH1H2=True)

    parameterData.mProcParameterMain(BP3_dictPointlistAtlas, 'BP3', 'AtlasBP3_check_prel_constraint', 50, 'check')
    parameterData.mProcCalculatorMain('AtlasBP3_check_prel_constraint', 'calc_AtlasBP3_check_prel_Mproc_constraint', '/**/settings_*.json', 
                    SM1='bb', SM2='gamgam', generateH1H2=True)

    parameterData.mProcParameterMain(BP5_dictPointlistAtlas, 'BP5', 'AtlasBP5_check_prel_constraint', 50, 'check')
    parameterData.mProcCalculatorMain('AtlasBP5_check_prel_constraint', 'calc_AtlasBP5_check_prel_Mproc_constraint', '/**/settings_*.json', 
                    SM1='bb', SM2='gamgam', generateH1H2=True)

    parameterData.mProcParameterMain(BP6_dictPointlistAtlas, 'BP6', 'AtlasBP6_check_prel_constraint', 50, 'check')
    parameterData.mProcCalculatorMain('AtlasBP6_check_prel_constraint', 'calc_AtlasBP6_check_prel_Mproc_constraint', '/**/settings_*.json', 
                    SM1='bb', SM2='gamgam', generateH1H2=True)


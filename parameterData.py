# -*- coding: utf-8 -*-
import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.interpolate
from scipy.interpolate import CubicSpline
mpl.rcParams.update(mpl.rcParamsDefault)
from numpy import ma
from subprocess import call
import subprocess
import configparser

#def parameterData(usr_params):

#    # create directory for storage
#    parentDir_toShell = "mS" + str(usr_params["ms"]) + "-" + "mX" + str(usr_params["mx"])
#    subprocess.run(["mkdir", parentDir_toShell])
#    
#    def preamble(usr_params):
#    
#        # parameter values used by script
#        programParametersDict = { 
#            "mHa_lb": 80, "mHa_ub": 80, "mHb_lb": 125.09, "mHb_ub": 125.09, "mHc_lb": 375, "mHc_ub": 375, 
#            "ths_lb": 1.352, "ths_ub": 1.352, "thx_lb": 1.175, "thx_ub": 1.175, "tsx_lb": -0.407, "tsx_ub": -0.407, 
#            "vs_lb": 120, "vs_ub": 120, "vx_lb": 890, "vx_ub": 890, 
#            "points": 100
#            }
#        
#        # change parameters used in script to user given masses
#        programParametersDict["mHa_lb"] = userParametersDict["ms"]
#        programParametersDict["mHa_ub"] = userParametersDict["ms"]
#        
#        programParametersDict["mHc_lb"] = userParametersDict["mx"]
#        programParametersDict["mHc_ub"] = userParametersDict["mx"]
#        
#        userParametersKeys = userParametersDict.keys()
#        
#        # additional parameters given by user inserted in programParametersDict
#        for key in userParametersKeys:
#            if key == "ms" or key == "mx":
#                continue
#            else:
#                programParametersDict[key] = userParametersDict[key]
#    
#        return programParametersDict 
#        
#    
#    # filename = parentDir_toShell
#    def vev(programParametersDict, filename):
#        
#        vevDir_toShell = parentDir + "/" + "vev_" + filename
#        subprocess.run(["mkdir", vevDir_toShell])
#        
##        createConfig_toShell = ["touch", "vev_config"]
#        
#        config = configparser.ConfigParser()
#        config['DEFAULT'] = {'bfb': 'apply',
#                             'uni': 'apply',
#                             'stu': 'apply',
#                             'Higgs': 'apply'}
#        config['scan'] = {'mHa': str(programParametersDict["mHa_lb"] + ' ' + str(programParametersDict["mHa_ub"]),
#                          'mHb': str(programParametersDict["mHb_lb"] + ' ' + str(programParametersDict["mHb_ub"]),
#                          'mHc': str(programParametersDict["mHc_lb"] + ' ' + str(programParametersDict["mHc_ub"]),
#                          
#                          't1':  str(programParametersDict["ths_lb"] + ' ' + str(programParametersDict["ths_ub"]),
#                          't2':  str(programParametersDict["thx_lb"] + ' ' + str(programParametersDict["thx_ub"]),
#                          't3':  str(programParametersDict["tsx_lb"] + ' ' + str(programParametersDict["tsx_ub"]),
#                          
#                          'vs':  str(programParametersDict["vs_lb"] + ' ' + str(programParametersDict["vs_ub"]),
#                          'vx':  str(programParametersDict["vx_lb"] + ' ' + str(programParametersDict["vx_ub"])}
#        with open(parentDir + '.ini', 'w') as configfile:
#            config.write(configfile)
#        
#    angleDir = parentDir + "/" + "angle_" + parentDir

programParametersDict = { 
            "mHa_lb": 80, "mHa_ub": 80, "mHb_lb": 125.09, "mHb_ub": 125.09, "mHc_lb": 375, "mHc_ub": 375, 
            "ths_lb": 1.352, "ths_ub": 1.352, "thx_lb": 1.175, "thx_ub": 1.175, "tsx_lb": -0.407, "tsx_ub": -0.407, 
            "vs_lb": 120, "vs_ub": 120, "vx_lb": 890, "vx_ub": 890, 
            "points": 100
            }

config = configparser.ConfigParser()
config['DEFAULT'] = {'bfb': 'apply',
                     'uni': 'apply',
                     'stu': 'apply',
                     'Higgs': 'apply'}
config['scan'] = {'mHa': str(programParametersDict["mHa_lb"]) + ' ' + str(programParametersDict["mHa_ub"]),
                  'mHb': str(programParametersDict["mHb_lb"]) + ' ' + str(programParametersDict["mHb_ub"]),
                  'mHc': str(programParametersDict["mHc_lb"]) + ' ' + str(programParametersDict["mHc_ub"]),
                  
                  't1':  str(programParametersDict["ths_lb"]) + ' ' + str(programParametersDict["ths_ub"]),
                  't2':  str(programParametersDict["thx_lb"]) + ' ' + str(programParametersDict["thx_ub"]),
                  't3':  str(programParametersDict["tsx_lb"]) + ' ' + str(programParametersDict["tsx_ub"]),
                  
                  'vs':  str(programParametersDict["vs_lb"]) + ' ' + str(programParametersDict["vs_ub"]),
                  'vx':  str(programParametersDict["vx_lb"]) + ' ' + str(programParametersDict["vx_ub"])}
with open('123-321' + '.ini', 'w') as configfile:
    config.write(configfile)









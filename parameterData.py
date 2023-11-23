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
 
def parameterData(usr_params, **kwargs):
    
    if 'points' in kwargs:
        points = kwargs['points']
        
    else:
#        print('User did not specify number of points in **kwargs. Setting points to 100')
        points = 100
 
    # create directory for storage
    dataId = 'mS' + str(usr_params['ms']) + '-' + 'mX' + str(usr_params['mx'])
    subprocess.run(['mkdir', dataId])

    def preamble(usr_params):

#        parameter values used by script
        programParametersDict = {
            'mHa_lb': 80, 'mHa_ub': 80, 'mHb_lb': 125.09, 'mHb_ub': 125.09, 'mHc_lb': 375, 'mHc_ub': 375,
            'ths_lb': 1.352, 'ths_ub': 1.352, 'thx_lb': 1.175, 'thx_ub': 1.175, 'tsx_lb': -0.407, 'tsx_ub': -0.407,
            'vs_lb': 120, 'vs_ub': 120, 'vx_lb': 890, 'vx_ub': 890,
            }
        
        # change parameters used in script to user given masses
        programParametersDict['mHa_lb'] = userParametersDict['ms']
        programParametersDict['mHa_ub'] = userParametersDict['ms']

        programParametersDict['mHc_lb'] = userParametersDict['mx']
        programParametersDict['mHc_ub'] = userParametersDict['mx']

        userParametersKeys = userParametersDict.keys()

#        additional parameters given by user inserted in programParametersDict
        for key in userParametersKeys:
            if key == 'ms' or key == 'mx':
                continue
            else:
                programParametersDict[key] = userParametersDict[key]

        return programParametersDict


def vev(programParametersDict, dataId, paramFree, points):

    paramDir = dataId + '/' + paramFree + '_' + dataId
    subprocess.run(['mkdir', paramDir])

    #        createConfig_toShell = ['touch', 'vev_config']

    config = configparser.ConfigParser()
    config['DEFAULT'] = {'bfb': 'apply',
                         'uni': 'apply',
                         'stu': 'apply',
                         'Higgs': 'apply'}
    config['scan'] = {'mHa': str(programParametersDict['mHa_lb']) + ' ' + str(programParametersDict['mHa_ub']),
                      'mHb': str(programParametersDict['mHb_lb']) + ' ' + str(programParametersDict['mHb_ub']),
                      'mHc': str(programParametersDict['mHc_lb']) + ' ' + str(programParametersDict['mHc_ub']),
                      
                      't1':  str(programParametersDict['ths_lb']) + ' ' + str(programParametersDict['ths_ub']),
                      't2':  str(programParametersDict['thx_lb']) + ' ' + str(programParametersDict['thx_ub']),
                      't3':  str(programParametersDict['tsx_lb']) + ' ' + str(programParametersDict['tsx_ub'])}
    
    if paramFree == 'ths':
        config['scan']['t1'] = str(-np.pi/2) + ' ' + str(np.pi/2)
        config['scan']['t2'] = str(programParametersDict['thx_lb']) + ' ' + str(programParametersDict['thx_ub'])
        config['scan']['t3'] = str(programParametersDict['tsx_lb']) + ' ' + str(programParametersDict['tsx_ub'])
        
        config['scan']['vs'] = str(programParametersDict['vs_lb']) + ' ' + str(programParametersDict['vs_ub'])
        config['scan']['vx'] = str(programParametersDict['vx_lb']) + ' ' + str(programParametersDict['vx_ub'])

    elif paramFree == 'thx':
        config['scan']['t1'] = str(programParametersDict['ths_lb']) + ' ' + str(programParametersDict['ths_ub'])
        config['scan']['t2'] = str(-np.pi/2) + ' ' + str(np.pi/2)
        config['scan']['t3'] = str(programParametersDict['tsx_lb']) + ' ' + str(programParametersDict['tsx_ub'])
        
        config['scan']['vs'] = str(programParametersDict['vs_lb']) + ' ' + str(programParametersDict['vs_ub'])
        config['scan']['vx'] = str(programParametersDict['vx_lb']) + ' ' + str(programParametersDict['vx_ub'])

    elif paramFree == 'tsx':
        config['scan']['t1'] = str(programParametersDict['ths_lb']) + ' ' + str(programParametersDict['ths_ub'])
        config['scan']['t2'] = str(programParametersDict['thx_lb']) + ' ' + str(programParametersDict['thx_ub'])
        config['scan']['t3'] = str(-np.pi/2) + ' ' + str(np.pi/2)
        
        config['scan']['vs'] = str(programParametersDict['vs_lb']) + ' ' + str(programParametersDict['vs_ub'])
        config['scan']['vx'] = str(programParametersDict['vx_lb']) + ' ' + str(programParametersDict['vx_ub'])
    
    if paramFree == 'vs':
        config['scan']['t1'] = str(programParametersDict['ths_lb']) + ' ' + str(programParametersDict['ths_ub'])
        config['scan']['t2'] = str(programParametersDict['thx_lb']) + ' ' + str(programParametersDict['thx_ub'])
        config['scan']['t3'] = str(programParametersDict['tsx_lb']) + ' ' + str(programParametersDict['tsx_ub'])
        
        config['scan']['vs'] = '1 1000'
        config['scan']['vx'] = str(programParametersDict['vx_lb']) + ' ' + str(programParametersDict['vx_ub'])

    elif paramFree == 'vx':
        config['scan']['vs'] = str(programParametersDict['vs_lb']) + ' ' + str(programParametersDict['vs_ub'])
        config['scan']['vx'] = '1 1000'
        
    else:
        raise Exception('No paramFree chosen in function vev')
    
    configDir = paramDir + '/' + 'config_' + paramFree + '_' + dataId + '.ini'
    with open(configDir, 'w') as configfile:
        config.write(configfile)
    
    configDir = 'config_' + paramFree + '_' + dataId + '.ini'
    outputDir = 'output_' + paramFree + '_' + dataId + '.tsv'
    
    runTRSM = lista = ['../../../TRSMBroken', outputDir, '--config', configDir, 'scan', '-n', str(points)]
    
    try:
        shell_output = subprocess.run(runTRSM, timeout = 180, cwd = paramDir)

    except subprocess.TimeoutExpired:
        print("Process timed out for taking too long. ")

#    shell_output = shell_output.stdout.decode('utf-8')
#    print(shell_output) 


programParametersDict = {
            'mHa_lb': 90, 'mHa_ub': 90, 'mHb_lb': 125.09, 'mHb_ub': 125.09, 'mHc_lb': 230, 'mHc_ub': 230,
            'ths_lb': 1.352, 'ths_ub': 1.352, 'thx_lb': 1.175, 'thx_ub': 1.175, 'tsx_lb': -0.407, 'tsx_ub': -0.407,
            'vs_lb': 120, 'vs_ub': 120, 'vx_lb': 890, 'vx_ub': 890,
            }

vev(programParametersDict, 'mS100-mX20', 'vx', 100)
print('=======================================')
#vev(programParametersDict, 'mS100-mX20', 'vs')



#'vs':  str(programParametersDict['vs_lb']) + ' ' + str(programParametersDict['vs_ub']),
#'vx':  str(programParametersDict['vx_lb']) + ' ' + str(programParametersDict['vx_ub'])}
#usr_params = {'ms': 100, 'mx': 20}
#parameterData(usr_params)






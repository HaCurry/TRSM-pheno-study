# -*- coding: utf-8 -*-
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



def paramDirCreator(userParametersDict, targetDir, **kwargs):

    ############################# kwargs #############################

    if 'createDir' in kwargs:
        createDir = kwargs['createDir']

    else:
        createDir = True

    ##################################################################
    
    # main directory for storage
    if os.path.isdir(targetDir) == False:
        subprocess.run(['mkdir', targetDir])

    else:
        pass

    # otherwise define dataId from userParametersDict
    if ('extra' in userParametersDict) and ('dataId' in userParametersDict['extra']):
        dataId = userParametersDict['extra']['dataId']

    # if dataId is not in userParametersDict raise exception
    else:
        raise Exception('You need to provide an identifier of userParametersDict. \n Please define a unique value in userParametersDict[\'extra\'][\'dataId\']')

    # create more sophisticated directory structure if createDir == True
    if createDir == True:

        if os.path.isdir(targetDir + '/' + dataId) == False:
            dataId = userParametersDict['extra']['dataId']
            subprocess.run(['mkdir', targetDir + '/' + dataId])

        else:
            pass

    # otherwise output all data in targetDir
    else:
        pass


def repackingProgramParamDict(userParametersDict, **kwargs):

    # parameter values used by script
    if 'manualBP' in kwargs:
        programParametersDict = kwargs['manualBP']

    # otherwise use BP2 values
    else:
        programParametersDict = {
            'bfb': 'apply', 'uni': 'apply', 'stu': 'apply', 'Higgs': 'apply',
            'mHa_lb': 80, 'mHa_ub': 80, 'mHb_lb': 125.09, 'mHb_ub': 125.09, 'mHc_lb': 375, 'mHc_ub': 375,
            'ths_lb': 1.352, 'ths_ub': 1.352, 'thx_lb': 1.175, 'thx_ub': 1.175, 'tsx_lb': -0.407, 'tsx_ub': -0.407,
            'vs_lb': 120, 'vs_ub': 120, 'vx_lb': 890, 'vx_ub': 890,
            }
    
    # or if user specifies the BP by name eg. 'BP2', then use the appropriate parameter values
    if 'BP' in kwargs:
        
        if kwargs['BP'] == 'BP2':
            programParametersDict = {
                'bfb': 'apply', 'uni': 'apply', 'stu': 'apply', 'Higgs': 'apply',
                'mHa_lb': 80, 'mHa_ub': 80, 'mHb_lb': 125.09, 'mHb_ub': 125.09, 'mHc_lb': 375, 'mHc_ub': 375,
                'ths_lb': 1.352, 'ths_ub': 1.352, 'thx_lb': 1.175, 'thx_ub': 1.175, 'tsx_lb': -0.407, 'tsx_ub': -0.407,
                'vs_lb': 120, 'vs_ub': 120, 'vx_lb': 890, 'vx_ub': 890,
                }
        
        elif kwargs['BP'] == 'BP3':
            programParametersDict = {
                'bfb': 'apply', 'uni': 'apply', 'stu': 'apply', 'Higgs': 'apply', 
                "mHa_lb": 125.09, "mHa_ub": 125.09, "mHb_lb": 200, "mHb_ub": 200, "mHc_lb": 400, "mHc_ub": 400, 
                "ths_lb": -0.129, "ths_ub": -0.129, "thx_lb": 0.226, "thx_ub": 0.226, "tsx_lb": -0.899, "tsx_ub": -0.899, 
                "vs_lb": 140, "vs_ub": 140, "vx_lb": 100, "vx_ub": 100, 
                }

    # raise exception if user specifies programParametersDict and specifies BP at the same time
    if ('manualBP' in kwargs) and ('BP' in kwargs):
        raise Exception('Cannot specify BP (Benchmark plane) and manualBP at the same time in kwargs.')



    userParametersKeys = userParametersDict.keys()

    # additional parameters given by user inserted in programParametersDict
    for key in userParametersKeys:
        programParametersDict[key] = userParametersDict[key]

    return programParametersDict



def createJSON(programParametersDict, path, filename):
    '''
    create JSON file from the given input dictionary programParametersDict.

    programParametersDict dict. dictionary which is converted to JSON.
    path string. directory where the json file is saved
    filename string. name of the JSON file (needs to end with .JSON)
    '''
    dictJSON = programParametersDict
    with open(path + '/' + filename, 'w') as f:
        json.dump(dictJSON, f, indent = 4)


def checkCreator(configDir, inputDict, points):
    '''
    Used for when scannerSmode == 'check' to create an input .tsv file for checking.

    configDir string. name of .tsv file (needs to end with .tsv)
    inputDict dict. dictionary with input settings.
    points int/float. used for the number of rows in the .tsv file (created by using linspace).
    returns nothing.
    '''
    mH1 = np.linspace(inputDict['mHa_lb'], inputDict['mHa_ub'], num = points)
    mH2 = np.linspace(inputDict['mHb_lb'], inputDict['mHb_ub'], num = points)
    mH3 = np.linspace(inputDict['mHc_lb'], inputDict['mHc_ub'], num = points)
    thetahS = np.linspace(inputDict['ths_lb'], inputDict['ths_ub'], num = points)
    thetahX = np.linspace(inputDict['thx_lb'], inputDict['thx_ub'], num = points)
    thetaSX = np.linspace(inputDict['tsx_lb'], inputDict['tsx_ub'], num = points)
    vs = np.linspace(inputDict['vs_lb'], inputDict['vs_ub'], num = points)
    vx = np.linspace(inputDict['vx_lb'], inputDict['vx_ub'], num = points)
    
    pandasDict = {'mH1': mH1, 'mH2': mH2, 'mH3': mH3, 'thetahS': thetahS, 'thetahX': thetahX, 'thetaSX': thetaSX, 'vs': vs, 'vx': vx}

    df = pandas.DataFrame(data = pandasDict, dtype = np.float64)

    df.to_csv(configDir, sep = "\t")


def param(programParametersDict, targetDir, paramFree, scannerSmode, **kwargs):

    '''
    Generates data given a dictionary programParametersDict and a free
    parameter paramFree to the output directory targetDir (with a nice
    directory structure if createdir is on which it is by default). Can
    generate through the scannerS modes scan or check (see scannerS manual).
    
    programParametersDict dict. parameter values in a dictionary with upper and
                                lower bounds. Constraints need to also be
                                included.
    targetDir string. output directory, outputs to a nice directory structure
                      if createDir is on.
    paramFree string. the free parameter over which data is to be generated.
    scannerSmode string. data generation through scannerS mode, see manual for 
                         details.
    kwargs points int.
           createDir int. creates nice directory structure inside targetDir if
                          enabled otherwise outputs everything into targetDir.
           shortLog bool. saves shell output from scannerS in a short format.
    '''
    
    ########################    kwargs    ########################

    # default option is 100. Number of points generated by param
    if 'points' in kwargs:
        points = kwargs['points']

    else:
        points = 100

    if 'createDir' in kwargs:
        createDir = kwargs['createDir']

    # default option set to True. Creates parameter specific directory inside
    # directory targetDir/dataId/, created by other functions.
    else:
        createDir = True


    # default option set to True. Saves shorter outputs from ScannerS to shell in .txt file
    if 'shortLog' in kwargs:
        shortLog = kwargs['shortLog']
    
    else:
        shortLog = True

    ##############################################################
    
    # check if dataId is in programParametersDict
    if ('extra' in programParametersDict) and ('dataId' in programParametersDict['extra']):
        dataId = programParametersDict['extra']['dataId']

    # else raise exception
    else:
               
        raise Exception('You need to provide an identifier of programParametersDict\nPlease define a unique value in programParametersDict[\'extra\'][\'dataId\']')
    
    if createDir == True:

        if os.path.isdir(targetDir + '/' + dataId + '/' + paramFree + '_' + dataId) == True:

            paramDir = targetDir + '/' + dataId + '/' + paramFree + '_' + dataId

        elif os.path.isdir(targetDir + '/' + dataId + '/' + paramFree + '_' + dataId) == False:

            if os.path.isdir(targetDir + '/' + dataId) == True:
                paramDir = targetDir + '/' + dataId + '/' + paramFree + '_' + dataId
                subprocess.run(['mkdir', paramDir])

            elif os.path.isdir(targetDir + '/' + dataId) == False:
                
                if os.path.isdir(targetDir) == True:
                    subprocess.run(['mkdir', targetDir + '/' + dataId])
                    paramDir = targetDir + '/' + dataId + '/' + paramFree + '_' + dataId
                    subprocess.run(['mkdir', paramDir])
                    
                elif os.path.isdir(targetDir) == False:
                    subprocess.run(['mkdir', targetDir])
                    subprocess.run(['mkdir', targetDir + '/' + dataId])
                    paramDir = targetDir + '/' + dataId + '/' + paramFree + '_' + dataId
                    subprocess.run(['mkdir', paramDir])
                
                else:
                    raise Exception('Error creating directories in param')

            else:
                raise Exception('Error creating directories in param')
        
        else:
            raise Exception('Error creating directories in param')

    # otherwise output everything in the directory targetDir
    elif createDir == False:
    
        print('createDir set to False, output generated in targetDir.')
    
        if os.path.isdir(targetDir) == True:
            paramDir = targetDir
        
        elif os.path.isdir(targetDir) == False:
            paramDir = targetDir
            subprocess.run(['mkdir', paramDir])
        
        else:
            raise Exception('Error creating directories in param')
    
    else:
        raise Exception('error occurred in createDir in param')

    # for .ini (config) file
    config = configparser.ConfigParser()

    # used to save programParametersDict (and additional stuff) to JSON later
    # deepcopy used so that eg. elements of the dictionary is also copied.
    save2JSON = copy.deepcopy(programParametersDict)
    
    # set constraints
    config['DEFAULT'] = {
                        'bfb': str(programParametersDict['bfb']),
                        'uni': str(programParametersDict['uni']),
                        'stu': str(programParametersDict['stu']),
                        'Higgs': str(programParametersDict['Higgs'])
                         }

    # set parameters in .ini (config)
    # save the free parameter values to programParametersDict
    config['scan'] = {'mHa': str(programParametersDict['mHa_lb']) + ' ' + str(programParametersDict['mHa_ub']),
                      'mHb': str(programParametersDict['mHb_lb']) + ' ' + str(programParametersDict['mHb_ub']),
                      'mHc': str(programParametersDict['mHc_lb']) + ' ' + str(programParametersDict['mHc_ub'])}

    if paramFree == 'ths':
        save2JSON['ths_lb'], save2JSON['ths_ub'] = -np.pi/2, np.pi/2

        config['scan']['t1'] = str(-np.pi/2) + ' ' + str(np.pi/2)
        config['scan']['t2'] = str(programParametersDict['thx_lb']) + ' ' + str(programParametersDict['thx_ub'])
        config['scan']['t3'] = str(programParametersDict['tsx_lb']) + ' ' + str(programParametersDict['tsx_ub'])

        config['scan']['vs'] = str(programParametersDict['vs_lb']) + ' ' + str(programParametersDict['vs_ub'])
        config['scan']['vx'] = str(programParametersDict['vx_lb']) + ' ' + str(programParametersDict['vx_ub'])

    elif paramFree == 'thx':
        save2JSON['thx_lb'], save2JSON['thx_ub'] = -np.pi/2, np.pi/2

        config['scan']['t1'] = str(programParametersDict['ths_lb']) + ' ' + str(programParametersDict['ths_ub'])
        config['scan']['t2'] = str(-np.pi/2) + ' ' + str(np.pi/2)
        config['scan']['t3'] = str(programParametersDict['tsx_lb']) + ' ' + str(programParametersDict['tsx_ub'])

        config['scan']['vs'] = str(programParametersDict['vs_lb']) + ' ' + str(programParametersDict['vs_ub'])
        config['scan']['vx'] = str(programParametersDict['vx_lb']) + ' ' + str(programParametersDict['vx_ub'])

    elif paramFree == 'tsx':
        save2JSON['tsx_lb'], save2JSON['tsx_ub'] = -np.pi/2, np.pi/2

        config['scan']['t1'] = str(programParametersDict['ths_lb']) + ' ' + str(programParametersDict['ths_ub'])
        config['scan']['t2'] = str(programParametersDict['thx_lb']) + ' ' + str(programParametersDict['thx_ub'])
        config['scan']['t3'] = str(-np.pi/2) + ' ' + str(np.pi/2)

        config['scan']['vs'] = str(programParametersDict['vs_lb']) + ' ' + str(programParametersDict['vs_ub'])
        config['scan']['vx'] = str(programParametersDict['vx_lb']) + ' ' + str(programParametersDict['vx_ub'])

    elif paramFree == 'vs':
        save2JSON['vs_lb'], save2JSON['vs_ub'] = 1, 1000

        config['scan']['t1'] = str(programParametersDict['ths_lb']) + ' ' + str(programParametersDict['ths_ub'])
        config['scan']['t2'] = str(programParametersDict['thx_lb']) + ' ' + str(programParametersDict['thx_ub'])
        config['scan']['t3'] = str(programParametersDict['tsx_lb']) + ' ' + str(programParametersDict['tsx_ub'])

        config['scan']['vs'] = '1 1000'
        config['scan']['vx'] = str(programParametersDict['vx_lb']) + ' ' + str(programParametersDict['vx_ub'])

    elif paramFree == 'vx':
        save2JSON['vx_lb'], save2JSON['vx_ub'] = 1, 1000

        config['scan']['t1'] = str(programParametersDict['ths_lb']) + ' ' + str(programParametersDict['ths_ub'])
        config['scan']['t2'] = str(programParametersDict['thx_lb']) + ' ' + str(programParametersDict['thx_ub'])
        config['scan']['t3'] = str(programParametersDict['tsx_lb']) + ' ' + str(programParametersDict['tsx_ub'])

        config['scan']['vs'] = str(programParametersDict['vs_lb']) + ' ' + str(programParametersDict['vs_ub'])
        config['scan']['vx'] = '1 1000'

    # if paramFree is set to Nofree, then all parameters are fixed according to the user given parameters.
    elif paramFree == 'Nofree':
        config['scan']['t1'] = str(programParametersDict['ths_lb']) + ' ' + str(programParametersDict['ths_ub'])
        config['scan']['t2'] = str(programParametersDict['thx_lb']) + ' ' + str(programParametersDict['thx_ub'])
        config['scan']['t3'] = str(programParametersDict['tsx_lb']) + ' ' + str(programParametersDict['tsx_ub'])

        config['scan']['vs'] = str(programParametersDict['vs_lb']) + ' ' + str(programParametersDict['vs_ub'])
        config['scan']['vx'] = str(programParametersDict['vx_lb']) + ' ' + str(programParametersDict['vx_ub'])

    else:
        raise Exception('No paramFree defined in function vev')

    # define the paths to .ini (config) file and .tsv (output) file
    # configDir = paramDir + '/' + 'config_' + paramFree + '_' + dataId + '.ini'
    # outputDir = paramDir + '/' + 'output_' + paramFree + '_' + dataId + '.tsv'

    # either randomly generate points within freeParam interval (scan) or...
    if scannerSmode == 'scan':

        # save .ini (config) file to the directory paramDir
        configDir = paramDir + '/' + 'configScan_' + paramFree + '_' + dataId + '.ini'
        with open(configDir, 'w') as configfile:
            config.write(configfile)

        # (re)define the config and output files for running in current working directory (see cwd in subprocess.run below)
        configDir = 'configScan_' + paramFree + '_' + dataId + '.ini'
        outputDir = 'outputScan_' + paramFree + '_' + dataId + '.tsv'

        # conditional for the appropriate relative path to the executable TRSMBroken
        if createDir == True:
            runTRSM = ['../../../../TRSMBroken', outputDir, '--config', configDir, 'scan', '-n', str(points)]

        elif createDir == False:
            runTRSM = ['../../TRSMBroken', outputDir, '--config', configDir, 'scan', '-n', str(points)]

        else:
            raise Exception('createDir is not working in runTRSM')

        # for length of shell output
        loglines = -17

    # ...generate a constantly spaced number of points in the paramFree interval (interval hardcoded into the script)
    elif scannerSmode == 'check':

        # save .tsv (config) file to the directory paramDir
        configDir = paramDir + '/' + 'configCheck_' + paramFree + '_' + dataId + '.tsv'
        checkCreator(configDir, save2JSON, points)

        # (re)define the config and output files for running in current working directory (see cwd in subprocess.run below)
        configDir = 'configCheck_' + paramFree + '_' + dataId + '.tsv'
        outputDir = 'outputCheck_' + paramFree + '_' + dataId + '.tsv'

        
        # conditional for the appropriate relative path to the executable TRSMBroken
        if createDir == True:
            runTRSM = ['../../../../TRSMBroken', outputDir, 'check', configDir]

        elif createDir == False:
            runTRSM = ['../../TRSMBroken', outputDir, 'check', configDir]

        else:
            raise Exception('createDir is not working in runTRSM')

        # for length of shell output
        loglines = -9

    else:
        raise Exception('scannerSmode not given or invalid value (allowed \'scan\' or \'check\')')
    
    # save programParametersDict as JSON in the directory paramDir and add the paths of the config and output to the JSON
    if 'extra' in save2JSON:
        pass
    else:
        save2JSON['extra'] = {}

    # additional metadata saved to programParametersDict and then converted to a JSON file in the directory paramDir
    save2JSON['extra']['pathDataOutput'] = paramDir + '/' + outputDir
    save2JSON['extra']['pathDataConfig'] = paramDir + '/' + configDir
    save2JSON['extra']['points'] = points
    save2JSON['extra']['scannerSmode'] = scannerSmode
    paramFreeTranslate = {'ths': 'thetahS', 'thx': 'thetahX', 'tsx': 'thetaSX', 'vs': 'vs', 'vx': 'vx', 'Nofree': 'Nofree'}
    save2JSON['extra']['paramFree'] = paramFreeTranslate[paramFree]
    createJSON(save2JSON, paramDir, 'settings_' + paramFree + '_' + dataId + '.json')
    # delete dictionary so no conflict is caused for future or concurrent runs
    del save2JSON 

    # run TRSMBroken executable
    try:

        shell_output = subprocess.run(runTRSM, timeout = 180, capture_output = True, cwd = paramDir)
        shell_output = shell_output.stdout.decode('utf-8')
        shell_output_short = (shell_output.splitlines())[loglines:]

        # print the important part of the shell output as .txt if shortLog == True
        if shortLog == True:
            
            for line in shell_output_short:
                print(line)

        # save the full shell output as .txt
        with open(paramDir + '/' 'full_log_' + paramFree + '_' + dataId + '.txt', 'w') as text_file:
            text_file.write(shell_output)

        # save the important part of the shell output as .txt
        with open(paramDir + '/' + 'short_log_' + paramFree + '_' + dataId + '.txt', 'w') as text_file:
            
            for line in shell_output_short:
                text_file.write(line + '\n')

    # if TRSMBroken executable does not find points within 180 seconds, timeout and save the dud point
    except subprocess.TimeoutExpired:

        print('Process timed out for taking too long. ')
#        Write down faulty point in duds.txt
        # with open(targetDir + '/' + 'duds.txt', 'a') as dud:
            # dud.write(dataId + ' ' + paramFree + ' ' + str(datetime.datetime.now()) + '\n')
        # saves the dud point
        with open(targetDir + '/' + dataId + '_' + paramFree + '_' + str(datetime.datetime.now()) + '.txt', 'a') as dud:
            dud.write(dataId + ' ' + paramFree + ' ' + str(datetime.datetime.now()) + '\n')



def parameterMain(listUserParametersDict, targetDir, scannerSmode, **kwargs):
    '''Main function'''

    startTime = str(datetime.datetime.now())
    
    print('+---------------+')
    print(' Starting script')
    print('+---------------+')
    print(scannerSmode.center(17))
    print('+---------------+')
    
    loading = len(listUserParametersDict)
    loadingstep = 1

    for userParametersDict in listUserParametersDict:

        print('===========')
        print(userParametersDict)
        print('===========')
        
        
        # create directory for storage, returns name of directory
        paramDirCreator(userParametersDict, targetDir, **kwargs)

        # reformats user given dictionary to usable format for param
        programParametersDict = repackingProgramParamDict(userParametersDict, **kwargs)

        param(programParametersDict, targetDir, 'ths', scannerSmode, **kwargs)
        param(programParametersDict, targetDir, 'thx', scannerSmode, **kwargs)
        param(programParametersDict, targetDir, 'tsx', scannerSmode, **kwargs)
        
        param(programParametersDict, targetDir, 'vs',  scannerSmode, **kwargs)
        param(programParametersDict, targetDir, 'vx',  scannerSmode, **kwargs)

        param(programParametersDict, targetDir, 'Nofree',scannerSmode, **kwargs)

        print('completed ' + str(loadingstep) + '/' + str(loading) + ' mass points')
        loadingstep = loadingstep + 1
    
    print('+----------------+')
    print(' Script complete!')
    print('+----------------+')

    endTime = str(datetime.datetime.now())

    with open('processTime.txt', 'a') as text_file:
        text_file.write('normal start:' + startTime + '\nnormal end:' + endTime + '\n\n')



def mProcWrapper(userParametersDict, mprocBP, targetDir, mprocPoints, scannerSmode):

    # reformats user given dictionary to usable format for param
    programParametersDict = repackingProgramParamDict(userParametersDict, BP = mprocBP, points = mprocPoints)

    param(programParametersDict, targetDir, 'ths', scannerSmode, BP = mprocBP, points = mprocPoints)
    param(programParametersDict, targetDir, 'thx', scannerSmode, BP = mprocBP, points = mprocPoints)
    param(programParametersDict, targetDir, 'tsx', scannerSmode, BP = mprocBP, points = mprocPoints)
    
    param(programParametersDict, targetDir, 'vs',  scannerSmode, BP = mprocBP, points = mprocPoints)
    param(programParametersDict, targetDir, 'vx',  scannerSmode, BP = mprocBP, points = mprocPoints)
    
    param(programParametersDict, targetDir, 'Nofree',scannerSmode, BP = mprocBP, points = 5) # could set points = 1 as it seems the values in the outputs are identical (?)



def mProcParameterMain(listUserParametersDict, BP, targetDir, mprocMainPoints, scannerSmode):
    '''Main function (multiprocessing)'''

    dataIdList = [paramDirCreator(listUserParametersDict[i], targetDir) for i in range(len(listUserParametersDict))]
    
    # for userParametersDict in listUserParametersDict:
        # dataId = paramDirCreator(userParametersDict, targetDir)
        # dataIdList.append(dataId)
        
    mprocStartTime = str(datetime.datetime.now())
    
    print('*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*')
    print(' Starting script (multiprocessing)')
    print('*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*')
    print(scannerSmode.center(35))
    print('*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*')
    
    # for userParametersDict in listUserParametersDict:
        # starmapIter.append( (userParametersDict, BP, targetDir, mprocMainPoints) )
    
    starmapIter = [(listUserParametersDict[i], BP, targetDir, mprocMainPoints, scannerSmode) for i in range(len(listUserParametersDict))]
    
    pool = multiprocessing.Pool()

    try:
        pool.starmap(mProcWrapper, starmapIter)
        # pool.terminate()

    except KeyboardInterrupt:
        # code from StackExchange: https://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool
        pool.terminate()
        print('You cancelled the script!')
        sys.exit('Script exiting')

    print('*~~~~~~~~~~~~~~~~*')
    print(' Script complete!')
    print('*~~~~~~~~~~~~~~~~*')

    mprocEndTime = str(datetime.datetime.now())

    
    with open('processTime.txt', 'a') as text_file:
        text_file.write('mProc start:' + mprocStartTime + '\nmProc end:' + mprocEndTime + '\n\n\n')





if __name__ == '__main__':

    df2 = pandas.read_table('Atlas2023Limits_BP2lessThanOrEqualToTrue.tsv', index_col = 0)

    ms_BP2 = df2['ms']
    mx_BP2 = df2['mx']
    limit_obs_BP2 = df2['limit_obs']

    BP2_dictPointlistAtlas = [{
                               'mHa_lb': ms_BP2[i], 'mHa_ub': ms_BP2[i],
                               'mHb_lb': 125.09,    'mHb_ub': 125.09,
                               'mHc_lb': mx_BP2[i], 'mHc_ub': mx_BP2[i],
                               'extra': {'ObservedLimit': 10**(-3) * limit_obs_BP2[i], 'dataId': 'S' + str(ms_BP2[i]) + '-' + 'X' + str(mx_BP2[i]) } } for i in  range(len(ms_BP2))]

    df3 = pandas.read_table('Atlas2023Limits_BP3lessThanOrEqualToTrue.tsv', index_col = 0)
     
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


    # parameterMain([BP3_dictPointlistAtlas[0]], 'tjolahopp2', 'scan', BP = 'BP3', createDir = False, points = 12)
    # # (listUserParametersDict, BP, targetDir, mprocMainPoints, scannerSmode)


    # mProcParameterMain(BP2_dictPointlistAtlas, 'BP2', 'AtlasBP2_check_prel2', 50, 'check')
    # mProcParameterMain(BP3_dictPointlistAtlas, 'BP3', 'AtlasBP3_check_prel', 50, 'check')
    
    # mProcParameterMain(BP2_dictPointlistAtlas, 'BP2', 'AtlasBP2_scan_prel', 50, 'scan')
    # mProcParameterMain(BP3_dictPointlistAtlas, 'BP3', 'AtlasBP3_scan_prel', 50, 'scan')

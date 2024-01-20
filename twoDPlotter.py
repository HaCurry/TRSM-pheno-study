#-*- coding: utf-8 -*-
import pandas

import numpy as np

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
import glob
import json

import functions as TRSM
import Exclusion_functions as excl
import parameterData
# import adjustText


def exclusionCompiler(settingsGlob, dataPath, locOutputData, **kwargs):
    
    #################################### kwargs ####################################

    if 'XStotKey' in kwargs:
        XStotKey = kwargs['XStotKey']

    else:
        XStotKey = 'x_H3_H1H2_SM1SM2'


    if 'XS1Key' in kwargs:
        XS1Key = kwargs['XS1Key']

    else:
        XS1Key = 'x_H3_H1_SM1_H2_SM2'


    if 'XS2Key' in kwargs:
        XS2Key = kwargs['XS2Key']

    else:
        XS2Key = 'x_H3_H1_SM2_H2_SM1'

    if 'ObsLimKey' in kwargs:
        ObsLimKey = kwargs['ObsLimKey']

    else:
        ObsLimKey = 'ObservedLimit'

    if 'msKey' in kwargs:
        msKey = kwargs['msKey']

    else:
        raise Exception('No msKey given in kwargs')

    if 'mxKey' in kwargs:
        mxKey = kwargs['mxKey']

    else:
        raise Exception('No mxKey given in kwargs')

    if 'dataPathKey' in kwargs:
        dataPathKey = kwargs['dataPathKey']

    else:
        dataPathKey = 'pathCalcppXNPSM_H1H2_'

    ################################################################################

    # if not os.path.isdir(locOutputData):
    #     os.makedirs(locOutputData)
    
    pathList = parameterData.directorySearcher(dataPath, settingsGlob)
    dictList = parameterData.dictConstruct(pathList)
    if len(dictList) == 0: raise Exception('No files find with given settingsGlob = ' + settingsGlob + '\n and dataPath = ' + dataPath)
    saveTable = {'ms': [], 'mx': [], 'ObservedLimit': [], XStotKey: [], XS1Key: [], XS2Key: []}

    for dictElement in dictList:
        
        # save the mHa, mHb, mHc mass values in a variable
        ms = dictElement[msKey]
        mx = dictElement[mxKey]

        # save the ObsLim values in a variable
        ObservedLimit = dictElement['extra'][ObsLimKey]

        # save the TRSM XS values in a variable
        dataPath = dictElement['extra'][dataPathKey]
        # df = pandas.DataFrame(data = dataPath)
        try:
            df = pandas.read_table(dataPath, index_col = 0)
            # print(df)
            listXStot = [i for i in df[XStotKey]]
            listXS1 = [i for i in df[XS1Key]]
            listXS2 = [i for i in df[XS2Key]]
     
            # check if the scannerS or calculation produced any error
            for element in listXStot:
                if abs(listXStot[0] - element) > 10**(-8):
                    raise Exception('{} not equal everywhere'.format(XStotKey))
        
            for element in listXS1:
                if abs(listXS1[0] - element) > 10**(-8):
                    raise Exception('{} not equal everywhere'.format(XS1Key))

            for element in listXS2:
                if abs(listXS2[0] - element) > 10**(-8):
                    raise Exception('{} not equal everywhere'.format(XS2Key))

        except pandas.errors.EmptyDataError:
            listXStot = [np.nan]
            listXS1 = [np.nan]
            listXS2 = [np.nan]

            

        XStot = listXStot[0]
        XS1 = listXS1[0]
        XS2 = listXS2[0]

        saveTable['ms'].append(ms)
        saveTable['mx'].append(mx)
        saveTable['ObservedLimit'].append(ObservedLimit)
        saveTable[XStotKey].append(XStot)
        saveTable[XS1Key].append(XS1)
        saveTable[XS2Key].append(XS2)

    # print(saveTable)
    df = pandas.DataFrame(data = saveTable)
    print(df)
    df.to_csv(locOutputData, sep = "\t")


def exclusionPlotter(dataPath, locOutputData, epsilon, **kwargs):

    ''' Deprecated '''
    
    #################################### kwargs ####################################

    if 'msKey' in kwargs:
        msKey = kwargs['msKey']

    else:
        msKey = 'ms'

    if 'mxKey' in kwargs:
        mxKey = kwargs['mxKey']

    else:
        mxKey = 'mx'

    if 'XStotKey' in kwargs:
        XStotKey = kwargs['XStotKey']

    else:
        # XStotKey = 'x_H3_H1H2_SM_tot'
        XStotKey = 'x_H3_H1H2_SM1SM2'


    if 'XS1Key' in kwargs:
        XS1Key = kwargs['XS1Key']

    else:
        # XS1Key = 'x_H3_H1H2_SM_1'
        XS1Key = 'x_H3_H1_SM1_H2_SM2'


    if 'XS2Key' in kwargs:
        XS2Key = kwargs['XS2Key']

    else:
        # XS2Key = 'x_H3_H1H2_SM_2'
        XS2Key = 'x_H3_H1_SM2_H2_SM1'
    
    
    if 'ObsLimKey' in kwargs:
        ObsLimKey = kwargs['ObsLimKey']

    else:
        ObsLimKey = 'ObservedLimit'

    if 'xlims' in kwargs:
        xlims = kwargs['xlims']

    else:
        raise Exception('please provide xlim bounds')

    if 'ylims' in kwargs:
        ylims = kwargs['ylims']

    else:
        raise Exception('please provide ylim bounds')

    
    ################################################################################

    # create directory to save figures
    if not os.path.isdir(locOutputData):
        os.makedirs(locOutputData)

    # read data
    df = pandas.read_table(dataPath, index_col = 0)

    # store data in lists
    msList = df[msKey]    
    mxList = df[mxKey]
    ObsLimList = df[ObsLimKey] 
    XStotList = df[XStotKey]
    XS1List = df[XS1Key]
    XS2List = df[XS2Key]
    
    # store everything in a dictionary for the last figure
    values = {msKey: msList, mxKey: mxList, 
              ObsLimKey: ObsLimList, 
              XStotKey: XStotList, XS1Key: XS1List, XS2Key: XS2List}
    
    # error check: check all data is of equal length
    (len(msList) + len(mxList) + len(ObsLimList) + len(XS1List)
    + len(XS2List) + len(XStotList)) / (6 * len(msList))

    # check if anything is excluded
    exclTotList = []
    excl1List = []
    excl2List = []

    for i in range(len(ObsLimList)):
        if XStotList[i] - ObsLimList[i] > epsilon:
            exclTotList.append({msKey: msList[i], mxKey: mxList[i], ObsLimKey: ObsLimList[i], XStotKey: XStotList[i]})
    
    for i in range(len(ObsLimList)):
        if XS1List[i] - ObsLimList[i] > epsilon:
            excl1List.append({msKey: msList[i], mxKey: mxList[i], ObsLimKey: ObsLimList[i], XS1Key: XS1List[i]})

    for i in range(len(ObsLimList)):
        if XS2List[i] - ObsLimList[i] > epsilon:
            excl2List.append({msKey: msList[i], mxKey: mxList[i], ObsLimKey: ObsLimList[i], XS2Key: XS2List[i]})
    
    # print the excluded mass points
    print('=============================================')
    print('Excluded points ' + XStotKey + ': ' + str(exclTotList))
    print('=============================================')
    print('Excluded points ' + XS1Key + ': ' + str(excl1List))
    print('=============================================')
    print('Excluded points ' + XS2Key + ': ' + str(excl2List))
    print('=============================================')
       
    # plot Observed Limits or anything with the column name ObsLimKey
    plt.scatter(msList, mxList, c=ObsLimList, cmap='viridis')
    for i in range(len(ObsLimList)):
        # plt.text(ms[i], mx[i], '{:.3}'.format(limit_obs[i]), fontsize = 8)
        plt.annotate('{:.1e}'.format(ObsLimList[i]), (msList[i], mxList[i]),
                     textcoords = 'offset points', xytext= (0,0), fontsize = 10, rotation = 0, 
                     path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground="w")])
    plt.title(ObsLimKey)
    plt.xlim(xlims)
    plt.ylim(ylims)
    # plt.savefig(locOutputData + '/' + ObsLimKey + '_RAW' + '.pdf')
    # plt.show()
    plt.close()

    # plot total-cross section or anything with the column name XStotKey
    plt.scatter(msList, mxList, c=XStotList, cmap='viridis')
    for i in range(len(XStotList)):
        # plt.text(ms[i], mx[i], '{:.3}'.format(limit_obs[i]), fontsize = 8)
        plt.annotate('{:.1e}'.format(XStotList[i]), (msList[i], mxList[i]),
                     textcoords = 'offset points', xytext= (0,0), fontsize = 10, rotation = 0, 
                     path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground="w")])
    plt.title(XStotKey)
    plt.xlim(xlims)
    plt.ylim(ylims)
    # plt.savefig(locOutputData + '/' + XStotKey + '_RAW' + '.pdf')
    # plt.show()
    plt.close()

    # plot cross-section of first mode or anything with the column name XS1Key
    plt.scatter(msList, mxList, c=XS1List, cmap='viridis')
    for i in range(len(XS1List)):
        # plt.text(ms[i], mx[i], '{:.3}'.format(limit_obs[i]), fontsize = 8)
        plt.annotate('{:.1e}'.format(XS1List[i]), (msList[i], mxList[i]),
                     textcoords = 'offset points', xytext= (0,0), fontsize = 10, rotation = 0, 
                     path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground="w")])
    plt.title(XS1Key)
    plt.xlim(xlims)
    plt.ylim(ylims)
    # plt.savefig(locOutputData + '/' + XS1Key  + '_RAW' +  '.pdf')
    # plt.show()
    plt.close()

    # plot cross-section of second mode or anything with the column name XS2Key
    plt.scatter(msList, mxList, c=XS2List, cmap='viridis')
    for i in range(len(XS2List)):
        # plt.text(ms[i], mx[i], '{:.3}'.format(limit_obs[i]), fontsize = 8)
        plt.annotate('{:.1e}'.format(XS2List[i]), (msList[i], mxList[i]),
                     textcoords = 'offset points', xytext= (0,0), fontsize = 10, rotation = 0, 
                     path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground="w")])
    plt.title(XS2Key)
    plt.xlim(xlims)
    plt.ylim(ylims)
    # plt.savefig(locOutputData + '/' + XS2Key  + '_RAW' +  '.pdf')
    # plt.show()
    plt.close()

    # if user gives the below key names then plot the keyX on x-axis, keyY on y-axis
    # and keyA/keyB in the z-axis eg. S(bb)H(gamgam)/S(gamgam)H(bb)
    if ('keyX' in kwargs) and ('keyY' in kwargs) and ('keyA' in kwargs) and ('keyB' in kwargs):
        keyX = kwargs['keyX']
        keyY = kwargs['keyY']
        keyA = kwargs['keyA']
        keyB = kwargs['keyB']

        X = values[keyX]
        Y = values[keyY]
        C = np.array(values[keyA])/np.array(values[keyB])

        print('{}/{}: '.format(keyA, keyB) + str(C))
        print('=============================================')

        plt.scatter(X, Y, c = C, cmap='viridis')
        for i in range(len(X)):
            # plt.text(ms[i], mx[i], '{:.3}'.format(limit_obs[i]), fontsize = 8)
            plt.annotate('{:.1e}'.format(C[i]), (X[i], Y[i]),
                         textcoords = 'offset points', xytext= (0,0), fontsize = 10, rotation = 0, 
                         path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground="w")])

        plt.title('{}/{}'.format(keyA, keyB))
        plt.xlim(xlims)
        plt.ylim(ylims)
        # plt.savefig(locOutputData + '/' + keyA + '_dividedBy_' + keyB   + '_RAW' +   '.pdf')
        # plt.show()
        plt.close()


def checkCreator2d(pointsSq, locOutputData, mxBounds, msBounds, mxKey, msKey, mhKey, **kwargs):

    ############################# kwargs #############################

    if 'mH' in kwargs:
        mH = kwargs['mH']

        if (isinstance(mH, float) == False) and (isinstance(mH, int) == False):
            raise Exception('mH need to be of type float or int') 

    else:
        mH = 125.09


    if 'ths' in kwargs:
        ths = kwargs['ths']

        if (isinstance(ths, float) == False) and (isinstance(ths, int) == False):
            raise Exception('ths need to be of type float or int') 

    else:
        raise Exception('Please provide value of ths')


    if 'thx' in kwargs:
        thx = kwargs['thx']

        if (isinstance(thx, float) == False) and (isinstance(thx, int) == False):
            raise Exception('thx need to be of type float or int') 

    else:
        raise Exception('Please provide value of thx')
    

    if 'tsx' in kwargs:
        tsx = kwargs['tsx']

        if (isinstance(tsx, float) == False) and (isinstance(tsx, int) == False):
            raise Exception('tsx need to be of type float or int') 

    else:
        raise Exception('Please provide value of tsx')


    if 'vs' in kwargs:
        vs = kwargs['vs']

        if (isinstance(vs, float) == False) and (isinstance(vs, int) == False):
            raise Exception('vs need to be of type float or int') 

    else:
        raise Exception('Please provide value of vs')


    if 'vx' in kwargs:
        vx = kwargs['vx']

        if (isinstance(vx, float) == False) and (isinstance(vx, int) == False):
            raise Exception('vx need to be of type float or int') 

    else:
        raise Exception('Please provide value of vx')

    ##################################################################

    mx = np.linspace(mxBounds[0], mxBounds[1], pointsSq)
    ms = np.linspace(msBounds[0], msBounds[1], pointsSq)

    mxToConfig = []
    msToConfig = []

    for i in mx:
        for j in ms:
            mxToConfig.append(i)
            msToConfig.append(j)        

    configDict = {}

    configDict[mxKey] = mxToConfig
    configDict[msKey] = msToConfig
    configDict[mhKey] = [mH for i in range(len(mxToConfig))]
    configDict['thetahS'] = [ths for i in range(len(mxToConfig))]
    configDict['thetahX'] = [thx for i in range(len(mxToConfig))]
    configDict['thetaSX'] = [tsx for i in range(len(mxToConfig))]
    configDict['vs'] = [vs for i in range(len(mxToConfig))]
    configDict['vx'] = [vx for i in range(len(mxToConfig))]

    df = pandas.DataFrame(data = configDict, dtype = np.float64)

    df.to_csv(locOutputData, sep = "\t")


def runTRSM(TRSMpath, cwd, configName, outputName, scannerSmode, **kwargs):

    ############################# kwargs #############################

    if 'capture_output' in kwargs:
        capture_output = kwargs['capture_output']

        if isinstance(capture_output, bool) == False:
            raise Exception('capture_output need to be of type bool')

        else:
            pass

    else:
        capture_output = True
        
    ##################################################################
    
    if scannerSmode == 'scan':

        if 'points' in kwargs:
            points = kwargs['points']

            if isinstance(points, int) == False:
                raise Exception('points need to be of type int')

            else:
                pass

        else:
            raise Exception('points need to be defined if scannerSmode is set to scan')
        
        # runTRSM = ['../../../../TRSMBroken', outputName, '--config', configName, 'scan', '-n', str(points)]
        runTRSM = [TRSMpath, outputName, '--config', configName, 'scan', '-n', str(points)]
        loglines = -17

    elif scannerSmode == 'check':
        runTRSM = [TRSMpath, outputName, 'check', configName]
        loglines = -9

    shell_output = subprocess.run(runTRSM, capture_output = capture_output, cwd = cwd)

    if capture_output == True:
        shell_output = shell_output.stdout.decode('utf-8')
        shell_output_short = (shell_output.splitlines())[loglines:]
        for line in shell_output_short:
            print(line)
    else:
        pass


def calculateSort2D(dataPath, outputDir, outputName, SM1, SM2, **kwargs):

    ############################# kwargs #############################

    if 'ppXNPnorm' in kwargs:
        ppXNPnorm = kwargs['ppXNPnorm']

    else:
        ppXNPnorm = 1

    if 'ppXNPSMnorm' in kwargs:
        ppXNPSMnorm = kwargs['ppXNPSMnorm']

    else:
        ppXNPSMnorm = 1
        
    ##################################################################
    
    XNP_H1H2, XNP_H1H1, XNP_H2H2 = parameterData.dataCalculator('XNP', 'mH1', dataPath)
    ppXNP_H1H2, ppXNP_H1H1, ppXNP_H2H2 = parameterData.dataCalculator('ppXNP', 'mH1', dataPath, ggF_xs_SM_Higgs=ppXNPnorm)
    ppXNPSM_H1H2, ppXNPSM_H1H1, ppXNPSM_H2H2 = parameterData.dataCalculator('ppXNPSM', 'mH1', dataPath,
                                                                             SM1=SM1, SM2=SM2, ggF_xs_SM_Higgs_SM1SM2=ppXNPSMnorm)
    dictToTable = {}

    dictToTable['mH1'] = XNP_H1H2[0]
    dictToTable['mH2'] = XNP_H1H2[1]
    dictToTable['mH3'] = XNP_H1H2[2]


    dictToTable['b_H3_H1H2'] = XNP_H1H2[3]
    dictToTable['b_H3_H1H1'] = XNP_H1H1[3]
    dictToTable['b_H3_H2H2'] = XNP_H2H2[3]


    dictToTable['x_H3_H1H2'] = ppXNP_H1H2[4]
    dictToTable['x_H3_H1H1'] = ppXNP_H1H1[4]
    dictToTable['x_H3_H2H2'] = ppXNP_H2H2[4]


    dictToTable['x_H3_H1H2_SM1SM2'] = ppXNPSM_H1H2[3]
    dictToTable['x_H3_H1_SM1_H2_SM2'] = ppXNPSM_H1H2[4]
    dictToTable['x_H3_H1_SM2_H2_SM1'] = ppXNPSM_H1H2[5]

    dictToTable['x_H3_H1H1_SM1SM2'] = ppXNPSM_H1H1[3]
    dictToTable['x_H3_H2H2_SM1SM2'] = ppXNPSM_H2H2[3]


    df = pandas.DataFrame(data = dictToTable)
    fname = outputDir + '/' + outputName
    df.to_csv(fname, sep = "\t")

    XNP = [XNP_H1H2, XNP_H1H1, XNP_H2H2]
    ppXNP = [ppXNP_H1H2, ppXNP_H1H1, ppXNP_H2H2 ]
    ppXNPSM = [ppXNPSM_H1H2, ppXNPSM_H1H1, ppXNPSM_H2H2 ] 
    
    return XNP, ppXNP, ppXNPSM


def pandasReader(path, axis1Key, axis2Key, axis3Key, zKey):

    BP2_df = pandas.read_table(path, index_col=0) 
    axis1 = np.array([i for i in BP2_df[axis1Key]])
    axis2 = np.array([i for i in BP2_df[axis2Key]])
    axis3 = np.array([i for i in BP2_df[axis3Key]])
    z = np.array([i for i in BP2_df[zKey]])

    return axis1, axis2, axis3, z 


def pandasDynamicReader(path, listIndex):

    df = pandas.read_table(path, index_col=0)

    dynamicDict = {}
    for key in listIndex:
        dynamicDict[key] = np.array([i for i in df[key]])

    return dynamicDict


def exclusionCheck(ObsLimList, compareDict, compareKeys, epsilon):

    for key in compareKeys:

        exclList = []
        for i in range(len(ObsLimList)):

            if (compareDict[key])[i] - ObsLimList[i] > epsilon:
                exclList.append({'index': i, 'ObservedLimit': ObsLimList[i], key: (compareDict[key])[i]})
            else:
                pass
  
            # print the excluded mass points
            print('=============================================')
            print('Excluded points ' + key + ': ' + str(exclList))
            print('=============================================')
   

def plotAuxTitleAndBounds2D(title, xtitle, ytitle, ztitle, **kwargs):

    ############################# kwargs #############################

    if ('xlims' in kwargs) and ('ylims' in kwargs):
        plt.xlim(kwargs['xlims'])        
        plt.ylim(kwargs['ylims'])

    elif ('xlims' in kwargs) or ('ylims' in kwargs):
        raise Exception('Either specify both xlims and ylims or none')
    
    else:
        pass
            
    ##################################################################

    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.colorbar(label=ztitle)


def plotAuxVar2D(x, y, n, nInterp=500):
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(n)

    # Set up a regular grid of interpolation points
    xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    xi, yi = np.meshgrid(xi, yi)

    return x, y, z, xi, yi


def plotAuxRegion2D(label1, label2, label3, xyText1, xyText2, xyText3, plot1, plot2, plot3):
    
    plt.plot(plot1[0], plot1[1], ls = 'dashed')
    plt.text(xyText1[0], xyText1[1], label1, size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

    plt.plot(plot2[0], plot2[1], ls = 'dashed')
    plt.text(xyText2[0], xyText2[1], label2, size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))#, rotation=18)

    plt.plot(plot3[0], plot3[1], ls = 'dashed')
    plt.text(xyText3[0], xyText3[1], label3, size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))#, rotation=32)
       

def plotAuxAnnotator2D(xlist, ylist, zlist, fmt, **kwargs):

    ############################# kwargs #############################

    if 'txtcoord' in kwargs:
        txtcoord = kwargs['txtcoord']

    else:
        txtcoord = 'offset points'

    if 'xytxt' in kwargs:
        xytxt = kwargs['xytxt']

    else:
        xytxt = (0,0)

    if 'fontsize' in kwargs:
        fsize = kwargs['fontsize']

    else:
        fsize = 10

    if 'rot' in kwargs:
        rot = kwargs['rot']

    else: 
        rot = 0

    if 'lwidth' in kwargs:
        lwidth = kwargs['lwidt']

    else:
        lwidth = 1.5

    if 'fground' in kwargs:
        fground = kwargs['fground']

    else:
        fground = 'w'
    
    ##################################################################
    
    for i in range(len(zlist)):
        plt.annotate(fmt.format(zlist[i]), (xlist[i], ylist[i]),
                     textcoords = txtcoord, xytext= xytxt, fontsize = fsize, rotation = rot, 
                     path_effects=[mpl.patheffects.withStroke(linewidth=lwidth, foreground=fground)])

    # texts = [plt.text(xlist[i], ylist[i], '{:.1e}'.format(zlist[i]), ha='center', va='center') for i in range(len(zlist))]
    # adjustText.adjust_text(texts)
    
if __name__ == "__main__":

    print('hejsan')

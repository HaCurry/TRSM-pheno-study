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


# pathList = directorySearcher(relPath, '/**/settingsCalc_Nofree*.json')

# dictList = parameterData.dictConstruct(pathList)

# saveTable = {'ms': [], 'mx': [], 'ObservedLimit': [], 'theoryXStot': [], 'theoryXS1': [], 'theoryXS2': []}
# for dictElement in dictList

#     # save the mHa, mHb, mHc mass values in a variable
#     ms = dictElement[msUser]
#     mx = dictElement[mxUser]

#     # save the ObsLim values in a variable
#     ObservedLimit = dictElement['ObservedLimit']

#     # save the TRSM XS values in a variable
#     dataPath = dictElement[dataPathUser]
#     df = pandas.DataFrame(data = dataPath)
#     theoryXStot = [i for i in df[XSUserTot]]
#     theoryXS1 = [i for i in df[XSUser1]]
#     theoryXS2 = [i for i in df[XSUser2]]
    
#     # check if the list elements are the same
#     for element in theoryXS:
#         if abs(theoryXStot[0] - element) > 10**(-8)
#             raise Exception('theoryXStot not equal everywhere')
        
#     for element in theoryXS1:
#         if abs(theoryXS1[0] - element) > 10**(-8)
#             raise Exception('theoryXS1 not equal everywhere')

#     for element in theoryXS2:
#         if abs(theoryXS2[0] - element) > 10**(-8)
#             raise Exception('theoryXS2 not equal everywhere')

#     saveTable['ms'].append(ms)
#     saveTable['mx'].append(mx)
#     saveTable['ObservedLimit'].append(ObservedLimit)
    
# df = pandas.DataFrame(data = saveTable)
# df.to_csv(locOutputData, sep = "\t")

def exclusionCompiler(settingsGlob, dataPath, locOutputData, **kwargs):
    
    #################################### kwargs ####################################

    if 'XStotKey' in kwargs:
        XStotKey = kwargs['XStotKey']

    else:
        XStotKey = 'x_H3_H1H2_SM_tot'


    if 'XS1Key' in kwargs:
        XS1Key = kwargs['XS1Key']

    else:
        XS1Key = 'x_H3_H1H2_SM_1'


    if 'XS2Key' in kwargs:
        XS2Key = kwargs['XS2Key']

    else:
        XS2Key = 'x_H3_H1H2_SM_2'

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
        df = pandas.read_table(dataPath, index_col = 0)
        # print(df)
        listXStot = [i for i in df[XStotKey]]
        listXS1 = [i for i in df[XS1Key]]
        listXS2 = [i for i in df[XS2Key]]

        # check if the scannerS or calculation produced any error
        for element in listXStot:
            if abs(listXStot[0] - element) > 10**(-8):
                raise Exception('theoryXStot not equal everywhere')
        
        for element in listXS1:
            if abs(listXS1[0] - element) > 10**(-8):
                raise Exception('theoryXS1 not equal everywhere')

        for element in listXS2:
            if abs(listXS2[0] - element) > 10**(-8):
                raise Exception('theoryXS2 not equal everywhere')

        XStot = listXStot[0]
        XS1 = listXS1[0]
        XS2 = listXS2[0]

        saveTable['ms'].append(ms)
        saveTable['mx'].append(mx)
        saveTable['ObservedLimit'].append(ObservedLimit)
        saveTable[XStotKey].append(XStot)
        saveTable[XS1Key].append(XS1)
        saveTable[XS2Key].append(XS2)
        print(saveTable['ms'])

    df = pandas.DataFrame(data = saveTable)
    df.to_csv(locOutputData, sep = "\t")


def exclusionPlotter(dataPath, locOutputData, epsilon, **kwargs):

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
        XStotKey = 'x_H3_H1H2_SM_tot'


    if 'XS1Key' in kwargs:
        XS1Key = kwargs['XS1Key']

    else:
        XS1Key = 'x_H3_H1H2_SM_1'


    if 'XS2Key' in kwargs:
        XS2Key = kwargs['XS2Key']

    else:
        XS2Key = 'x_H3_H1H2_SM_2'
    
    
    if 'ObsLimKey' in kwargs:
        ObsLimKey = kwargs['ObsLimKey']

    else:
        ObsLimKey = 'ObservedLimit'
    
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
    plt.show()
    plt.savefig(locOutputData + '/' + ObsLimKey)
    plt.close()

    # plot total-cross section or anything with the column name XStotKey
    plt.scatter(msList, mxList, c=XStotList, cmap='viridis')
    for i in range(len(XStotList)):
        # plt.text(ms[i], mx[i], '{:.3}'.format(limit_obs[i]), fontsize = 8)
        plt.annotate('{:.1e}'.format(XStotList[i]), (msList[i], mxList[i]),
                     textcoords = 'offset points', xytext= (0,0), fontsize = 10, rotation = 0, 
                     path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground="w")])
    plt.title(XStotKey)
    plt.show()
    plt.savefig(locOutputData + '/' + XStotKey)
    plt.close()

    # plot cross-section of first mode or anything with the column name XS1Key
    plt.scatter(msList, mxList, c=XS1List, cmap='viridis')
    for i in range(len(XS1List)):
        # plt.text(ms[i], mx[i], '{:.3}'.format(limit_obs[i]), fontsize = 8)
        plt.annotate('{:.1e}'.format(XS1List[i]), (msList[i], mxList[i]),
                     textcoords = 'offset points', xytext= (0,0), fontsize = 10, rotation = 0, 
                     path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground="w")])
    plt.title(XS1Key)
    plt.show()
    plt.savefig(locOutputData + '/' + XS1Key)
    plt.close()

    # plot cross-section of second mode or anything with the column name XS2Key
    plt.scatter(msList, mxList, c=XS2List, cmap='viridis')
    for i in range(len(XS2List)):
        # plt.text(ms[i], mx[i], '{:.3}'.format(limit_obs[i]), fontsize = 8)
        plt.annotate('{:.1e}'.format(XS2List[i]), (msList[i], mxList[i]),
                     textcoords = 'offset points', xytext= (0,0), fontsize = 10, rotation = 0, 
                     path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground="w")])
    plt.title(XS2Key)
    plt.show()
    plt.savefig(locOutputData + '/' + XS2Key)
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
        
        plt.scatter(X, Y, c = C, cmap='viridis')
        for i in range(len(X)):
            # plt.text(ms[i], mx[i], '{:.3}'.format(limit_obs[i]), fontsize = 8)
            plt.annotate('{:.1e}'.format(C[i]), (X[i], Y[i]),
                         textcoords = 'offset points', xytext= (0,0), fontsize = 10, rotation = 0, 
                         path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground="w")])

        plt.title('{}/{}'.format(keyA, keyB))
        plt.show()
        plt.savefig(locOutputData + '/' + keyA + '_dividedBy_' + keyB)
        plt.close()



if __name__ == "__main__":

    exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP2_check_prel', 'compiled_AtlasBP2_check_prel.tsv',
                      msKey='mHa_ub', mxKey='mHc_ub')   

    exclusionPlotter('compiled_AtlasBP2_check_prel.tsv', 0, 
                     keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1H2_SM_1')

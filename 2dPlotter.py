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


pathList = directorySearcher(relPath, '/**/settingsCalc_Nofree*.json')

dictList = parameterData.dictConstruct(pathList)

saveTable = {'ms': [], 'mx': [], 'ObservedLimit': [], 'theoryXStot': [], 'theoryXS1': [], 'theoryXS2': []}
for dictElement in dictList

    # save the mHa, mHb, mHc mass values in a variable
    ms = dictElement[msUser]
    mx = dictElement[mxUser]

    # save the ObsLim values in a variable
    ObservedLimit = dictElement['ObservedLimit']

    # save the TRSM XS values in a variable
    dataPath = dictElement[dataPathUser]
    df = pandas.DataFrame(data = dataPath)
    theoryXStot = [i for i in df[XSUserTot]]
    theoryXS1 = [i for i in df[XSUser1]]
    theoryXS2 = [i for i in df[XSUser2]]
    
    # check if the list elements are the same
    for element in theoryXS:
        if abs(theoryXStot[0] - element) > 10**(-8)
            raise Exception('theoryXStot not equal everywhere')
        
    for element in theoryXS1:
        if abs(theoryXS1[0] - element) > 10**(-8)
            raise Exception('theoryXS1 not equal everywhere')

    for element in theoryXS2:
        if abs(theoryXS2[0] - element) > 10**(-8)
            raise Exception('theoryXS2 not equal everywhere')

    saveTable['ms'].append(ms)
    saveTable['mx'].append(mx)
    saveTable['ObservedLimit'].append(ObservedLimit)
    
df = pandas.DataFrame(data = saveTable)
df.to_csv(locOutputData, sep = "\t")

def exclusionCompiler(settingsGlob, dataPath, locOutputData):
    
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

    if 'msKey' in kwargs:
        msKey = kwargs['msKey']

    else:
        raise Exception('No msKey given in kwargs')

    if 'mxKey' in kwargs:
        mxKey = kwargs['mxKey']

    else:
        raise Exception('No mxKey given in kwargs')


    ################################################################################

    dictList = parameterData.dictConstruct(pathList)
    saveTable = {'ms': [], 'mx': [], 'ObservedLimit': [], XStotKey: [], XS1Key: [], XS2Key: []}

    for dictElement in dictList:
        
        # save the mHa, mHb, mHc mass values in a variable
        ms = dictElement[msKey]
        mx = dictElement[mxKey]

        # save the ObsLim values in a variable
        ObservedLimit = dictElement['ObservedLimit']

        # save the TRSM XS values in a variable
        dataPath = dictElement[dataPathUser]
        df = pandas.DataFrame(data = dataPath)
        listXStot = [i for i in df[XStotKey]]
        listXS1 = [i for i in df[XS1Key]]
        listXS2 = [i for i in df[XS2Key]]

        # check if the scannerS or calculation produced any error
        for element in listXStot:
            if abs(listXStot[0] - element) > 10**(-8)
                raise Exception('theoryXStot not equal everywhere')
        
        for element in listXS1:
            if abs(listXS1[0] - element) > 10**(-8)
                raise Exception('theoryXS1 not equal everywhere')

        for element in listXS2:
            if abs(listXS2[0] - element) > 10**(-8)
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

    df = pandas.DataFrame(data = saveTable)
    df.to_csv(locOutputData, sep = "\t")


if __name__ == "__main__":

    print('temp')

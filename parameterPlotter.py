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


# NOTE the dominant SMmode changes in BP3 to SMmode = 2!
def sorter(xlist, ylist):
    '''
    Sort xlist first in terms of magnitude. Then sort ylist according to the sorting of xlist.
    returns sorted xlist and ylist as np.arrays
    '''

    xlist = np.array(xlist)
    ylist = np.array(ylist)
    idx = np.argsort(xlist)
    xlist = xlist[idx]
    ylist = ylist[idx]

    return xlist, ylist


def tupleConstruct(dictList, **kwargs):
   
    if 'ShowObsLimit' in kwargs:
        ShowObsLimit = kwargs['ShowObsLimit']

        if isinstance(ShowObsLimit, bool) == True:
            pass

        else:
            raise Exception('ShowObsLimit should be of type Bool')

    else:
        ShowObsLimit = True

    tuplesThs, tuplesThx, tuplesTsx, tuplesVs, tuplesVx, tuplesNofree = [], [], [], [], [], []
    for dictElement in dictList:
        paramFree        = (dictElement)['paramFree']
        pathDataOutput   = (dictElement)['pathDataOutput']
        if ShowObsLimit == True: ObservedLimit    = (dictElement)['ObservedLimit']
        elif ShowObsLimit == False: ObservedLimit = 'empty'
        else: raise Exception('ObsLim invalid value. ObsLim is of type bool')
        dataId           = (dictElement)['dataId']

        # if ShowObsLimit == True: pass

        # elif ShowObsLimit == False: ObservedLimit = 'empty'


        if paramFree == 'thetahS':
            tuplesThs.append((paramFree, pathDataOutput, ObservedLimit, dataId))

        elif paramFree == 'thetahX':
            tuplesThx.append((paramFree, pathDataOutput, ObservedLimit, dataId))

        elif paramFree == 'thetaSX':
            tuplesTsx.append((paramFree, pathDataOutput, ObservedLimit, dataId))

        elif paramFree == 'vs':
            tuplesVs.append((paramFree, pathDataOutput, ObservedLimit, dataId))

        elif paramFree == 'vx':
            tuplesVx.append((paramFree, pathDataOutput, ObservedLimit, dataId))

        elif paramFree == 'Nofree':
            tuplesNofree.append((paramFree, pathDataOutput, ObservedLimit, dataId))

        else:
            raise Exception('invalid value of paramFree found in tupleConstruct')

    return tuplesThs, tuplesThx, tuplesTsx, tuplesVs, tuplesVx, tuplesNofree 



def dudPlot(outputPath, dataId, generalPhysics, axis):
    x = np.linspace(1,5)
    plt.plot(x,x)
    plt.title('pandas.EmptyDataError')
    plt.savefig(outputPath + '/' + dataId + '_' + generalPhysics 
                + '_' + axis + '_dud' + '.png')
    plt.close()
    

def plotter(tuplesVar, outputPath, generalPhysics, title, solo, together, **kwargs):

    #################################### kwargs ####################################

    # for observed limits
    if 'ShowObsLimit' in kwargs:
        ShowObsLimit = kwargs['ShowObsLimit']

        if isinstance(ShowObsLimit, bool) == False:
            raise Exception('ObsLim must be of type bool.')

    else:
        ShowObsLimit = True


    if 'yConstLs' in kwargs:
        yConstLs = kwargs['yConstLs']

        if isinstance(yConstLs, str) == False:
            raise Exception('yConstLs must be of type string in matplotlib linestyle format,\n see matplotlib documentation for more')

    else:
        yConstLs = 'dashed'

    if 'yConstClr' in kwargs:
        yConstClr = kwargs['yConstClr']

        if isinstance(yConstClr, str) == False:
            raise Exception('yConstClr must be of type string in matplotlib linestyle format,\n see matplotlib documentation for more')

    else:
        yConstClr = 'r'

    if 'ls' in kwargs:
        ls = kwargs['ls']

    else:
        ls = 'solid'

    if 'marker' in kwargs:
        marker = kwargs['marker']

    else:
        marker = '.'

    if 'yscale' in kwargs:

        if kwargs['yscale'] == 'log':
            yscaleLog = True

        else:
            raise Exception('invalid yscale value, only yscale = \'log\' is valid.')

    else:
        yscaleLog = False

    if 'saveStep' in kwargs:
        saveStep = kwargs['saveStep']
        if isinstance(saveStep, bool) == False:
            raise Exception('saveStep needs to be of type bool')

    else:
        saveStep = False

    if 'fext' in kwargs:
        fext = kwargs['fext']
        if isinstance(fext, str) == False:
            raise Exception('fext needs to be a string in the format .[fileextension (pdf, png, etc.)] .')

    else:
        fext = '.png'

################################################################################

    if not os.path.isdir(outputPath):
       os.makedirs(outputPath)

    xlimsDict = {'thetahS': (-np.pi/2, np.pi/2), 'thetahX': (-np.pi/2, np.pi/2), 'thetaSX': (-np.pi/2, np.pi/2), 'vs': (1, 1000), 'vx': (1, 1000), 'Nofree': (1, 1000)}
    # axisDict = {'thetahS': 'thetahS', 'thetahX': 'thetahX', 'thetaSX': 'thetaSX', 'vs': 'vs', 'vx': 'vx', 'Nofree': 'mH1'}

    if together == True:

        plt.figure()
        for (x, y, axis, ObservedLimit, dataId) in tuplesVar:
            # print(x,y, dataId)
            plt.plot(x,y, ls=ls, marker=marker)

            if 'ylims' in kwargs:
                ylims = kwargs['ylims']
                plt.ylim(ylims)

            else:
                pass

            plt.xlim(xlimsDict[axis])

        if yscaleLog == True: 
            plt.yscale('log')

        plt.savefig(outputPath + '/' + generalPhysics + '_' + title + fext )
        plt.close()

        if saveStep == True: 

            plt.figure()
            if 'ylims' in kwargs:
                ylims = kwargs['ylims']
                plt.ylim(ylims)

            else:
                pass

            plt.xlim(xlimsDict[axis])

            if yscaleLog == True: 
                plt.yscale('log')

            figNr = 0
            for (x, y, axis, ObservedLimit, dataId) in tuplesVar:

                plt.plot(x,y, ls=ls, marker=marker)
                if ShowObsLimit == True: yaxis = plt.axhline(y=ObservedLimit, ls=yConstLs, color=yConstClr)


                plt.title(axis + ' ' + dataId)
                plt.savefig(outputPath + '/' + generalPhysics + '_' + title + '_' + str(figNr) + fext)
                if ShowObsLimit == True: yaxis.remove()
                figNr = figNr + 1

            plt.close()

    if solo == True:

        soloDir = outputPath + '/' + 'solo'
        if not os.path.isdir(soloDir):
           os.makedirs(soloDir)

        for (x, y, axis, ObservedLimit, dataId) in tuplesVar:

            plt.figure()
            plt.xlim(xlimsDict[axis])
            if 'ylims' in kwargs:
                ylims = kwargs['ylims']
                plt.ylim(ylims)

            else:
                pass

            if yscaleLog == True: 
                plt.yscale('log')

            plt.plot(x,y, ls=ls, marker=marker)
            if ShowObsLimit == True: yaxis = plt.axhline(y=ObservedLimit, ls=yConstLs, color=yConstClr)

            plt.title(axis + ' ' + dataId)
            plt.savefig(soloDir + '/' + dataId + '_' + generalPhysics + '_' + title + '_' + axis + fext)
            plt.close()


def parameterPlot(relPath, settingsGlob, locOutputPath, XNPNP, together, solo, **kwargs):

    #################################### kwargs ####################################

    if ('XNP' not in kwargs) and ('ppXNP' not in kwargs) and ('ppXNPSM' not in kwargs):
        raise Exception('Please provide physical quantity. \nSet one of \'XNP\', \'ppXNP\', \'ppXNPSM\' to True ')

    else:

        if 'XNP' in kwargs:

            XNP = kwargs['XNP']
            if isinstance[XNP, bool] == False:
                raise Exception('XNP need to be of type bool')

            else: pass

        else: XNP = False

        if 'ppXNP' in kwargs:

            ppXNP = kwargs['ppXNP']
            if isinstance[ppXNP, bool] == False:
                raise Exception('ppXNP need to be of type bool')

            else: pass

        else: ppXNP = False

        if 'ppXNPSM' in kwargs:

            ppXNPSM = kwargs['ppXNPSM']
            if isinstance(ppXNPSM, bool) == False:
                raise Exception('ppXNPSM need to be of type bool')

            else: pass

            if 'ppXNPSM' in kwargs:

                # if ppXNPSM is given and user not defined SM final states, raise exception
                if ('SM1' not in kwargs) and ('SM2' not in kwargs):
                    raise Exception('ppXNPSM is True but SM1 and SM2 not given.')

                # otherwise continue as normal
                else:
                    pass

                if ('SMmode' not in kwargs):
                    raise Exception('ppXNPSM is True but SMmode is not given. \nPossible values are the *strings* \'1\',\'2\', \'tot\'.')

                else:
                    SMmode = kwargs['SMmode']
                    if isinstance(SMmode, str) == False:
                        raise Exception('SMmode need to be H1_SM1_H2_SM2 or H1H2_SM1SM2 if XNPNP = H1H2 and H1H1_SM1SM2 or H2H2_SM1SM2 if XNPNP = H1H1 or XNPNP = H2H2')

        else: ppXNPSM = False

    if together == False and solo == False:
        raise Exception('Both together and solo cannot be set to false')

    else:
        pass

    ##############################################################

    print('*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*')
    print(' Starting script parameterPlot ')
    print('*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*')
    
    # find paths to JSON files and store them in a list as dicts
    pathList = parameterData.directorySearcher(relPath, settingsGlob)
    if len(pathList) == 0: raise Exception('No paths found')
    dictList = parameterData.dictConstruct(pathList)

    # will be used for the plotting
    tuplesThs = []
    tuplesThx = []
    tuplesTsx = []
    tuplesVs = []
    tuplesVx = []
    tuplesNofree = []

    print('Creating tuples ...')
    loading = len(dictList)
    loadingStep = 0

    # loop over the dicts and store the data in the appropriate list of tuples
    for dictElement in dictList:
        paramFree, pathDataOutput, dataId = dictElement['extra']['paramFree'], dictElement['extra']['pathDataOutput'], dictElement['extra']['dataId']

        # store observed limit in a variable if exists
        if 'ObservedLimit' in dictElement['extra']:
            ObservedLimit = dictElement['extra']['ObservedLimit']

        # otherwise save it as 'empty'
        else:
            ObservedLimit = 'empty'

        # save all paths found in settings file
        if XNPNP == 'H1H2':
            path_XNP     = dictElement['extra']['pathCalcXNP_H1H2_']
            path_ppXNP   = dictElement['extra']['pathCalcppXNP_H1H2_']
            path_ppXNPSM = dictElement['extra']['pathCalcppXNPSM_H1H2_']

        elif XNPNP == 'H1H1':
            path_XNP     = dictElement['extra']['pathCalcXNP_H1H1_']
            path_ppXNP   = dictElement['extra']['pathCalcppXNP_H1H1_']
            path_ppXNPSM = dictElement['extra']['pathCalcppXNPSM_H1H1_']

        elif XNPNP == 'H2H2':
            path_XNP     = dictElement['extra']['pathCalcXNP_H2H2_']
            path_ppXNP   = dictElement['extra']['pathCalcppXNP_H2H2_']
            path_ppXNPSM = dictElement['extra']['pathCalcppXNPSM_H2H2_']

        else:
            raise Exception('Invalid value for XNPNP not given. Possible values of XNPNP are \'H1H2\', \'H1H1\', \'H2H2\'')

        # variables needed when reading the data using pandas
        if XNP == True:
            yKey = 'b_H3_' + XNPNP
            path = path_XNP

        elif ppXNP == True:
            yKey = 'x_H3_' + XNPNP
            path = path_ppXNP

        elif ppXNPSM == True:
            # yKey = 'x_H3_' + XNPNP + '_' + 'SM_' + SMmode
            yKey = 'x_H3_' + SMmode
            path = path_ppXNPSM

        else:
            raise Exception('Neither XNP, ppXNP, ppXNPSM set to True')

        df = pandas.read_table(path, index_col = 0)
        # x = [i for i in df[paramFree]]
        # y = [i for i in df[yKey]]
        x = df[paramFree]
        y = df[yKey]

        if paramFree == 'thetahS':
            tuplesThs.append((x, y, paramFree, ObservedLimit, dataId))

        elif paramFree == 'thetahX':
            tuplesThx.append((x, y, paramFree, ObservedLimit, dataId))

        elif paramFree == 'thetaSX':
            tuplesTsx.append((x, y, paramFree, ObservedLimit, dataId))

        elif paramFree == 'vs':
            tuplesVs.append((x, y, paramFree, ObservedLimit, dataId))

        elif paramFree == 'vx':
            tuplesVx.append((x, y, paramFree, ObservedLimit, dataId))

        elif paramFree == 'Nofree':
            tuplesNofree.append((x, y, paramFree, ObservedLimit, dataId))

        else:
            raise Exception('Error ocurred in creating tuples')

        print(str(loadingStep/loading))
        loadingStep = loadingStep + 1

    # store all tuples together to be looped over for plotting
    tuplesAll = [tuplesThs, tuplesThx, tuplesTsx, tuplesVs, tuplesVx, tuplesNofree]

    # part of the filename of the figures being saved
    if XNP == True: generalPhysics = 'XNP'

    elif ppXNP == True: generalPhysics = 'ppXNP'

    elif ppXNPSM == True: generalPhysics = 'ppXNPSM'

    else: raise Exception('XNP, ppXNP, ppXNPSM not given')

    print('creating plots...')
    # for tuplesVar in tuplesAll:
    plotter(tuplesThs, locOutputPath, generalPhysics, XNPNP + '_thetahS', solo, together, **kwargs)
    plotter(tuplesThx, locOutputPath, generalPhysics, XNPNP + '_thetahX', solo, together, **kwargs)
    plotter(tuplesTsx, locOutputPath, generalPhysics, XNPNP + '_thetaSX', solo, together, **kwargs)
    plotter(tuplesVs, locOutputPath, generalPhysics, XNPNP + '_vs', solo, together, **kwargs)
    plotter(tuplesVx, locOutputPath, generalPhysics, XNPNP + '_vx', solo, together, **kwargs)
    plotter(tuplesNofree, locOutputPath, generalPhysics, XNPNP + '_Nofree', solo, together, **kwargs)

    print('*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*')
    print(' script finished parameterPlot ')
    print('*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*')
    


if __name__ == "__main__":

    # Deprecated, moved to oneD_AtlasLimitsPlot.py
    # parameterPlot('calc_AtlasBP2_check_prel', '/**/settingsCalc_*.json', 'plot_AtlasBP2_check_prel', 'H1H2', True, True, 
                  # ppXNPSM=True,ShowObsLimit=True, SM1='bb', SM2='gamgam', SMmode='1', saveStep=True, yscale='log', ylims=(10**(-6),8*10**(-2)))
    print('tjenare')
# ppXNPSM

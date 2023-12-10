# -*- coding: utf-8 -*-
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


# NOTE the dominant SMmode changes in BP3 to SMmode = 2!
def dataGenerator(generalPhysics, axis, path, **kwargs):
    '''
    Pulls data from path with an assumed free axis and calculates physical
    quantities defined by generalPhysics using the module functions.py.
    Returns as lists of lists.

    generalPhysics can be XNP, ppXNP, ppXNPSM
    axis is the desired axis of the physical quantity
    path is the path to the data
    **kwargs need to define SM1 SM2 if generalPhysics = ppXNPSM.
             User can also give additional axes in axis2, axis3.
             User can give normalization of ppXNP, default set to 1.
             User can give normalization of ppXNPSM, default set to 1.

    returns: H1H2, H1H1, H2H2, where each array contains elements with the axis
             list and the physical quantity
             eg. for XNP, H1H2 = np.array([axis, axis2, axis3, b_H3_H1H2])
    '''

    ########################    kwargs    ########################

    if (generalPhysics == 'ppXNPSM'):

        if 'SM1' and 'SM2' in kwargs:
            SM1, SM2 = kwargs['SM1'], kwargs['SM2']

        else:
            raise Exception('No SM final state chosen in plotter, please define SM1 and SM2 in kwargs')

    if 'axis2' in kwargs:
        axis2 = kwargs['axis2']

    else:
        axis2 = 'mH2'

    if 'axis3' in kwargs:
        axis3 = kwargs['axis3']

    else:
        axis3 = 'mH3'

    # rescale ppXSH, ppXHH, ppXSS cross-section.  
    # Default set to SM di-Higgs cross-section 31.02 * 10**(-3)
    if 'ggF_xs_SM_Higgs' in kwargs:
        ggF_xs_SM_Higgs = kwargs['ggF_xs_SM_Higgs']

    else:
        # rescaled SM dihiggs cross-section (ggF): 31.02 * 10**(-3)
        # https://cds.cern.ch/record/2764447/files/ATL-PHYS-SLIDE-2021-092.pdf
        # Default set to 1
        ggF_xs_SM_Higgs = 1

    # Rescale SM1SM2 cross-section
    # Default set to 1 (no rescaling ocurrs)
    if 'ggF_xs_SM_Higgs_SM1SM2' in kwargs:
        ggF_xs_SM_Higgs_SM1SM2 = kwargs['ggF_xs_SM_Higgs_SM1SM2']

    else:
        ggF_xs_SM_Higgs_SM1SM2 = 1

    ##############################################################

    if generalPhysics == 'XNP':
        H1H2, H1H1, H2H2, x_H3_gg = TRSM.XNP_massfree(path, axis, axis2, axis3)

    elif generalPhysics == 'ppXNP':
        H1H2, H1H1, H2H2 = TRSM.ppXNP_massfree(path, axis, axis2, axis3, 
                                               normalizationNP=ggF_xs_SM_Higgs)

    elif generalPhysics == 'ppXNPSM':
        H1H2, H1H1, H2H2 = TRSM.ppXNPSM_massfree(path, axis, axis2, axis3, 
                                                 SM1, SM2, 
                                                 normalizationSM=ggF_xs_SM_Higgs_SM1SM2)

    else:
        raise Exception('No general physics chosen')

    return H1H2, H1H1, H2H2


def directorySearcher(relPath, globPathname):
    '''
    relPath string. relative path to directory where glob searches.
    globPathname string. the files in glob format.

    returns: relative paths in listPaths.
    '''
    relListPaths = glob.glob(relPath + '/' + globPathname, recursive=True)

    return relListPaths


def auxSoloPlot(xlims, ylims, path, filename, yConst, **kwargs):
    '''
    Plots and saves figure in the ranges xlims and ylims.

    path. string. directory to save figure. Saves the plot in the directory path.

    filename. name of the file. Saves the figure with file name filename.

    ylims. tuple. y-limit bounds. Values can be set to None, and matplotlib auto sets the bound

    xlims. tuple. x-limit bounds. Values can be set to None, and matplotlib auto sets the bound

    kwarg yConst. int/float. default nothing. plots a constant line at y = yConst.

        kwarg yConstLs. string. default 'dashed'. dependent on yConst, linestyle of yConst 

        kwarg yConstClr. string. default 'r'. dependent on yConst, color of yConst

    kwarg yscale. string. Can only be set to 'log' otherwise raises error.

    kwarg show. bool. If True, script will plot the figure with gui, otherwise does nothing
    '''

    #################################### kwargs ####################################

    # for observed limits
    if yConst is None:
        pass

    else:

        if 'yConstLs' in kwargs:
            yConstLs = kwargs['yConstLs']
            if isinstance(yConstLs, str):
                raise Exception('yConstLs must be of type string in matplotlib linestyle format,\n see matplotlib documentation for more')

        else:
            yConstLs = 'dashed'

        if 'yConstClr' in kwargs:
            yConstClr = kwargs['yConstClr']
            if isinstance(yConstClr, str):
                raise Exception('yConstClr must be of type string in matplotlib linestyle format,\n see matplotlib documentation for more')
        else:
            yConstClr = 'r'

        plt.axhline(y=yConst, color=yConstClr, linestyle=yConstLs)    

    # for cross-sections
    if 'yscale' in kwargs:

        if kwargs['yscale'] == 'log':
            plt.yscale('log')

        else:
            raise Exception('invalid yscale value, only yscale = \'log\' is valid.')

    # plots figure using gui
    if 'show' in kwargs:

        if kwargs['show'] == True:
            show = True

        elif kwargs['show'] == False:
            show = False

        else:
            raise Exception('show set to invalid value in auxSoloPlot')

    else:
        show = False

    if 'fext' in kwargs:
        fext = kwargs['fext']

    else:
        fext = '.png'
        

################################################################################

    # if one of the bounds set to none then use matplotlib auto settings
    plt.xlim(left=xlims[0], right=xlims[1])
    plt.ylim(bottom=ylims[0], top=ylims[1])

    plt.savefig(path + '/' + filename + fext)

    if show == True:
        plt.show()
        plt.close()

    else:
        plt.close()


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


def definer(generalPhysics, axis, path, **kwargs):
    '''
    produces all list elements from dataGenerator in a nice format
    '''

    # user decides the desired decay mode           (S -> bb, H -> gamgam) or (H -> bb, S -> gamgam)
    # default is set to both decay modes summed     (S -> bb, H -> gamgam) + (H -> bb, S -> gamgam)
    if generalPhysics == 'ppXNPSM':

        if 'modeSM' in kwargs:
            modeSM = kwargs['modeSM']

        else:
            modeSM = 3

    elif generalPhysics != 'ppXNPSM':

        if 'modeSM' in kwargs:
            raise Exception('modeSM decided but general physics is not ppXNPSM.\nPlease remove modeSM from function call if \ngeneralPhysics!=ppXNPSM')

        else:
            pass

    else:
        pass

    H1H2, H1H1, H2H2 = dataGenerator(generalPhysics, axis, path, **kwargs)

    xlist_H1H2, ylist_H1H2 = sorter(H1H2[0], H1H2[modeSM])
    # ylist_H1H2 = H1H2[modeSM]

    xlist_H1H1, ylist_H1H1 = sorter(H1H1[0], H1H1[3])
    # ylist_H1H1 = H1H1[3]

    xlist_H2H2, ylist_H2H2 = sorter(H2H2[0], H2H2[3])
    # ylist_H2H2 = H2H2[3]

    return (xlist_H1H2, ylist_H1H2), (xlist_H1H1, ylist_H1H1), (xlist_H2H2, ylist_H2H2)


def dictConstruct(paths, key):

    dictList = []
    
    for pathVar in paths:
        
        with open(pathVar) as f:
            contentsJSON = json.load(f)
        
        dictList.append(contentsJSON[key])

    return dictList


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
        ObservedLimit    = (dictElement)['ObservedLimit']
        dataId           = (dictElement)['dataId']

        if ShowObsLimit == True: pass

        elif ShowObsLimit == False: ObservedLimit = None

        else: raise Exception('ObsLim invalid value. ObsLim is of type bool')

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
    

def soloPlot(generalPhysics, axis, xlims, ylims, dataPath, outputPath, yConst, dataId, **kwargs):

    if 'ls' in kwargs:
        ls = kwargs['ls']

    else:
        ls = 'None'

    if 'marker' in kwargs:
        marker = kwargs['marker']

    else:
        marker = 'None'
    

    # repackages data from dataGenerator to a nice format and sorts the lists according to the xlists
    (xlist_H1H2, ylist_H1H2), (xlist_H1H1, ylist_H1H1), (xlist_H2H2, ylist_H2H2) = definer(generalPhysics, axis, dataPath, **kwargs)

    # from stackexchange:  https://stackoverflow.com/a/1274436/17456342
    if not os.path.isdir(outputPath):
       os.makedirs(outputPath)

    else:
        pass

    outputPathH1H2 = outputPath + '/' + 'H1H2'
    outputPathH1H1 = outputPath + '/' + 'H1H1'
    outputPathH2H2 = outputPath + '/' + 'H2H2'

    if not os.path.isdir(outputPathH1H2):
       os.makedirs(outputPathH1H2)

    else:
        pass

    if not os.path.isdir(outputPathH1H1):
       os.makedirs(outputPathH1H1)

    else:
        pass

    if not os.path.isdir(outputPathH2H2):
       os.makedirs(outputPathH2H2)

    else:
        pass
    # fix this: maybe make function out this repeated process 
    filename_H1H2 = dataId + '_' + generalPhysics+ '_' + axis + '_H1H2'
    filename_H1H1 = dataId + '_' + generalPhysics+ '_' + axis + '_H1H1'
    filename_H2H2 = dataId + '_' + generalPhysics+ '_' + axis + '_H2H2'

    # if yConst == 'None':
    #     pass

    # else:
    #     kwargs['yConst'] = yConst
    
    # fix this: maybe make function out this repeated process 
    plt.close()
    plt.plot(xlist_H1H2, ylist_H1H2, marker=marker, ls=ls)
    auxSoloPlot(xlims, ylims, outputPathH1H2 , filename_H1H2, yConst, **kwargs)

    plt.close()
    plt.plot(xlist_H1H1, ylist_H1H1, marker=marker, ls=ls)
    auxSoloPlot(xlims, ylims, outputPathH1H1 , filename_H1H1, yConst, **kwargs)

    plt.close()
    plt.plot(xlist_H2H2, ylist_H2H2, marker=marker, ls=ls)
    auxSoloPlot(xlims, ylims, outputPathH2H2 , filename_H2H2, yConst, **kwargs)


def parameterPlotterSolo(relPath, outputPath, settingsGlob, generalPhysics, xlims, ylims, **kwargs):

    #################################### kwargs ####################################

    # For debugging purposes, not necessary for the user
    # sets the number of tuples to loop over. For testing 
    # set numFigs to a small integer.
    if ('figStart' in kwargs) and ('figEnd' in kwargs):
        figStart, figEnd = kwargs['figStart'], kwargs['figEnd']

    else:
        figStart, figEnd = None, None

    if 'ShowObsLimit' in kwargs:
        ShowObsLimit = kwargs['ShowObsLimit']

        if isinstance(ShowObsLimit, bool) == True:
            pass

        else:
            raise Exception('ShowObsLimit should be of type Bool')

    else:
        ShowObsLimit = True

    ################################################################################

    outputPaths = directorySearcher(relPath, settingsGlob)
    if len(outputPaths) == 0: raise Exception('did not find any files with name ' + settingsGlob)
    dictList = dictConstruct(outputPaths, 'extra')

    tuplesThs, tuplesThx, tuplesTsx, tuplesVs, tuplesVx, tuplesNofree = tupleConstruct(dictList, ShowObsLimit)
    allTuples = [tuplesThs, tuplesThx, tuplesTsx, tuplesVs, tuplesVx, tuplesNofree]

    xlimsDict = {'thetahS': (-np.pi/2, np.pi/2), 'thetahX': (-np.pi/2, np.pi/2), 'thetaSX': (-np.pi/2, np.pi/2), 'vs': (1, 1000), 'vx': (1, 1000), 'Nofree': (None, None)}
    axisDict = {'thetahS': 'thetahS', 'thetahX': 'thetahX', 'thetaSX': 'thetaSX', 'vs': 'vs', 'vx': 'vx', 'Nofree': 'mH1'}
    loadstep, loading = 1, len(tuplesThs) + len(tuplesThx) + len(tuplesTsx) + len(tuplesVs) + len(tuplesVx) + len(tuplesNofree)
    for tupleVar in allTuples:

        for (axis, dataPath, ObservedLimit, dataId) in tupleVar:

            try:
                soloPlot(generalPhysics, axisDict[axis], xlimsDict[axis], ylims, dataPath, outputPath, ObservedLimit, dataId, **kwargs)

            except pandas.errors.EmptyDataError:
                dudPlot(outputPath, dataId, generalPhysics, axis)

            print('Loading {}'.format(int(loadstep/loading * 100)))
            loadstep = loadstep + 1


def listAppender(tuples, generalPhysics, **kwargs):

    axisDict = {'thetahS': 'thetahS', 'thetahX': 'thetahX', 'thetaSX': 'thetaSX', 'vs': 'vs', 'vx': 'vx', 'Nofree': 'mH1'}
    together_H1H2, together_H1H1, together_H2H2 = [], [], []

    for (axis, dataPath, ObservedLimit, dataId) in tuples:

        try:
            (xlist_H1H2, ylist_H1H2), (xlist_H1H1, ylist_H1H1), (xlist_H2H2, ylist_H2H2) = definer(generalPhysics, axisDict[axis], dataPath, **kwargs)

        except pandas.errors.EmptyDataError:
            (xlist_H1H2, ylist_H1H2), (xlist_H1H1, ylist_H1H1), (xlist_H2H2, ylist_H2H2) = ([],[]), ([],[]), ([], [])

        together_H1H2.append((xlist_H1H2, ylist_H1H2, axis, ObservedLimit, dataId))
        together_H1H1.append((xlist_H1H1, ylist_H1H1, axis, ObservedLimit, dataId))
        together_H2H2.append((xlist_H2H2, ylist_H2H2, axis, ObservedLimit, dataId))

    return together_H1H2, together_H1H1, together_H2H2


def togetherPlot(together_HiggsHiggs, outputPath, generalPhysics, title, **kwargs):

    #################################### kwargs ####################################

    # for observed limits
    if 'ShowObsLimit' in kwargs:
        ShowObsLimit = kwargs['ShowObsLimit']

        if isinstance(ShowObsLimit, bool) == False:
            raise Exception('ObsLim must be of type bool.')

    else:
        ShowObsLimit = False


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

    if 'ylims' in kwargs:
        ylims = kwargs['ylims']

    else:
        ylims = (None, None)

    ################################################################################

    if not os.path.isdir(outputPath):
       os.makedirs(outputPath)

    xlimsDict = {'thetahS': (-np.pi/2, np.pi/2), 'thetahX': (-np.pi/2, np.pi/2), 'thetaSX': (-np.pi/2, np.pi/2), 'vs': (1, 1000), 'vx': (1, 1000), 'Nofree': (None, None)}
    axisDict = {'thetahS': 'thetahS', 'thetahX': 'thetahX', 'thetaSX': 'thetaSX', 'vs': 'vs', 'vx': 'vx', 'Nofree': 'mH1'}

    ymin, ymax = 0
    for (x, y, axisDicts, ObservedLimit, dataId) in together_HiggsHiggs:

        plt.plot(x,y, ls=ls, marker=marker)

        if (not ObservedLimit is None) and (2 * ObservedLimit > ymax):
            ymax = 2 * ObservedLimit

        elif (ObservedLimit is None) and (2 * max(y) > ymax):
            ymax = 2 * max(y)
            

    xmin, xmax = plt.xlim(xlimsDict[axis])
    ylims = plt.gca().get_ylim()
    # ybounds = plt.gca().get_ylim()

    print(xlims, ylims)

    if yscaleLog == True: 
        plt.yscale('log')

    plt.savefig(outputPath + '/' + generalPhysics + '_' + title + fext )
    plt.close()

    if saveStep == True: 
        plt.figure()
        plt.xlim(xlims)
        plt.ylim(ylims)
        if yscaleLog == True: 
            plt.yscale('log')

        figNr = 0
        for (x, y, axis, ObservedLimit, dataId) in together_HiggsHiggs:

            plt.plot(x,y, ls=ls, marker=marker)
            if ShowObsLimit == True: yaxis = plt.axhline(y=ObservedLimit, ls=yConstLs, color=yConstClr)


            plt.title(axis + ' ' + dataId)
            plt.savefig(outputPath + '/' + generalPhysics + '_' + title + '_' + str(figNr) + fext)
            if ShowObsLimit == True: yaxis.remove()
            figNr = figNr + 1

        plt.close()



def togetherPlotWrapper(tuplesVar, outputPath, generalPhysics, title, **kwargs):

    togetherVar_H1H2, togetherVar_H1H1, togetherVar_H2H2 = listAppender(tuplesVar, generalPhysics, **kwargs)
    togetherPlot(togetherVar_H1H2, outputPath, generalPhysics, 'H1H2_' + title, **kwargs)
    togetherPlot(togetherVar_H1H1, outputPath, generalPhysics, 'H1H1_' + title, **kwargs)
    togetherPlot(togetherVar_H2H2, outputPath, generalPhysics, 'H2H2_' + title, **kwargs)


def parameterPlotterTogether(relPath, outputPath, settingsGlob, generalPhysics, **kwargs):

    #################################### kwargs ####################################

    # For debugging purposes, not necessary for the user
    # sets the number of tuples to loop over. For testing 
    # set numFigs to a small integer.
    if ('figStart' in kwargs) and ('figEnd' in kwargs):
        figStart, figEnd = kwargs['figStart'], kwargs['figEnd']

    else:
        figStart, figEnd = None, None

    
    if ('thetahS' in kwargs) or ('thetahX' in kwargs) or ('thetaSX' in kwargs) or ('vs' in kwargs) or ('vx' in kwargs) or ('Nofree' in kwargs) or ('all' in kwargs):

        if 'thetahS' in kwargs:
            thetahS = kwargs['thetahS']
            if isinstance(thetahS, bool) == False:
                raise Exception('thetahS set to non bool value')
        else: thetahS = False

        if 'thetahX' in kwargs:
            thetahX = kwargs['thetahX']
            if isinstance(thetahX, bool) == False:
                raise Exception('thetahX set to non bool value')
        else: thetahX = False

        if 'thetaSX' in kwargs:
            thetaSX = kwargs['thetaSX']
            if isinstance(thetaSX, bool) == False:
                raise Exception('thetaSX set to non bool value')
        else: thetaSX = False

        if 'vs' in kwargs: 
            vs = kwargs['vs']
            if isinstance(vs, bool) == False:
                raise Exception('vs set to non bool value')
        else: vs = False

        if 'vx' in kwargs: 
            vx = kwargs['vx']
            if isinstance(vx, bool) == False:
                raise Exception('vx set to non bool value')
        else: vx = False

        if 'Nofree' in kwargs: 
            Nofree = kwargs['Nofree']
            if isinstance(Nofree, bool) == False:
                raise Exception('Nofree set to non bool value')
        else: Nofree = False

        if 'all' in kwargs: 
            all = kwargs['all']
            if isinstance(all, bool) == False:
                raise Exception('all set to non bool value')
        else: all = False

    else:
        raise Exception('no free parameter given. \nPlease specify a boolean value to either or some of thetahS, thetahX, thetaSX, vs, vx, Nofree \nor specif all = True for all paramters.')

    

    ################################################################################

    outputPaths = directorySearcher(relPath, settingsGlob)
    dictList = dictConstruct(outputPaths, 'extra')
    tuplesThs, tuplesThx, tuplesTsx, tuplesVs, tuplesVx, tuplesNofree = tupleConstruct(dictList, **kwargs)
    allTuples = [tuplesThs, tuplesThx, tuplesTsx, tuplesVs, tuplesVx, tuplesNofree]

    if thetahS == True:

        togetherPlotWrapper(tuplesThs, outputPath, generalPhysics, 'thetahS', **kwargs)

    else:
        pass

    if thetahX == True:
        togetherPlotWrapper(tuplesThx, outputPath, generalPhysics, 'thetahX', **kwargs)

    else:
        pass

    if thetaSX == True:
        togetherPlotWrapper(tuplesTsx, outputPath, generalPhysics, 'thetaSX', **kwargs)

    else:
        pass

    if vs == True:
        togetherPlotWrapper(tuplesVs, outputPath, generalPhysics, 'vs', **kwargs)

    else:
        pass
    
    if vx == True:
        togetherPlotWrapper(tuplesVx, outputPath, generalPhysics, 'vx', **kwargs)
        
    else:
        pass

    if Nofree == True:
        togetherPlotWrapper(tuplesNofree, outputPath, generalPhysics, 'Nofree', **kwargs)

    else:
        pass

    if all == True:
        togetherPlotWrapper(tuplesThs, outputPath, generalPhysics, 'thetahS', **kwargs)
        togetherPlotWrapper(tuplesThx, outputPath, generalPhysics, 'thetahX', **kwargs)
        togetherPlotWrapper(tuplesTsx, outputPath, generalPhysics, 'thetaSX', **kwargs)
        togetherPlotWrapper(tuplesVs, outputPath, generalPhysics, 'vs', **kwargs)
        togetherPlotWrapper(tuplesVx, outputPath, generalPhysics, 'vx', **kwargs)
        togetherPlotWrapper(tuplesNofree, outputPath, generalPhysics, 'Nofree', **kwargs)
        print(tuplesNofree)
    else:
        pass



if __name__ == "__main__":

    # parameterPlotterSolo('AtlasBP2_check_prel2', 'plot_AtlasBP2_check_prel2', '/**/settings_*.json', 'ppXNPSM', (None, None), (None, None),
                         # marker='.', ls='solid', SM1='bb', SM2='gamgam', figStart=None, figEnd=None, SMmode=4, yscale='log') 

    parameterPlotterTogether('AtlasBP2_check_prel2', 'togetherTest4','/**/settings_*.json', 'ppXNPSM', SM1='bb', SM2='gamgam', 
                             thetahS=True, saveStep=True, ShowObsLimit=True, ylims=(None, 2 * 3.9 * 10**(-2)), yscale='log')

    # parameterPlotterSolo('AtlasBP2_check_prel2', 'tabort', '/**/settings_Nofree_S70.0-X300.0.json', 'ppXNPSM', (None, None), (None, None),
                         # marker='.', ls='solid', SM1='bb', SM2='gamgam', figStart=None, figEnd=None, SMmode=4, yscale='log', show=True) 


    # parameterPlotterMain('AtlasBP3_check_prel', 'plot_AtlasBP3_check_prel', '/**/settings_*.json', 'ppXNPSM', (None, None), (None, None), True, False, 
	   #                      marker='.', ls='solid', SM1='bb', SM2='gamgam', figStart=None, figEnd=None, SMmode=5)

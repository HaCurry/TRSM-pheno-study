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
            linestyle = kwargs['yConstLs']

        else:
            ls = 'dashed'

        if 'yConstClr' in kwargs:
            clr = kwargs['yConstClr']

        else:
            clr = 'r'

        plt.axhline(y=yConst, color=clr, linestyle=ls)    

    # for cross-sections
    if 'yscale' in kwargs:

        if kwargs['yscale'] == 'log':
            plt.yscale('log')

        else:
            raise Exception('invalid log scale parameterPlot')

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


def soloPlot(generalPhysics, axis, xlims, ylims, dataPath, outputPath, yConst, dataId, **kwargs):

    # fix this: this is not a nice solution
    # if 'yConst' in kwargs:
    #     kwargs['yConst'] = ObservedLimit

    # else:
    #     pass

    # if yConst is None:
    #     pass

    # else:
    #     kwargs['yConst'] = yConst

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


def parameterPlotterMain(relPath, outputPath, settingsGlob, generalPhysics, xlims, ylims, solo, together, **kwargs):

    #################################### kwargs ####################################

    # For debugging purposes, not necessary for the user
    # sets the number of tuples to loop over. For testing 
    # set numFigs to a small integer.
    if ('figStart' in kwargs) and ('figEnd' in kwargs):
        figStart, figEnd = kwargs['figStart'], kwargs['figEnd']

    else:
        figStart, figEnd = None, None

    if 'ObsLim' in kwargs:
        ObsLim = kwargs['ObsLim']

        if isinstance(ObsLim, bool) == True:
            pass

        else:
            raise Exception('ObsLim should be of type Bool')

    else:
        ObsLim = True

    ################################################################################

    outputPaths = directorySearcher(relPath, settingsGlob)
    dictList = dictConstruct(outputPaths, 'extra')

    if ObsLim == True:
                    # axis                     # dataPath                    # ObservedLimit                 # dataId
        tuples = [( (dictList[i])['paramFree'], (dictList[i])['pathDataOutput'], (dictList[i])['ObservedLimit'], (dictList[i])['dataId'] ) for i in range(len( dictList))]
        # print(tuples[0:2])
    else:
                    # axis                     # dataPath                    # ObservedLimit                 # dataId
        tuples = [( (dictList[i])['paramFree'], (dictList[i])['pathDataOutput'], None, (dictList[i])['dataId'] ) for i in range(len( dictList))]

    tuples = tuples[figStart:figEnd]

    loading = len(tuples)
    loadstep = 1
    
    if solo == True:
        for (axis, dataPath, ObservedLimit, dataId) in tuples:

            if (axis == 'thetahS') or (axis == 'thetahX') or (axis == 'thetaSX'): xlims = (-np.pi/2, np.pi/2)

            elif (axis == 'vs') or (axis == 'vx'): xlims = (1, 1000)

            elif (axis == 'None'): axis, xlims = 'mH1', (None, None)

            else:
                raise Exception('axis has invalid value in parameterPlotterMain')

            try:
                soloPlot(generalPhysics, axis, xlims, ylims, dataPath, outputPath, ObservedLimit, dataId, **kwargs)

            except pandas.errors.EmptyDataError:
                x = np.linspace(1,5)
                plt.plot(x,x)
                plt.title('pandas.EmptyDataError')
                plt.savefig(outputPath + '/' + dataId + '_' + generalPhysics 
                            + '_' + axis + '_dud' + '.png')
                plt.close()

            print('Loading {}'.format(int(loadstep/loading * 100)))
            loadstep = loadstep + 1
            
    elif solo == False:
        pass

    else:
        raise Exception('solo set to invalid value.')


    if together == True:

        def togetherPlot(iterable, xlims, ylims, filename, generalPhysics, **kwargs):

            plt.close()
            # axis                     # dataPath                    # ObservedLimit                 # dataId

            for x, y in iterable:
                plt.plot(x,y)

                plt.xlim(left = xlims[0], right = xlims[1])
                plt.ylim(bottom=ylims[0], top=ylims[1])

            filename = relPath + '/' + generalPhysics + filename

            # plt.title(filename_H1H2)
            plt.savefig(relPath)

    elif together == False:
        pass

    else:
        raise Exception('together set to invalid value.')
    

    if (solo == False) and (together == False):
       raise Exception('solo and together set to false, script is doing nothing.')


if __name__ == "__main__":

    parameterPlotterMain('AtlasBP2_check_prel', 'testPlott', '/**/settings_*.json', 'ppXNPSM', (None, None), (None, None), True, False, 
                         marker='.', ls='solid', SM1='bb', SM2='gamgam', figStart=None, figEnd=None, SMmode=4, yscale='log') 

    # parameterPlotterMain('AtlasBP3_check_prel', 'plot_AtlasBP3_check_prel', '/**/settings_*.json', 'ppXNPSM', (None, None), (None, None), True, False, 
    #                      marker='.', ls='solid', SM1='bb', SM2='gamgam', figStart=None, figEnd=None, SMmode=5) 
    

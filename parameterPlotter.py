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
    relListPaths = glob.glob(relPath + '/**/output_*.tsv', recursive=True)
    return relListPaths


def auxSoloPlot(xlims, ylims, path, filename, **kwargs):
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
    if 'yConst' in kwargs:

        if 'yConstLs' in kwargs:
            linestyle = kwargs['yConstLs']

        else:
            ls = 'dashed'

        if 'yConstClr' in kwargs:
            clr = kwargs['yConstClr']

        else:
            clr = 'r'

        plt.axhline(y=kwargs['yConst'], color=clr, linestyle=ls)    

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

################################################################################

    # if one of the bounds set to none then use matplotlib auto settings
    plt.xlim(left=xlims[0], right=xlims[1])
    plt.ylim(left=ylims[0], right=ylims[1])

    plt.savefig(path + '/' + filename)

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

    H1H2, H1H1, H2H2 = dataGenerator(generalPhysics, axis, path, **kwargs)

    xlist_H1H2 = H1H2[0]
    ylist_H1H2 = H1H2[modeSM]
    #name_H1H2 = 'H1H2'

    xlist_H1H1 = H1H1[0]
    ylist_H1H1 = H1H1[3]
    #name_H1H1 = 'H1H1'

    xlist_H2H2 = H2H2[0]
    ylist_H2H2 = H2H2[3]
    #name_H2H2 = 'H2H2'

    return (xlist_H1H2, ylist_H1H2), (xlist_H1H1, ylist_H1H1), (xlist_H2H2, ylist_H2H2)


def dictConstruct(paths, key):

    dictList = []

    for pathVar in paths:

        with open(pathVar) as f:
            contentsJSON = json.load(f)

        dictList.append(contentsJSON[key])

    return dictList


def solo(generalPhysics, axis, xlims, ylims, dataPath, outputPath, ObservedLimit, dataId, **kwargs):

    # fix this: this is not a nice solution
    kwargs['yConst'] = ObservedLimit
    
    # returns lists in nice format
    # fix this: put sorter in definer so this becomes one line
    (xlist_H1H2, ylist_H1H2), (xlist_H1H1, ylist_H1H1), (xlist_H2H2, ylist_H2H2) = definer(generalPhysics, axis, dataPath, **kwargs)

    # sort according to xlist
    (xlist_H1H2, ylist_H1H2) = sorter(xlist_H1H2, ylist_H1H2)
    (xlist_H1H1, ylist_H1H1) = sorter(xlist_H1H1, ylist_H1H1)
    (xlist_H2H2, ylist_H2H2) = sorter(xlist_H2H2, ylist_H2H2)

    # from stackexchange:  https://stackoverflow.com/a/1274436/17456342
    if not os.path.isdir(outputPath):
       os.makedirs(outputPath)

    else:
        pass

    outputPathH1H2 = outputPath + '/' + '_H1H2'
    outputPathH1H1 = outputPath + '/' + '_H1H1'
    outputPathH2H2 = outputPath + '/' + '_H2H2'

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
    filename_H1H2 = outputPathH1H2 + '/' + dataId + '_' + generalPhysics+ '_' + axis + '_H1H2'
    filename_H1H1 = outputPathH1H1 + '/' + dataId + '_' + generalPhysics+ '_' + axis + '_H1H1'
    filename_H2H2 = outputPathH2H2 + '/' + dataId + '_' + generalPhysics+ '_' + axis + '_H2H2'

    # fix this: maybe make function out this repeated process 
    plt.close()
    plt.plot(xlist_H1H2, ylist_H1H2, marker=marker, ls=ls)
    auxSoloPlot(xlims, ylims, outputPathH1H2 , filename_H1H2, **kwargs)

    plt.close()
    plt.plot(xlist_H1H1, ylist_H1H1, marker=marker, ls=ls)
    auxSoloPlot(xlims, ylims, outputPathH1H1 , filename_H1H1, **kwargs)

    plt.close()
    plt.plot(xlist_H2H2, ylist_H2H2, marker=marker, ls=ls)
    auxSoloPlot(xlims, ylims, outputPathH2H2 , filename_H2H2, **kwargs)


def parameterPlotterMain(relPath, outputPath, generalPhysics, xlims, ylims, solo, together, **kwargs):

    #################################### kwargs ####################################

    if 'ls' in kwargs:
        ls = kwargs['ls']

    else:
        ls = 'None'

    if 'marker' in kwargs:
        marker = kwargs['marker']

    else:
        marker = 'None'

    ################################################################################

    outputPaths = directorySearcher(relPath, '/**/settings_*.json')

    dictList = dictConstruct(outputPaths, 'extra')

    tuples = [( (dictList[i])['path2output'], (dictList[i])['dataId'],  (dictList[i])['ObservedLimit'], ) for i in range(len(dictList))]

    if solo == True:
        for (axis, dataPath, ObservedLimit, dataId) in tuples:
            solo(generalPhysics, axis, xlims, ylims, dataPath, outputPath, ObservedLimit, dataId, **kwargs)

    elif solo == False:
        pass

    else:
        raise Exception('solo set to invalid value.')


    if together == True:

        def togetherPlot(iterable, xlims, ylims, relPath, filename, generalPhysics, **kwargs):

            plt.close()
            for x, y in iterable:
                plt.plot(x,y)

                plt.xlim(left = xlims[0], right = xlims[1])
                plt.ylim(left = ylims[0], right = ylims[1])

            filename = relPath + '/' + generalPhysics + filename

            plt.title(filename_H1H2)
            plt.savefig(relPath)

    elif together == False:
        pass

    else:
        raise Exception('together set to invalid value.')
    

    if (solo == False) and (together == False):
    together   raise Exception('solo and together set to false, script is doing nothing.')


if __name__ == "__main__":

    parameterPlotterSoloMain('ppXNPSM', 'thetahS', (-np.pi/2, np.pi/2), 'test5', SM1 = 'bb', SM2 = 'gamgam')

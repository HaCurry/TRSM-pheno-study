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

import functions as TRSM
import Exclusion_functions as excl

# NOTE the dominant SMmode changes in BP3 to SMmode = 2!
def dataGenerator(generalPhysics, axis, path, **kwargs):
    ''' 
    generalPhysics can be XNP, ppXNP, ppXNPSM
    axis is the desired axis of the physical quantity
    path is the path to the data
    **kwargs need to define SM1 SM2 if generalPhysics = ppXNPSM.
             User can also give additional axes in axis2, axis3.
             User can give normalization of ppXNP, default set to 1.
             User can give normalization of ppXNPSM, default set to 1.

    returns H1H2, H1H1, H2H2, where each array contains elements with the axis list and the physical quantity
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
        H1H2, H1H1, H2H2 = TRSM.ppXNP_massfree(path, axis, axis2, axis3, normalizationNP = ggF_xs_SM_Higgs)
        
    elif generalPhysics == 'ppXNPSM':
        H1H2, H1H1, H2H2 = TRSM.ppXNPSM_massfree(path, axis, axis2, axis3, SM1, SM2, normalizationSM = ggF_xs_SM_Higgs_SM1SM2)
        
    else:
        raise Exception('No general physics chosen')

    return H1H2, H1H1, H2H2



def directorySearcher(relPath, globPathname):
    ''' 
    relPath is relative path to directory where glob searches
    globPathname is the files in globstyle you want the paths to

    returns: relative paths in listPaths
    '''
    relListPaths = glob.glob(relPath + '/**/output_*.tsv', recursive = True)
    return relListPaths



def parameterPlot(xlist, ylist, xlims, **kwargs):

    if 'ls' in kwargs:
        ls = kwargs['ls']

    else:
        ls = 'None'
    
    plt.plot(xlist, ylist, marker = '.', linestyle = ls)

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
            
        plt.axhline(y = kwargs['yConst'], color = clr, linestyle = ls)
    
    plt.xlim(xlims)

    if 'ylims' in kwargs:
        plt.ylim(kwargs['ylims'])

    # for cross-sections
    if 'yscale' in kwargs:

        if kwargs['yscale'] == 'log':
            plt.yscale('log')

        else:
            raise Exception('invalid log scale parameterPlot')


# if 'show' in kwargs:
# 
    # if kwargs['show'] == True:
# 
        # plt.show()
# 
    # elif kwargs['show'] == False:
        # pass
# 
    # else:
        # raise Exception('invalid show value in parameterPlot')
# 
# 
# plt.savefig(saveDir + '/' + name)

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



def definer(generalPhysics, axis, path, sort, **kwargs):
    '''
    produces all the list elements in a nice format
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
                


def parameterPlotterSolo(generalPhysics, axis, xlims, relPath, **kwargs):

    outputPaths = directorySearcher(relPath, '/**/output_*.tsv')

    H1H2 = []
    H1H1 = []
    H2H2 = []

    if 'solo' in kwargs:

        if kwargs['solo'] == True:
            for path in outputPaths:

                # returns lists in nice format
                (xlist_H1H2, ylist_H1H2), (xlist_H1H1, ylist_H1H1), (xlist_H2H2, ylist_H2H2) = definer(generalPhysics, axis, path, sort, **kwargs)

                # sort according to xlist
                (xlist_H1H2, ylist_H1H2) = sorter(xlist_H1H2, ylist_H1H2)
                (xlist_H1H1, ylist_H1H1) = sorter(xlist_H1H1, ylist_H1H1)
                (xlist_H2H2, ylist_H2H2) = sorter(xlist_H2H2, ylist_H2H2)
                
                
                plt.close()
                parameterPlot(xlist_H1H2, ylist_H1H2, xlims, **kwargs)
                filename_H1H2 = os.path.dirname(path) + '/' + generalPhysics + '_solo_parameterPlot_H1H2'
                plt.title(filename_H1H2)
                plt.savefig(filename)
                plt.show()
                plt.close()
                
                parameterPlot(xlist_H1H1, ylist_H1H1, xlims, **kwargs)
                filename_H1H1 = os.path.dirname(path) + '/' + generalPhysics + '_solo_parameterPlot_H1H1'
                plt.title(filename_H1H1)
                plt.savefig(filename_H1H1)
                plt.show()
                plt.close()

                parameterPlot(xlist_H2H2, ylist_H2H2, xlims, **kwargs)
                filename_H2H2 = os.path.dirname(path) + '/' + generalPhysics + '_solo_parameterPlot_H2H2'
                plt.title(filename_H2H2)
                plt.savefig(filename_H2H2)
                plt.show()
                plt.close()

                H1H2.append((xlist_H1H2, ylist_H1H2))
                H1H1.append((xlist_H1H1, ylist_H1H1))
                H2H2.append((xlist_H2H2, ylist_H2H2))

        elif kwargs['solo'] == False:
            pass

        else:
            raise Exception('solo set to invalid value')

    if 'together' in kwargs:

        if kwargs['together'] == True:

            def togetherPlot(iterable, xlims, relPath, filename, generalPhysics, **kwargs):
            
                plt.close()
                for x, y in iterable:
                    parameterPlot(x,y, xlims, **kwargs)

                filename_H1H2 = relPath + '/' + generalPhysics + filename
            plt.title(filename_H1H2)
            plt.savefig(relPath)
            

                

        elif kwargs['together'] == False:

            # if both solo and togher set to false then script is not doing anythying
            if kwargs['solo'] == False:
                raise Exception('Both solo and together set to False. Script doing nothing')
            # otherwise just continue
            pass

        else:
            raise Exception('together set to invalid value')
        
    
if __name__ == "__main__":

    parameterPlotterSoloMain('ppXNPSM', 'thetahS', (-np.pi/2, np.pi/2), 'test5', SM1 = 'bb', SM2 = 'gamgam')

    
    
        

    
        
    
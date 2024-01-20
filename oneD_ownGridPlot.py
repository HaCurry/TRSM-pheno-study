
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
import parameterPlotter


def plotAuxEnvelope1D(x, ymin, ymax, paramFree, **kwargs):
    plt.figure()

    if paramFree == 'thetahS':
        freeVar = r'$\theta_{hS}$'
        plt.xlim(-np.pi/2, np.pi/2)
        plt.xlabel(freeVar)
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')
        
    elif paramFree == 'thetahX':
        freeVar = r'$\theta_{hX}$'
        plt.xlim(-np.pi/2, np.pi/2)
        plt.xlabel(freeVar)
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    elif paramFree == 'thetaSX':
        freeVar = r'$\theta_{SX}$'
        plt.xlim(-np.pi/2, np.pi/2)
        plt.xlabel(freeVar)
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    elif paramFree == 'vs':
        freeVar = r'$v_{S}$'
        plt.xlim(1, 1000)
        plt.xlabel(freeVar + ' [GeV]')
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    elif paramFree == 'vx':
        freeVar = r'$v_{X}$'
        plt.xlim(1, 1000)
        plt.xlabel(freeVar + ' [GeV]')
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    elif paramFree == 'Nofree':
        freeVar = r'Nofree'
        plt.xlim(1, 1000)
        plt.xlabel(freeVar)
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')


    else: raise Exception('No paramFree value given, something went wrong.')

    if 'plotAuxEnvelopeTitle' in kwargs:
        plt.title(kwargs['plotAuxEnvelopeTitle']) #+ ', ' + freeVar)

    else: pass

    plt.fill_between(x, ymin, ymax, alpha=0.2)
        

def plotAuxTogether1D(dictList, fileOutputPath, **kwargs):

    # assuming the dictList only containts elements with the same paramFree
    paramFree = (dictList[0])['paramFree']
    if 'plotAuxTogetherMark' in kwargs and kwargs['plotAuxTogetherMark'] == 'BP2':
        mark = 'BP2'

    elif 'plotAuxTogetherMark' in kwargs and kwargs['plotAuxTogetherMark'] == 'BP3':
        mark = 'BP3'

    else: mark = 'none'

    plt.figure()
    if paramFree == 'thetahS':
        freeVar = r'$\theta_{hS}$'
        plt.xlim(-np.pi/2, np.pi/2)
        plt.xlabel(freeVar)
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')
        if mark == 'BP2': markCoord = 1.352, 1
        elif mark == 'BP3': markCoord = -0.129, 1
        else: pass
        
    elif paramFree == 'thetahX':
        freeVar = r'$\theta_{hX}$'
        plt.xlim(-np.pi/2, np.pi/2)
        plt.xlabel(freeVar)
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')
        if mark == 'BP2': markCoord = 1.175, 1
        elif mark == 'BP3': markCoord = 0.226, 1
        else: pass

    elif paramFree == 'thetaSX':
        freeVar = r'$\theta_{SX}$'
        plt.xlim(-np.pi/2, np.pi/2)
        plt.xlabel(freeVar)
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')
        if mark == 'BP2': markCoord = -0.407, 1
        elif mark == 'BP3': markCoord = -0.899, 1
        else: pass

    elif paramFree == 'vs':
        freeVar = r'$v_{S}$'
        plt.xlim(1, 1000)
        plt.xlabel(freeVar + ' [GeV]')
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')
        if mark == 'BP2': markCoord = 120, 1
        elif mark == 'BP3': markCoord = 140, 1
        else: pass

    elif paramFree == 'vx':
        freeVar = r'$v_{X}$'
        plt.xlim(1, 1000)
        plt.xlabel(freeVar + ' [GeV]')
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')
        if mark == 'BP2': markCoord = 890, 1
        elif mark == 'BP3': markCoord = 100, 1
        else: pass

    elif paramFree == 'Nofree':
        freeVar = r'Nofree'
        plt.xlim(1, 1000)
        plt.xlabel(freeVar)
        plt.ylabel(r'$\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')
        if mark == 'BP2': markCoord = 1, 1
        elif mark == 'BP3': markCoord = 1, 1
        else: pass

    else: raise Exception('No paramFree value given, something went wrong.')

    if 'plotAuxTogetherTitle' in kwargs:
        plt.title(kwargs['plotAuxTogetherTitle']) #+ ', ' + freeVar)

    else: pass

    for dictElement in dictList:
        x, y, axis, ObservedLimit, dataId = dictElement['x'], dictElement['y'], dictElement['paramFree'], dictElement['ObservedLimit'], dictElement['dataId']

        # low opacity
        if 'lowopacity' in kwargs and kwargs['lowopacity'] == True:
            plt.plot(x, y, alpha=0.2, color='C0')

        # normal plots
        else:
            plt.plot(x, y, ls='solid', marker='.')

    if mark == 'BP2' or mark == 'BP3':
        plt.plot(markCoord[0], markCoord[1], ls='none', marker='o', color='black')

    else: pass
    
    plt.tight_layout()
    if 'lowopacity' in kwargs and kwargs['lowopacity'] == True:
        plt.savefig(fileOutputPath + '_lowopacity_' + '.png')
        plt.savefig(fileOutputPath + '_lowopacity_' + '.pdf')
        plt.close()
    else:
        plt.savefig(fileOutputPath + '.png')
        plt.savefig(fileOutputPath + '.pdf')
        plt.close()
        
   

if __name__ == "__main__":

    ### 1D paramter plots, 50 points, with log scale and fixed ylims

    # parameterPlotter.parameterPlot('calc_ownGridRegion1BP2_check_prel_Mproc', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP2_check_prel_noconstraints', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, yscale='log', ylims=(10**(-8),8*10**(-2)), normNofree=True)

    # parameterPlotter.parameterPlot('calc_ownGridRegion2BP2_check_prel_Mproc', '/**/settingsCalc_*.json', 'plot_ownGridRegion2BP2_check_prel_noconstraints', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, yscale='log', ylims=(10**(-8),8*10**(-2)), normNofree=True)


    # parameterPlotter.parameterPlot('calc_ownGridRegion1BP3_check_prel_Mproc', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP3_check_prel_noconstraints', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, yscale='log', ylims=(10**(-8),8*10**(-2)), normNofree=True)

    # parameterPlotter.parameterPlot('calc_ownGridRegion2BP3_check_prel_Mproc', '/**/settingsCalc_*.json', 'plot_ownGridRegion2BP3_check_prel_noconstraints', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, yscale='log', ylims=(10**(-8),8*10**(-2)), normNofree=True)

    # parameterPlotter.parameterPlot('calc_ownGridRegion1BP2_check_prel_Mproc', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP2_check_prel_noconstraints_Normed', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, yscale='log', normNofree=True)

    ### 1D paramter plots, 50 points, with normalization
    
    # parameterPlotter.parameterPlot('calc_ownGridRegion1BP2_check_prel_Mproc', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP2_check_prel_noconstraints_Normed_nolog', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, normNofree=True)

    # parameterPlotter.parameterPlot('calc_ownGridRegion2BP2_check_prel_Mproc', '/**/settingsCalc_*.json', 'plot_ownGridRegion2BP2_check_prel_noconstraints_Normed_nolog', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, normNofree=True)

    # parameterPlotter.parameterPlot('calc_ownGridRegion1BP3_check_prel_Mproc', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP3_check_prel_noconstraints_Normed_nolog', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM2_H2_SM1', saveStep=True, normNofree=True)

    # parameterPlotter.parameterPlot('calc_ownGridRegion2BP3_check_prel_Mproc', '/**/settingsCalc_*.json', 'plot_ownGridRegion2BP3_check_prel_noconstraints_Normed_nolog', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM2_H2_SM1', saveStep=True, normNofree=True)

    ### 1D paramter plots, 100 points, with normalization and improved titles and labels on and envelope plots

    # parameterPlotter.parameterPlot('calc_ownGridRegion1BP2_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP2_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, normNofree=True,
    #                                plotAuxEnvelope1D=plotAuxEnvelope1D, plotAuxEnvelopeTitle=r'BP2 R1: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
    #                                plotAuxTogether1D=plotAuxTogether1D, plotAuxTogetherTitle=r'BP2 R1: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    # parameterPlotter.parameterPlot('calc_ownGridRegion2BP2_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion2BP2_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, normNofree=True,
    #                                plotAuxEnvelope1D=plotAuxEnvelope1D, plotAuxEnvelopeTitle=r'BP2 R2: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
    #                                plotAuxTogether1D=plotAuxTogether1D, plotAuxTogetherTitle=r'BP2 R2: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    # parameterPlotter.parameterPlot('calc_ownGridRegion1BP3_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP3_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM2_H2_SM1', saveStep=True, normNofree=True, 
    #                                plotAuxEnvelope1D=plotAuxEnvelope1D, plotAuxEnvelopeTitle=r'BP3 R1: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
    #                                plotAuxTogether1D=plotAuxTogether1D, plotAuxTogetherTitle=r'BP3 R1: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    # parameterPlotter.parameterPlot('calc_ownGridRegion2BP3_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion2BP3_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
    #               ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM2_H2_SM1', saveStep=True, normNofree=True,
    #                                plotAuxEnvelope1D=plotAuxEnvelope1D, plotAuxEnvelopeTitle=r'BP3 R2: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
    #                                plotAuxTogether1D=plotAuxTogether1D, plotAuxTogetherTitle=r'BP3 R2: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    ### 1D paramter plots, 100 points, with normalization and improved titles and labels on and envelope plots low opacity plots
        
    parameterPlotter.parameterPlot('calc_ownGridRegion1BP2_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP2_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
                  ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, normNofree=True,
                                   plotAuxEnvelope1D=plotAuxEnvelope1D, plotAuxEnvelopeTitle=r'BP2 R1: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
                                   plotAuxTogether1D=plotAuxTogether1D, plotAuxTogetherTitle=r'BP2 R1: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
                                   lowopacity=True, plotAuxTogetherMark='BP2')

    parameterPlotter.parameterPlot('calc_ownGridRegion2BP2_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion2BP2_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
                  ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, normNofree=True,
                                   plotAuxEnvelope1D=plotAuxEnvelope1D, plotAuxEnvelopeTitle=r'BP2 R2: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
                                   plotAuxTogether1D=plotAuxTogether1D, plotAuxTogetherTitle=r'BP2 R2: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
                                   lowopacity=True, plotAuxTogetherMark='BP2')

    parameterPlotter.parameterPlot('calc_ownGridRegion1BP3_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP3_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
                  ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM2_H2_SM1', saveStep=True, normNofree=True, 
                                   plotAuxEnvelope1D=plotAuxEnvelope1D, plotAuxEnvelopeTitle=r'BP3 R1: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
                                   plotAuxTogether1D=plotAuxTogether1D, plotAuxTogetherTitle=r'BP3 R1: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
                                   lowopacity=True, plotAuxTogetherMark='BP3')

    parameterPlotter.parameterPlot('calc_ownGridRegion2BP3_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion2BP3_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
                  ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM2_H2_SM1', saveStep=True, normNofree=True,
                                   plotAuxEnvelope1D=plotAuxEnvelope1D, plotAuxEnvelopeTitle=r'BP3 R2: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
                                   plotAuxTogether1D=plotAuxTogether1D, plotAuxTogetherTitle=r'BP3 R2: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $',
                                   lowopacity=True, plotAuxTogetherMark='BP3')

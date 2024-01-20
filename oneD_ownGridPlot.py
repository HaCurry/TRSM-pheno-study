
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


def plotAuxTogether1D(x, ymin, ymax, paramFree, **kwargs):
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

    ### 1D paramter plots, 100 points, with normalization and improved titles and labels on envelopeplots

    parameterPlotter.parameterPlot('calc_ownGridRegion1BP2_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP2_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
                  ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, normNofree=True)
                                   plotAuxEnvelope1D=plotAuxTogether1D, plotAuxEnvelopeTitle=r'BP2 R1: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    parameterPlotter.parameterPlot('calc_ownGridRegion2BP2_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion2BP2_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
                  ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM1_H2_SM2', saveStep=True, normNofree=True)
                                   plotAuxEnvelope1D=plotAuxTogether1D, plotAuxEnvelopeTitle=r'BP2 R2: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    parameterPlotter.parameterPlot('calc_ownGridRegion1BP3_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion1BP3_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
                  ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM2_H2_SM1', saveStep=True, normNofree=True, 
                                   plotAuxEnvelope1D=plotAuxTogether1D, plotAuxEnvelopeTitle=r'BP3 R1: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

    parameterPlotter.parameterPlot('calc_ownGridRegion2BP3_check_prel_Mproc_100_TB', '/**/settingsCalc_*.json', 'plot_ownGridRegion2BP3_check_prel_noconstraints_Normed_nolog_100_TB', 'H1H2', True, True, 
                  ppXNPSM=True, ShowObsLimit=False, SM1='bb', SM2='gamgam', SMmode='H1_SM2_H2_SM1', saveStep=True, normNofree=True)
                                   plotAuxEnvelope1D=plotAuxTogether1D, plotAuxEnvelopeTitle=r'BP3 R2: $\sigma_{gg \ \to \  h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})}/\sigma^{\mathrm{fixed}}_{gg \ \to \ h _{3} \ \to \ h_{1}(\gamma\gamma)h_{2}(b\bar{b})} $')

        

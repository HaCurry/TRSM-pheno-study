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

# NOTE the dominant SMmode changes in BP3 to SMmode = 2!
def dataGenerator(physics, quantity, axis, path, **kwargs):

    ########################    kwargs    ########################
    
    if (physics == "ppXSHSM") or (physics == "ppXSSSM") or (physics == "ppXHHSM"):

        if 'SM1' and 'SM2' in kwargs:
                SM1, SM2 = kwargs['SM1'], kwargs['SM2']
    
        else:
            raise Exception('No SM final state chosen in plotter, please define SM1 and SM2')

        df = pandas.read_table(path, index_col = 0)

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
        # rescaled SM dihiggs cross-section (ggF):
        # https://cds.cern.ch/record/2764447/files/ATL-PHYS-SLIDE-2021-092.pdf
        ggF_xs_SM_Higgs = 31.02 * 10**(-3)

    # Rescale ppX__SM cross-section
    # Default set to 1 (no rescaling ocurrs)
    if 'ggF_xs_SM_Higgs_SM1SM2' in kwargs:
        ggF_xs_SM_Higgs_SM1SM2 = kwargs['ggF_xs_SM_Higgs_SM1SM2']

    else:
        ggF_xs_SM_Higgs_SM1SM2 = 1

    # dataGenerator outputs eg. 
    # XSHSM1SM2 + XSHSM2SM1 if SMmode = 0
    # XSHSM1SM2 if SMmode = 1
    # XSHSM2SM1 if SMmode = 2
    # default set to 1
    # NOTE the dominant SMmode changes in BP3 to SMmode = 2!
    if 'SMmode' in kwargs:
        SMmode = kwargs['SMmode']

    else:
        SMmode = 1

    ##############################################################
    

    df = pandas.read_table(path, index_col = 0)
    
    mH1_H1H2 = np.array([i for i in df[axis]])
    mH2_H1H2 = np.array([i for i in df[axis2]])
    mH3_H1H2 = np.array([i for i in df[axis3]])

    b_H3_H1H2 = np.array([i for i in df["b_H3_H1H2"]])
    b_H3_H1H1 = np.array([i for i in df["b_H3_H1H1"]])
    b_H3_H2H2 = np.array([i for i in df["b_H3_H2H2"]])

    idx = np.argsort(mH1_H1H2)
    mH1_H1H2  = mH1_H1H2[idx]
    
    
    if physics == "XSH":
        b_H3_H1H2 = b_H3_H1H2[idx]
        return mH1_H1H2, b_H3_H1H2
            
    elif physics == "XHH":

        if BP == "BP2":    
            b_H3_H2H2 = b_H3_H2H2[idx]
            return mH1_H1H2, b_H3_H2H2

        elif BP == "BP3":
            b_H3_H1H1 = b_H3_H1H1[idx]
            return mH1_H1H2, b_H3_H1H1
        
    elif physics == "XSS":

        if BP == "BP2":
            b_H3_H1H1 = b_H3_H1H1[idx]
            return mH1_H1H2, b_H3_H1H1

        elif BP == "BP3":
            b_H3_H2H2 = b_H3_H2H2[idx]
            return mH1_H1H2, b_H3_H2H2

    
    x_H3_gg_H1H2 = np.array([i for i in df["x_H3_gg"]])
    x_H3_gg_H1H2 = x_H3_gg_H1H2[idx]
#    x_H3_gg_H1H1 = x_H3_gg_H1H2.copy()
#    x_H3_gg_H2H2 = x_H3_gg_H1H2.copy()

    
    if (physics == "ppXSH") or (physics == "ppXSHSM") or (physics == "XSHSM"):
        
        b_H3_H1H2 = b_H3_H1H2[idx]

        if physics == "ppXSH":
            pp_X_H1H2 = np.array([(b_H3_H1H2[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H2))])
    #        pp_X_H1H2 = np.array([b_H3_H1H2[i] for i in range(len(b_H3_H1H2))])
            return mH1_H1H2, pp_X_H1H2
        
        else: # physics == "ppXSHSM" or physics == "XSHSM"
#            SM1, SM2 = "bb", "gamgam"
            b_H1_bb     = np.array([i for i in df["b_H1_" + SM1]])        #"b_H1_bb"
            b_H1_bb     = b_H1_bb[idx]

            b_H1_gamgam = np.array([i for i in df["b_H1_" + SM2]])        #"b_H1_gamgam"
            b_H1_gamgam = b_H1_gamgam[idx]

            b_H2_bb     = np.array([i for i in df["b_H2_" + SM1]])        #"b_H2_bb"
            b_H2_bb     = b_H2_bb[idx]

            b_H2_gamgam = np.array([i for i in df["b_H2_" + SM2]])        #"b_H2_gamgam"
            b_H2_gamgam = b_H2_gamgam[idx]
            
            b_H1H2_bbgamgam = [b_H1_bb_H2_gamgam[i] + b_H1_gamgam_H2_bb[i] for i in range(len(b_H1_bb))]
            b_H1_bb_H2_gamgam = [b_H1_bb[i] * b_H2_gamgam[i] for i in range(len(b_H1_bb))]
            b_H1_gamgam_H2_bb = [b_H2_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]

            if physics == "XSHSM":

                if SMmode == 0:
                    H1H2 = np.array([b_H1H2_bbgamgam])

                elif SMmode == 1:
                    H1H2 = np.array([b_H1_bb_H2_gamgam])

                elif SMmode == 2:
                    H1H2 = np.array([b_H1_gamgam_H2_bb])
                
                return mH1_H1H2, H1H2

            elif physics == "ppXSHSM":

                if SMmode == 0:
                    pp_X_H1H2_bbgamgam = [(b_H1H2_bbgamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H1H2_bbgamgam))]
                    H1H2 = pp_X_H1H2_bbgamgam
                    return mH1_H1H2, H1H2

                elif SMmode == 1:
                    pp_X_H1_bb_H2_gamgam = [b_H1_bb_H2_gamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
                    H1H2 = pp_X_H1_bb_H2_gamgam
                    return mH1_H1H2, H1H2
                    
                elif SMmode == 2:
                    pp_X_H1_gamgam_H2_bb = [b_H1_gamgam_H2_bb[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
                    H1H2 = pp_X_H1_gamgam_H2_bb
                    return mH1_H1H2, H1H2

                else:
                    raise Exception('No SMmode chosen in dataGenerator in conditionals ppXSH, ppXSHSM, XSHSM')

            else:
                raise Exception('No physics chosen in dataGenerator in conditionals ppXSH, ppXSHSM, XSHSM')
    
    elif physics == "ppXHH":
    
        if BP == "BP2":
            b_H3_H2H2 = b_H3_H2H2[idx]
            pp_X_H2H2 = np.array([(b_H3_H2H2[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H2H2))])
            return mH1_H1H2, pp_X_H2H2

        elif BP == "BP3":
            b_H3_H1H1 = b_H3_H1H1[idx]
            pp_X_H1H1 = np.array([(b_H3_H1H1[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H1))])
            return mH1_H1H2, pp_X_H1H1

    elif physics == "ppXSS":

        if BP == "BP2":
            b_H3_H1H1 = b_H3_H1H1[idx]
            pp_X_H1H1 = np.array([(b_H3_H1H1[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H1))])
            return mH1_H1H2, pp_X_H1H1

        elif BP == "BP3":
            b_H3_H2H2 = b_H3_H2H2[idx]
            pp_X_H2H2 = np.array([(b_H3_H2H2[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H2H2))])
            return mH1_H1H2, pp_X_H2H2
            
    else:
        raise Exception("No physics chosen")

    
        
    
#!/usr/bin/python3 python3
import configurer as config
import functions

import os
import subprocess

import numpy as np
import pandas

from scipy.optimize import NonlinearConstraint

if __name__ == '__main__':
   

    def ppXNPSM_massfree(BPdirectory, axes1, axes2, axes3, SM1, SM2, normalizationSM = (31.02 * 10**(-3)) * 0.0026):
        df = pandas.read_table(BPdirectory)#, index_col = 0)
        # PC
        # df = pandas.read_table ( r"\\wsl.localhost\Ubuntu\home\iram\scannerS\ScannerS-master\build\output_file.tsv" , index_col =0)
        
        mH1_H1H2 = [i for i in df[axes1]] #"mH1"
        mH2_H1H2 = [i for i in df[axes2]] #"mH2"
        mH3_H1H2 = [i for i in df[axes3]] #"mH3"
        
        mH1_H1H1 = mH1_H1H2.copy()
        mH2_H1H1 = mH2_H1H2.copy()
        mH3_H1H1 = mH3_H1H2.copy()
        
        mH1_H2H2 = mH1_H1H2.copy()
        mH2_H2H2 = mH2_H1H2.copy()
        mH3_H2H2 = mH3_H1H2.copy()
        
        mH1_x_H3_gg = mH1_H1H2.copy()
        mH2_x_H3_gg = mH2_H1H2.copy()
        mH3_x_H3_gg = mH3_H1H2.copy()
        
        b_H3_H1H2 = [i for i in df["b_H3_H1H2"]]
        b_H3_H1H1 = [i for i in df["b_H3_H1H1"]]
        b_H3_H2H2 = [i for i in df["b_H3_H2H2"]]
        # if energy == 13
        x_H3_gg_H1H2 = [i for i in df["x_H3_gg"]]
        x_H3_gg_H1H1 = x_H3_gg_H1H2.copy()
        x_H3_gg_H2H2 = x_H3_gg_H1H2.copy()
        # elif energy == 13.6
        # x_H3_gg_H1H2 = run3Interp(massList)
        
        b_H1_bb     = [i for i in df["b_H1_" + SM1]]        #"b_H1_bb"
        b_H1_gamgam = [i for i in df["b_H1_" + SM2]]        #"b_H1_gamgam"
        b_H2_bb     = [i for i in df["b_H2_" + SM1]]        #"b_H2_bb"
        b_H2_gamgam = [i for i in df["b_H2_" + SM2]]        #"b_H2_gamgam"
        
        epsilon = 10**(-6)
        
        check = ( len(mH1_H1H2 ) + len(mH2_H1H2) + len(mH3_H1H2) \
            + len(mH1_H1H1) + len(mH2_H1H1) + len(mH3_H1H1) \
            + len(mH1_H2H2) + len(mH2_H2H2) + len(mH3_H2H2) \
            + len(mH1_x_H3_gg) + len(mH2_x_H3_gg) + len(mH3_x_H3_gg) \
            + len(b_H3_H1H2) + len(b_H3_H1H1) + len(b_H3_H2H2) + len(x_H3_gg_H1H2) + len(x_H3_gg_H1H1) + len(x_H3_gg_H2H2) \
            + len(b_H1_bb) + len(b_H1_gamgam) + len(b_H2_bb) + len(b_H2_gamgam) ) / ( 22 *len(df["Unnamed: 0"]) )
        
        if  abs( check - 1 )  > + epsilon:
            raise Exception('length of lists not equal in ppXNPSM_massfree')
        
        b_H1_bb_H2_gamgam = [b_H1_bb[i] * b_H2_gamgam[i] for i in range(len(b_H1_bb))]
        b_H1_gamgam_H2_bb = [b_H2_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
        
        b_H1H2_bbgamgam = [b_H1_bb_H2_gamgam[i] + b_H1_gamgam_H2_bb[i] for i in range(len(b_H1_bb))]
        # b_H1H2_bbgamgam = [b_H1_bb[i] * b_H2_gamgam[i] + b_H2_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
        b_H1H1_bbgamgam = [b_H1_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
        b_H2H2_bbgamgam = [b_H2_bb[i] * b_H2_gamgam[i] for i in range(len(b_H2_bb))]
        
        
        ggF_bbgamgam_xs_SM_Higgs = normalizationSM
        # bbgamgam BR: https://inspirehep.net/files/a34811e0b9462ca5900081ffe6c92bdb
        # ggF XS: https://cds.cern.ch/record/2764447/files/ATL-PHYS-SLIDE-2021-092.pdf
        # ggF_bbgamgam_xs_SM_Higgs = (31.02 * 10**(-3)) * 0.0026  
        # ggF_bbgamgam_xs_SM_Higgs = (31.02 * 10**(-3)) * (10**(-2)*0.028)  
        # ggF_bbgamgam_xs_SM_Higgs = 1 
        
        # rescaled cross-section
        pp_X_H1H2_bbgamgam = [(b_H1H2_bbgamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H1H2_bbgamgam))]
        # pp_X_H1H2_bbgamgam = [x_H3_gg_H1H2[i] *  b_H3_H1H2[i] for i in range(len(b_H1H2_bbgamgam))]
        
        pp_X_H1H1_bbgamgam = [(b_H1H1_bbgamgam[i] * x_H3_gg_H1H1[i] * b_H3_H1H1[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H1H1_bbgamgam))]
        # pp_X_H1H1_bbgamgam = [ x_H3_gg_H1H1[i] * b_H3_H1H1[i] for i in range(len(b_H1H1_bbgamgam))]
        
        pp_X_H2H2_bbgamgam = [(b_H2H2_bbgamgam[i] * x_H3_gg_H2H2[i] * b_H3_H2H2[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H2H2_bbgamgam))]
        # pp_X_H2H2_bbgamgam = [x_H3_gg_H2H2[i] * b_H3_H2H2[i] for i in range(len(b_H2H2_bbgamgam))]
        
        
        pp_X_H1_bb_H2_gamgam = [b_H1_bb_H2_gamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
        # pp_X_H1_bb_H2_gamgam = [x_H3_gg_H1H2[i] * b_H3_H1H2[i] for i in range(len(b_H3_H1H2))]
        pp_X_H1_gamgam_H2_bb = [b_H1_gamgam_H2_bb[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
        # pp_X_H1_gamgam_H2_bb = [x_H3_gg_H1H2[i] * b_H3_H1H2[i] for i in range(len(b_H3_H1H2))]
        
        
            
        H1H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H1H2_bbgamgam, pp_X_H1_bb_H2_gamgam, pp_X_H1_gamgam_H2_bb])
        H1H1 = np.array([mH1_H1H1, mH2_H1H1, mH3_H1H1, pp_X_H1H1_bbgamgam])
        H2H2 = np.array([mH1_H2H2, mH2_H2H2, mH3_H2H2, pp_X_H2H2_bbgamgam])
        
        return H1H2, H1H1, H2H2
    
    BPdirectory = 'x_output_mH190_mH2125.09_mH3500.tsv' 

    df = pandas.read_table(BPdirectory)
    
    print((df['x_H3_gg']*df['b_H3_H1H2']*(df['b_H1_bb']*df['b_H2_gamgam']))[0])
    
    H1H2, H1H1, H2H2 = ppXNPSM_massfree(BPdirectory, 'mH1', 'mH2', 'mH3', 'bb', 'gamgam', normalizationSM=1) 
    
    print(H1H2[4][0])

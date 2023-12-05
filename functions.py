# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:16:40 2023

@author: Iram Haque
"""

import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects
import scipy.interpolate
from scipy.interpolate import CubicSpline
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
from numpy import ma


def massAndBrs(dataFrame, axes1, axes2, axes3):

    mH1_H1H2 = [i for i in dataFrame[axes1]]
    mH2_H1H2 = [i for i in dataFrame[axes2]]
    mH3_H1H2 = [i for i in dataFrame[axes3]]
    
    mH1_H1H1 = mH1_H1H2.copy()
    mH2_H1H1 = mH2_H1H2.copy()
    mH3_H1H1 = mH3_H1H2.copy()
    
    mH1_H2H2 = mH1_H1H2.copy()
    mH2_H2H2 = mH2_H1H2.copy()
    mH3_H2H2 = mH3_H1H2.copy()

    massH1H2 = [mH1_H1H2, mH2_H1H2, mH3_H1H2]
    massH1H1 = [mH1_H1H1, mH2_H1H1, mH3_H1H1]
    massH2H2 = [mH1_H2H2, mH2_H2H2, mH3_H2H2]
    
    b_H3_H1H2 = [i for i in dataFrame["b_H3_H1H2"]]
    b_H3_H1H1 = [i for i in dataFrame["b_H3_H1H1"]]
    b_H3_H2H2 = [i for i in dataFrame["b_H3_H2H2"]]

    return massH1H2, massH1H1, massH2H2, b_H3_H1H2, b_H3_H1H1, b_H3_H2H2



def XNP_massfree(BPdirectory, axes1, axes2, axes3):
    
    df = pandas.read_table(BPdirectory, index_col = 0)
    
    mH1_H1H2 = [i for i in df[axes1]]
    mH2_H1H2 = [i for i in df[axes2]]
    mH3_H1H2 = [i for i in df[axes3]]
    
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
    x_H3_gg = [i for i in df["x_H3_gg"]]
    
    w_H3 = [i for i in df[""]]
    
    
    
    H1H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, b_H3_H1H2])
    H1H1 = np.array([mH1_H1H1, mH2_H1H1, mH3_H1H1, b_H3_H1H1])
    H2H2 = np.array([mH1_H2H2, mH2_H2H2, mH3_H2H2, b_H3_H2H2])
    x_H3_gg = np.array([mH1_x_H3_gg, mH2_x_H3_gg, mH3_x_H3_gg, x_H3_gg])
    
    return H1H2, H1H1, H2H2, x_H3_gg


def NPSM_massfree(BPdirectory, axes1, axes2, axes3, SM1, SM2):
    
    df = pandas.read_table(BPdirectory)
    
    input1_H1H2 = df[axes1]
    input2_H1H2 = df[axes2]
    input3_H1H2 = df[axes3]
    
    input1_H1H1 = input1_H1H2.copy()
    input2_H1H1 = input2_H1H2.copy()
    input3_H1H1 = input3_H1H2.copy()

    input1_H2H2 = input1_H1H2.copy()
    input2_H2H2 = input2_H1H2.copy()
    input3_H2H2 = input3_H1H2.copy()
    
    b_H1_bb     = [i for i in df["b_H1_" + SM1]]    #"b_H1_bb"
    b_H1_gamgam = [i for i in df["b_H1_" + SM2]]    #"b_H1_gamgam"
    b_H2_bb     = [i for i in df["b_H2_" + SM1]]    #"b_H2_bb"
    b_H2_gamgam = [i for i in df["b_H2_" + SM2]]    #"b_H2_gamgam"
    
    check = ( len(input1_H1H2) + len(input2_H1H2) + len(input3_H1H2) + len(b_H1_bb) + len(b_H1_gamgam) + len(b_H2_bb) + len(b_H2_gamgam) )/ (7 * len(df["Unnamed: 0"]))
    epsilon = 10**(-6)
    
    if abs(check - 1) > epsilon:
        raise Exception('length of lists in NPSM_massfree are not equal')
    
    b_H1_bb_H2_gamgam = [b_H1_bb[i] * b_H2_gamgam[i] for i in range(len(b_H1_bb))]
    b_H2_bb_H1_gamgam = [b_H2_bb[i] * b_H1_gamgam[i] for i in range(len(b_H2_bb))]
    
    # H1H2 -> SM
    if SM1 == SM2:
        b_H1H2_bbgamgam = b_H1_bb_H2_gamgam # [b_H1_bb[i] * b_H2_gamgam[i] for i in range(len(b_H1_bb))]
    else:
        b_H1H2_bbgamgam = [b_H1_bb_H2_gamgam[i] + b_H2_bb_H1_gamgam[i] for i in range(len(b_H1_bb_H2_gamgam))]
        
    b_H1H1_bbgamgam = [b_H1_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
    b_H2H2_bbgamgam = [b_H2_bb[i] * b_H2_gamgam[i] for i in range(len(b_H2_bb))]
    
    H1H2 = np.array([input1_H1H2, input2_H1H2, input3_H1H2, b_H1H2_bbgamgam, b_H1_bb_H2_gamgam, b_H2_bb_H1_gamgam])
    H1H1 = np.array([input1_H1H1, input2_H1H1, input3_H1H1, b_H1H1_bbgamgam])
    H2H2 = np.array([input1_H2H2, input2_H2H2, input3_H2H2, b_H2H2_bbgamgam])
    
    return H1H2, H1H1, H2H2


def ppXNP_massfree(BPdirectory, axes1, axes2, axes3, normalizationNP = 31.02 * 10**(-3)):
    
    df = pandas.read_table(BPdirectory, index_col = 0)
    
    mH1_H1H2 = [i for i in df[axes1]]
    mH2_H1H2 = [i for i in df[axes2]]
    mH3_H1H2 = [i for i in df[axes3]]
    
    mH1_H1H1 = mH1_H1H2.copy()
    mH2_H1H1 = mH2_H1H2.copy()
    mH3_H1H1 = mH3_H1H2.copy()
    
    mH1_H2H2 = mH1_H1H2.copy()
    mH2_H2H2 = mH2_H1H2.copy()
    mH3_H2H2 = mH3_H1H2.copy()
    
    b_H3_H1H2 = [i for i in df["b_H3_H1H2"]]
    b_H3_H1H1 = [i for i in df["b_H3_H1H1"]]
    b_H3_H2H2 = [i for i in df["b_H3_H2H2"]]
    
    x_H3_gg_H1H2 = [i for i in df["x_H3_gg"]]
    x_H3_gg_H1H1 = x_H3_gg_H1H2.copy()
    x_H3_gg_H2H2 = x_H3_gg_H1H2.copy()
    
    
    # rescaled SM dihiggs cross-section (ggF):
    # https://cds.cern.ch/record/2764447/files/ATL-PHYS-SLIDE-2021-092.pdf
    ggF_xs_SM_Higgs = normalizationNP
    
    # rescaled cross-section
    pp_X_H1H2 = [(b_H3_H1H2[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
    H1H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, b_H3_H1H2, pp_X_H1H2])
    
    pp_X_H1H1 = [(b_H3_H1H1[i] * x_H3_gg_H1H1[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H1))]
    H1H1 = np.array([mH1_H1H1, mH2_H1H1, mH3_H1H1, b_H3_H1H1, pp_X_H1H1])
    
    pp_X_H2H2 = [(b_H3_H2H2[i] * x_H3_gg_H2H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H2H2))]
    H2H2 = np.array([mH1_H2H2, mH2_H2H2, mH3_H2H2, b_H3_H2H2, pp_X_H2H2])

    
    return H1H2, H1H1, H2H2



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
    x_H3_gg_H1H2 = [i for i in df["x_H3_gg"]]
    x_H3_gg_H1H1 = x_H3_gg_H1H2.copy()
    x_H3_gg_H2H2 = x_H3_gg_H1H2.copy()
    
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


def mixingMatrix(ths, thx, tsx, angles, plotangle):
    
    def matrix(ths, thx, tsx):
        R11 = np.cos(ths)*np.cos(thx)
        R12 = -np.sin(ths)*np.cos(thx)
        R13 = -np.sin(thx)
        
        R21 = np.sin(ths)*np.cos(tsx) - np.cos(ths)*np.sin(thx)*np.sin(tsx) 
        R22 = np.cos(ths)*np.cos(tsx) + np.sin(ths)*np.sin(thx)*np.sin(tsx)
        R23 = -np.cos(thx)*np.sin(tsx)
    
        R31 = np.cos(ths)*np.sin(thx)*np.cos(tsx) + np.sin(ths)*np.sin(tsx)
        R32 = np.cos(ths)*np.sin(tsx) - np.sin(ths)*np.sin(thx)*np.cos(tsx)
        R33 = np.cos(thx)*np.cos(tsx)
        
        return np.array([[R11, R12, R13], [R21, R22, R23], [R31, R32, R33]])
    
    matrix_thsfree = matrix(angles, 
                            np.array([thx for i in range(len(angles))]), 
                            np.array([tsx for i in range(len(angles))]))
    
    matrix_thxfree = matrix(np.array([ths for i in range(len(angles))]), 
                            angles, 
                            np.array([tsx for i in range(len(angles))]))
    
    matrix_tsxfree = matrix(np.array([ths for i in range(len(angles))]), 
                            np.array([thx for i in range(len(angles))]), 
                            angles)
    if plotangle == 'ths':
        plt.plot(angles, matrix_thsfree[0][0], lw = 3)
        plt.text(angles[0], (matrix_thsfree[0][0])[0], r'$\kappa_{1}$')
        plt.plot(angles, matrix_thsfree[1][0], lw = 3)
        plt.text(angles[0], (matrix_thsfree[1][0])[0], r'$\kappa_{decimals}$')
        plt.plot(angles, matrix_thsfree[2][0], lw = 3)
        plt.text(angles[0], (matrix_thsfree[2][0])[0], r'$\kappa_{3}$')
        
        rest = 0.5
        plt.plot(angles, matrix_thsfree[0][1], lw = rest)
        plt.plot(angles, matrix_thsfree[1][1], lw = rest)
        plt.plot(angles, matrix_thsfree[2][1], lw = rest)
        
        plt.plot(angles, matrix_thsfree[0][2], lw = rest)
        plt.plot(angles, matrix_thsfree[1][2], lw = rest)
        plt.plot(angles, matrix_thsfree[2][2], lw = rest)
    
    elif plotangle == 'thx':
        plt.plot(angles, matrix_thxfree[0][0], lw = 3)
        plt.text(angles[0], (matrix_thxfree[0][0])[0], r'$\kappa_{1}$')
        plt.plot(angles, matrix_thxfree[1][0], lw = 3)
        plt.text(angles[0], (matrix_thxfree[1][0])[0], r'$\kappa_{2}$')
        plt.plot(angles, matrix_thxfree[2][0], lw = 3)
        plt.text(angles[0], (matrix_thxfree[2][0])[0], r'$\kappa_{3}$')
        
        rest = 0.5
        plt.plot(angles, matrix_thxfree[0][1], lw = rest)
        plt.plot(angles, matrix_thxfree[1][1], lw = rest)
        plt.plot(angles, matrix_thxfree[2][1], lw = rest)
        
        plt.plot(angles, matrix_thxfree[0][2], lw = rest)
        plt.plot(angles, matrix_thxfree[1][2], lw = rest)
        plt.plot(angles, matrix_thxfree[2][2], lw = rest)
    
    elif plotangle == 'tsx':
        plt.plot(angles, matrix_thxfree[0][0], lw = 3)
        plt.text(angles[0], (matrix_thxfree[0][0])[0], r'$\kappa_{1}$')
        plt.plot(angles, matrix_thxfree[1][0], lw = 3)
        plt.text(angles[0], (matrix_thxfree[1][0])[0], r'$\kappa_{2}$')
        plt.plot(angles, matrix_thxfree[2][0], lw = 3)
        plt.text(angles[0], (matrix_thxfree[2][0])[0], r'$\kappa_{3}$')
        
        rest = 0.5
        plt.plot(angles, matrix_thxfree[0][1], lw = rest)
        plt.plot(angles, matrix_thxfree[1][1], lw = rest)
        plt.plot(angles, matrix_thxfree[2][1], lw = rest)
        
        plt.plot(angles, matrix_thxfree[0][2], lw = rest)
        plt.plot(angles, matrix_thxfree[1][2], lw = rest)
        plt.plot(angles, matrix_thxfree[2][2], lw = rest)
 

def pointfinder(epsilon, pointS, pointX, listS, listX, br):
    S = pointS
    X = pointX
    index = 0
    print(len(listS), len(listX), len(br))
    for i in range(len(br)):
        testS = (listS)[i]
        testX = (listX)[i]
        if abs(S - testS) < epsilon and abs(X - testX) < epsilon:
            epsilon = max(abs(S - testS), abs(X - testX))
            index = i
    print(index, (listS)[index], (listX)[index], (br)[index])
    return (listS)[index], (listX)[index], (br)[index]
    

def pointGen(BP, region, size, generator):
    
    def random(ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition):
        ms = np.random.uniform(ms_lowerbound, ms_upperbound, 1)
        mx = np.random.uniform(mx_lowerbound, mx_upperbound, 1)
        if condition(ms, mx):
            point = [ms, mx]
            return point
        else:
            point = random(ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition)
            return point
    
    def BP2conditionRegion1(ms, mx):
        if (5.2 * ms + 125.09 > mx):
            return True
        else: 
            return False
    
    def BP2conditionRegion2(ms, mx):
        if (5.2 * ms + 125.09 > mx) and (mx > ms + 125.09):
            return True
        else: 
            return False
    
    def BP2conditionRegion3(ms, mx):
        if (ms + 125.09 > mx) and (2 * ms < mx):
            return True
        else: 
            return False

    def BP3conditionRegion1(ms, mx):
        if (mx > 2 * ms) and (3.27 * ms + 78 > mx) and (-0.34 * ms + 641 > mx) and (mx > 2 * ms):
            return True
        else:
            return False

    def BP3conditionRegion2(ms, mx):
        if (2 * ms > mx) and ((-0.72) * ms + 745 > mx) and (mx > ms + 125.09 ):
            return True
        else:
            return False

    def BP3conditionRegion3(ms, mx):
        if (ms + 125.09 > mx) and ((-1.29) * ms + 949 > mx) and (mx > ms):
            return True
        else:
            return False

    pointlist = []
    
    if BP == 'BP2':
    
        if region == 1:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 1, 124, 250, 500, BP2conditionRegion1
            
        elif region == 2:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 1, 124, 126, 250, BP2conditionRegion2
            
        elif region == 3:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 1, 124, 126, 250, BP2conditionRegion3

        else:
            raise Exception('No region chosen')
    
    elif BP == 'BP3':
        
        if region == 1:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 126, 290, 255, 650, BP3conditionRegion1
        
        elif region == 2:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 126, 380, 255, 600, BP3conditionRegion2
            
        elif region == 3:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 126, 500, 255, 550, BP3conditionRegion3
        
        else:
            raise Exception('No region chosen')
    
    else:
        raise Exception('No BP chosen')
    
    if generator == 'random':
        
        for i in range(size):
            point = random(ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition)
            pointlist.append(point)
        return np.array(pointlist)
    
    elif generator == 'grid':
        
        mslist = np.linspace(ms_lowerbound, ms_upperbound, size)
        mxlist = np.linspace(mx_lowerbound, mx_upperbound, size)
        
        for i in range(size):
            for j in range(size):
                if condition(mslist[i], mxlist[j]):
                    pointlist.append([mslist[i], mxlist[j]])
                else:
                    continue
        return np.array(pointlist)
    
    else:
        raise Exception('No generator chosen')


def plotmarkerAuto(markers, manualmarkers, visible, decimals, fsize, x, y, n):
    for i in range(len(markers)):
        pointS, pointX, br = pointfinder(5, (markers[i])[0], (markers[i])[1], x, y, n)
        plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        if visible == True:
            plt.plot(pointS, pointX, marker = 'o', mfc = 'none', color = 'r')


def plotmarkers(x, y, n, BP, mode, decimals, fsize):
    
    ''' deprecated '''
    
    if BP == 'BP2':
        
        if mode == 'XSH':
            
            # pointS, pointX, br = pointfinder(5, 45, 220, x, y, n)
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
            # plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            # region 1
        
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 125, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
            
            # region 2 & 3  
        
            pointS, pointX, br = pointfinder(5, 80, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
        
            pointS, pointX, br = pointfinder(5, 15, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 30, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 18, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 30, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 45, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 60, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 21, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 36, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 51, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 66, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 81, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 24, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 39, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 64, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 79, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 94, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 109, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
        
        elif mode == 'XSS':
            
            # pointS, pointX, br = pointfinder(5, 50, 145, x, y, n)
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
            # plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            # region 1
            
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 125, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
            
            # region 2

            pointS, pointX, br = pointfinder(5, 22, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 20, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 38, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 42, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 55, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 25, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 46, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 70, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            # region 3 (high x mass)

            pointS, pointX, br = pointfinder(5, 60, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 77, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 75, 190, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 85, 190, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 90, 203, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 98, 215, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            # region 3 (low x mass)

            pointS, pointX, br = pointfinder(5, 20, 135, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 40, 135, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 58, 135, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 40, 150, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 60, 150, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
            
            
        
        elif mode == 'XHH':
            
            # region 1
            
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 125, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
        else:
            raise Exception('Invalid mode in markerplot')
    
    elif BP == 'BP3':
        
        if mode == 'XSH':
            
            # plt.plot(180, 475, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 180, 475, x, y, n)
            # plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            # plt.plot(225, 400, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 225, 400, x, y, n)
            # plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            # region 2
    
            pointS, pointX, br = pointfinder(5, 200, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 200, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 390, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 230, 450, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 275, 500, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 300, 490, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 325, 480, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
        
        elif mode == 'XHH':
            
            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            # region 2
    
            pointS, pointX, br = pointfinder(5, 200, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 200, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 390, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 230, 450, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 275, 500, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 300, 490, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 325, 480, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
            
            # region 3
            
            # plt.plot(220, 300, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 220, 300, x, y, n)
            # plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            
            pointS, pointX, br = pointfinder(5, 235, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 200, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 160, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 190, 300, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 235, 300, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 235, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 223, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 350, 465, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 375, 450, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

        elif mode == 'XSS':
            
            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)




def plotmarkers2(x, y, n, BP, mode, formvar, xtext, ytext, fsize, rsize, lwidth = 1, fgcolor = "w"):
    
    ''' not like plotmarkerAuto. This uses annotate and has more options. 
    All points are hard coded using pointfinder '''
    
    if BP == 'BP2':
        
        if mode == 'XSH':
            
            # pointS, pointX, br = pointfinder(5, 45, 220, x, y, n)
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
            # plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            # region 1
        
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 110, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            # region 2 & 3  
        
            pointS, pointX, br = pointfinder(5, 80, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
        
            pointS, pointX, br = pointfinder(5, 15, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 30, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 18, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 30, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 45, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 60, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 21, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 36, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 51, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 66, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 81, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 24, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 39, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 64, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 79, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 94, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 109, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
        
        elif mode == 'XSS':
            
            # pointS, pointX, br = pointfinder(5, 50, 145, x, y, n)
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            # region 1
            
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 125, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            # region 2

            pointS, pointX, br = pointfinder(5, 22, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 20, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 38, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 42, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 55, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 25, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 46, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 70, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            # region 3 (high x mass)

            pointS, pointX, br = pointfinder(5, 60, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 77, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 75, 190, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 85, 190, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 90, 203, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 98, 215, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            # region 3 (low x mass)

            pointS, pointX, br = pointfinder(5, 20, 135, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 40, 135, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 58, 135, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 40, 150, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 60, 150, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            
        
        elif mode == 'XHH':
            
            # region 1
            
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 125, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
        else:
            raise Exception('Invalid mode in markerplot')
    
    elif BP == 'BP3':
        
        if mode == 'XSH':
            
            # plt.plot(180, 475, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 180, 475, x, y, n)
            # plt.annotate(formvar.format(br), (pointS, pointX),
                 # textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 # path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            # plt.plot(225, 400, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 225, 400, x, y, n)
            # plt.annotate(formvar.format(br), (pointS, pointX),
                 # textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 # path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            pointS, pointX, br = pointfinder(5, 140, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            pointS, pointX, br = pointfinder(5, 200, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            # region 2
    
            pointS, pointX, br = pointfinder(5, 200, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 200, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 390, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 230, 450, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 275, 500, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            pointS, pointX, br = pointfinder(5, 275, 450, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 300, 490, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 325, 480, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
        
        elif mode == 'XHH':
            
            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            # region 2
    
            pointS, pointX, br = pointfinder(5, 200, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 200, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 390, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 230, 450, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 275, 500, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 300, 490, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 325, 480, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            # region 3
            
            # plt.plot(220, 300, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 220, 300, x, y, n)
            # plt.annotate(formvar.format(br), (pointS, pointX),
                 # textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 # path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            
            pointS, pointX, br = pointfinder(5, 235, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 200, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 160, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 190, 300, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 235, 300, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 235, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 223, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 350, 465, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 375, 450, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

        elif mode == 'XSS':
            
            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])





            
def plotmarkerAuto2(markers, visible, decimals, fsize, x, y, n):
    """Plots markers in a figure given a list of tuples of coordinates with the 
    value of the coordinates given by pointfinder.
    
    If visible is set to True, a red o-shaped marker is plotted in the figure.
    
    Decimals determines the number of decimals in pointfinder.
    
    fsize determines the fontsize for the value given by pointfinder.
    
    x, y, n is used by pointfinder to generate the nearest value given the marker
    points. 
    """


    for i in range(len(markers)):
        dudS, dudX, br = pointfinder(5, (markers[i])[0], (markers[i])[1], x, y, n)
        pointS, pointX = (markers[i])[0], (markers[i])[1]
        plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        if visible == True:
            plt.plot(pointS, pointX, marker = 'o', mfc = 'none', color = 'r')

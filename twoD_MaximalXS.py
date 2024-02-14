#-*- coding: utf-8 -*-
import csv
import pandas

import numpy as np
# from scipy.interpolate import CubicSpline

# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import scipy.interpolate
# mpl.rcParams.update(mpl.rcParamsDefault)

# import subprocess
# import configparser
from os import makedirs
# import datetime
# import multiprocessing
# import sys
# import json
# import copy
# import glob
# from pathlib import Path
# from itertools import repeat

import functions as TRSM
import parameterData
import twoDPlotter as twoDPlot

if __name__ == '__main__':

    def maxPrinter(pathDir, fnameModelParams='ModelParams.txt'):
        df = pandas.read_table('{pathDirString}/ModelParams.txt'.format(pathDirString=pathDir), header=None, usecols=[0], names=['col0'])
        # pathList = ['testMax/40-200/40-200_output.tsv', 'testMax/70-400/70-400_output.tsv', 'testMax/90-300/90-300_output.tsv', 'testMax/90-450/90-450_output.tsv',]
        pathList = ['{pathDirString}/{rowString}/{rowString}_output.tsv'.format(pathDirString=pathDir, rowString=row) for row in df['col0']]
        
        for pathElement in pathList:
        
            H1H2, H1H1, H2H2 = TRSM.ppXNPSM_massfree(pathElement, 'mH1', 'mH2', 'mH3',  'bb', 'gamgam',  normalizationSM=1)

            # H1H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H1H2_bbgamgam, pp_X_H1_bb_H2_gamgam, pp_X_H1_gamgam_H2_bb])

            mH1 = H1H2[0]
            mH2 = H1H2[1]
            mH3 = H1H2[2]
            pp_X_H1H2_bbgamgam   = H1H2[3]
            pp_X_H1_bb_H2_gamgam = H1H2[4] 
            pp_X_H1_gamgam_H2_bb = H1H2[5]

            pp_X_H1H1_bbgamgam = H1H1[3]
            pp_X_H2H2_bbgamgam = H2H2[3]
            
            
            print('printing cross sections of file', pathElement)
            print('$-----------------------------$')
            print('tot', np.nanmax(pp_X_H1H2_bbgamgam))
            print('$-----------------------------$')
            print('H1->bb, H2->yy',np.nanmax(pp_X_H1_bb_H2_gamgam))
            print('$-----------------------------$')
            print('H1->yy, H2->bb',np.nanmax(pp_X_H1_gamgam_H2_bb))
            print('$-----------------------------$')
            print('all: {all}'.format(all=np.nanmax(pp_X_H1H2_bbgamgam + pp_X_H1H1_bbgamgam + pp_X_H2H2_bbgamgam)))
            print('$-----------------------------$')
            print('# of np.nans in list XS lists, {a}, {b}, {c} '.format(a=sum(np.isnan(pp_X_H1H2_bbgamgam)), b=sum(np.isnan(pp_X_H1_bb_H2_gamgam)), c=sum(np.isnan(pp_X_H1_gamgam_H2_bb))))
            print('*******************************\n')
        
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
      
        # twoDPlot.maxCompiler(None, None, 'testMax2.tsv',
        #                      includeObsLim=False)
    
    maxPrinter('old/testMax')
    maxPrinter('old/testMax0.9-0.04')

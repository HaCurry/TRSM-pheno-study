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


def checkCreator2d(pointsSq, locOutputData, mxBounds, msBounds, mxKey, msKey, mhKey, **kwargs):

    ############################# kwargs #############################

    if 'mH' in kwargs:
        mH = kwargs['mH']

        if (isinstance(mH, float) == False) and (isinstance(mH, int) == False):
            raise Exception('mH need to be of type float or int') 

    else:
        mH = 125.09


    if 'ths' in kwargs:
        ths = kwargs['ths']

        if (isinstance(ths, float) == False) and (isinstance(ths, int) == False):
            raise Exception('ths need to be of type float or int') 

    else:
        raise Exception('Please provide value of ths')


    if 'thx' in kwargs:
        thx = kwargs['thx']

        if (isinstance(thx, float) == False) and (isinstance(thx, int) == False):
            raise Exception('thx need to be of type float or int') 

    else:
        raise Exception('Please provide value of thx')
    

    if 'tsx' in kwargs:
        tsx = kwargs['tsx']

        if (isinstance(tsx, float) == False) and (isinstance(tsx, int) == False):
            raise Exception('tsx need to be of type float or int') 

    else:
        raise Exception('Please provide value of tsx')


    if 'vs' in kwargs:
        vs = kwargs['vs']

        if (isinstance(vs, float) == False) and (isinstance(vs, int) == False):
            raise Exception('vs need to be of type float or int') 

    else:
        raise Exception('Please provide value of vs')


    if 'vx' in kwargs:
        vx = kwargs['vx']

        if (isinstance(vx, float) == False) and (isinstance(vx, int) == False):
            raise Exception('vx need to be of type float or int') 

    else:
        raise Exception('Please provide value of vx')

    ##################################################################

    mx = np.linspace(mxBounds[0], mxBounds[1], pointsSq)
    ms = np.linspace(msBounds[0], msBounds[1], pointsSq)

    mxToConfig = []
    msToConfig = []

    for i in mx:
        for j in ms:
            mxToConfig.append(i)
            msToConfig.append(j)        

    configDict = {}

    configDict[mxKey] = mxToConfig
    configDict[msKey] = msToConfig
    configDict[mhKey] = [mH for i in range(len(mxToConfig))]
    configDict['thetahS'] = [ths for i in range(len(mxToConfig))]
    configDict['thetahX'] = [thx for i in range(len(mxToConfig))]
    configDict['thetaSX'] = [tsx for i in range(len(mxToConfig))]
    configDict['vs'] = [vs for i in range(len(mxToConfig))]
    configDict['vx'] = [vx for i in range(len(mxToConfig))]

    df = pandas.DataFrame(data = configDict, dtype = np.float64)

    df.to_csv(locOutputData, sep = "\t")


def runTRSM(TRSMpath, configPath, locOutputData, scannerSmode, **kwargs):
    
    if scannerSmode == 'scan':

        if 'points' in kwargs:
            points = kwargs['points']

            if isinstance(points, int) == False:
                raise Exception('points need to be of type int')

            else:
                pass

        else:
            raise Exception('points need to be defined if scannerSmode is set to scan')
        
        runTRSM = ['../../../../TRSMBroken', locOutputData, '--config', configPath, 'scan', '-n', str(points)]

    elif scannerSmode == 'check':
        runTRSM = ['../../../TRSMBroken', locOutputData, 'check', configPath]


if __name__ == '__main__':
    
    # checkCreator2d(100, 'plots2D/BP2_BR_XSH/config_BP2_BR_XSH.tsv', (126, 500), (1, 124), 'mH3', 'mH1', 'mH2',
                   # ths=1.352, thx=1.175, tsx=-0.407, vs=120, vx=890)

    H1H2, H1H1, H2H2 = parameterData.dataCalculator('XNP', 'mH1', 'plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv')

    
    x = H1H2[0]
    y = H1H2[2]
    n = H1H2[3]

    # convert to arrays to make use of previous answer to similar question
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(n)

    # Set up a regular grid of interpolation points
    nInterp = 500
    xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    xi, yi = np.meshgrid(xi, yi)
    boundaryx = np.linspace(0, 600, nInterp)

    # Interpolate; there's also method='cubic' for 2-D data such as here
    #rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
    #zi = rbf(xi, yi)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')



    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    plt.imshow(zi, vmin=0.1, vmax=0.55, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=0, vmax=1, origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    plt.title(r"BP2: $BR(X\to SH)$ with $m_{S}$, $m_{X}$ free")
    plt.xlabel(r"$m_{S}$")
    plt.ylabel(r"$m_{X}$")
    plt.xlim(0,124)        
    plt.ylim(124,500)
    plt.colorbar()

    plt.plot(boundaryx, np.array([2* 125.09 for i in range(500)]), label = r'$m_{X} = 2 \cdot m_{H}$')
    plt.text(3, 235, r'$M_{X} = 2\cdot M_{H}$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

    plt.plot(boundaryx, boundaryx + 125.09, label = r'$M_{X} = M_{S} + M_{H}$')
    plt.text(26, 134, r'$M_{X} = M_{S} + M_{H}$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))#, rotation=18)

    plt.plot(boundaryx, 2*boundaryx, label = r'$m_{X} = 2 \cdot m_{S}$')
    plt.text(75, 134, r'$M_{X} = 2\cdot M_{S}$', size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))#, rotation=32)

    # pointS, pointX, br = TRSM.pointfinder(5, 45, 220, x, y, n)
    # plt.plot(pointS, pointX, marker = "x", color = 'r')
    # plt.text(pointS, pointX, r'%s'%str(round(br,2)), fontsize = 8)

    # plt.savefig('XSH_bp2.pdf')
    plt.show()
    plt.close()





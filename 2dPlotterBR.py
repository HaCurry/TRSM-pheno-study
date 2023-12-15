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


def runTRSM(TRSMpath, cwd, configName, outputName, scannerSmode, **kwargs):

    if 'capture_output' in kwargs:
        capture_output = kwargs['capture_output']

        if isinstance(capture_output, bool) == False:
            raise Exception('capture_output need to be of type bool')

        else:
            pass

    else:
        capture_output = True
        
    
    if scannerSmode == 'scan':

        if 'points' in kwargs:
            points = kwargs['points']

            if isinstance(points, int) == False:
                raise Exception('points need to be of type int')

            else:
                pass

        else:
            raise Exception('points need to be defined if scannerSmode is set to scan')
        
        runTRSM = ['../../../../TRSMBroken', outputName, '--config', configName, 'scan', '-n', str(points)]
        loglines = -17

    elif scannerSmode == 'check':
        runTRSM = ['../../../TRSMBroken', outputName, 'check', configName]
        loglines = -9

    shell_output = subprocess.run(runTRSM, capture_output = capture_output, cwd = cwd)

    if capture_output == True:
        shell_output = shell_output.stdout.decode('utf-8')
        shell_output_short = (shell_output.splitlines())[loglines:]
        for line in shell_output_short:
            print(line)
    else:
        pass


def calculateSort2D(dataPath, outputDir, outputName, SM1, SM2, **kwargs):

    if 'ppXNPnorm' in kwargs:
        ppXNPnorm = kwargs['ppXNPnorm']

    else:
        ppXNPnorm = 1

    if 'ppXNPSMnorm' in kwargs:
        ppXNPSMnorm = kwargs['ppXNPSMnorm']

    else:
        ppXNPSMnorm = 1
        
    
    XNP_H1H2, XNP_H1H1, XNP_H2H2, x_H3_gg = parameterData.dataCalculator('XNP', 'mH1', dataPath)
    ppXNP_H1H2, ppXNP_H1H1, ppXNP_H2H2 = parameterData.dataCalculator('ppXNP', 'mH1', dataPath, ggF_xs_SM_Higgs=ppXNPnorm)
    ppXNPSM_H1H2, ppXNPSM_H1H1, ppXNPSM_H2H2 = parameterData.dataCalculator('ppXNPSM', 'mH1', dataPath,
                                                                             SM1=SM1, SM2=SM2, ggF_xs_SM_Higgs_SM1SM2=ppXNPSMnorm)
    dictToTable = {}

    dictToTable['mH1'] = XNP_H1H2[0]
    dictToTable['mH2'] = XNP_H1H2[1]
    dictToTable['mH3'] = XNP_H1H2[2]

    dictToTable['b_H3_H1H2'] = XNP_H1H2[3]
    dictToTable['b_H3_H1H1'] = XNP_H1H1[3]
    dictToTable['b_H3_H2H2'] = XNP_H2H2[3]

    # df_XNP = pandas.DataFrame(data = dictXNP)
    # locOutputData = outputDir + '/' + 'XNP'
    # df_XNP.to_csv(locOutputData, sep = "\t")


    # dictppXNP = {}
    
    # dictToTable['mH1'] = ppXNP_H1H2[0]
    # dictToTable['mH2'] = ppXNP_H1H2[1]
    # dictToTable['mH3'] = ppXNP_H1H2[2]

    dictToTable['pp_X_H1H2'] = ppXNP_H1H2[4]
    dictToTable['pp_X_H1H1'] = ppXNP_H1H1[4]
    dictToTable['pp_X_H2H2'] = ppXNP_H2H2[4]

    # df_ppXNP = pandas.DataFrame(data = dictppXNP)
    # locOutputData = outputDir + '/' + 'ppXNP'
    # df_ppXNP.to_csv(locOutputData, sep = "\t")


    # dictppXNPSM = {}

    # dictToTable['mH1'] = ppXNPSM_H1H2[0]
    # dictToTable['mH2'] = ppXNPSM_H1H2[1]
    # dictToTable['mH3'] = ppXNPSM_H1H2[2]

    dictToTable['pp_X_H1H2_SM1SM2'] = ppXNPSM_H1H2[3]
    dictToTable['pp_X_H1_SM1_H2_SM2'] = ppXNPSM_H1H2[4]
    dictToTable['pp_X_H1_SM2_H2_SM1'] = ppXNPSM_H1H2[5]

    dictToTable['pp_X_H1H1_SM1SM2'] = ppXNPSM_H1H1[3]
    dictToTable['pp_X_H2H2_SM1SM2'] = ppXNPSM_H2H2[3]

    # df_ppXNPSM = pandas.DataFrame(data = dictppXNPSM)
    # locOutputData = outputDir + '/' + 'ppXNPSM'
    # df_ppXNPSM.to_csv(locOutputData, sep = "\t")

    df = pandas.DataFrame(data = dictToTable)
    fname = outputDir + '/' + outputName
    df.to_csv(fname, sep = "\t")

    XNP = [XNP_H1H2, XNP_H1H1, XNP_H2H2]
    ppXNP = [ppXNP_H1H2, ppXNP_H1H1, ppXNP_H2H2 ]
    ppXNPSM = [ppXNPSM_H1H2, ppXNPSM_H1H1, ppXNPSM_H2H2 ] 
    
    return XNP, ppXNP, ppXNPSM


def calculateSort2D(generalPhysics, locOutputData, xIndex, yIndex, zIndex):

    if 'vmin' in kwargs and 'vmax' in kwargs:
        vmin = kwargs['vmin']
        vmax = kwargs['vmax']

    elif 'vmin' in kwargs or 'vmax' in kwargs:
        raise Exception('Please specify both vmin and vmax')

    else:
        vmin = 'None'
        vmax = 'None'

    if 'nInterp' in kwargs:
        nInterp = kwargs['nInterp']
        if isinstance(nInterp, int) == False:
            raise Exception('nInterp need to be of type int')

    else:
        nInterp = 500
        
    if 'mode' in kwargs:

        if kwargs['mode'] == 'H1H2':
            mode = 'H1H2'

        elif kwargs['mode'] == 'H1H1':
            mode = 'H1H1'

        elif kwargs['mode'] == 'H2H2':
            mode = 'H2H2'

        else:
            raise Exception('Invalid mode, please set mode to \'H1H2\', \'H1H1\', \'H2H2\'')

    else:
        mode = 'H1H2'

    if 'methodInterp' in kwargs:
        methodInterp = kwargs['methodInterp']
    
    else:
        methodInterp = 'linear'

    if 'xlims' in kwargs and 'ylims' in kwargs:
        xlims = kwargs['xlims']
        ylims = kwargs['ylims']

    elif 'xlims' in kwargs or 'ylims' in kwargs:
        raise Exception('Only provide both xlims and ylims or none at all')

    else:
        xlims = (None, None)
        ylims = (None, None)
    

    
    H1H2, H1H1, H2H2 = parameterData.dataCalculator(generalPhysics, 'mH1', locOutputData)

    if mode == 'H1H2':
        x = H1H2[xIndex]
        y = H1H2[yIndex]
        n = H1H2[zIndex]

    elif mode == 'H1H1':
        x = H1H2[xIndex]
        y = H1H2[yIndex]
        n = H1H2[zIndex]

    elif mode == 'H2H2':
        x = H1H2[xIndex]
        y = H1H2[yIndex]
        n = H1H2[zIndex]

    else:
        raise Exception('Invalid mode, please set mode to \'H1H2\', \'H1H1\', \'H2H2\'')

    # convert to arrays to make use of previous answer to similar question
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(n)

    # Set up a regular grid of interpolation points
    xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate; there's also method='cubic' for 2-D data such as here
    #rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
    #zi = rbf(xi, yi)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method=methodInterp)

    if vmin == 'None' and vmax == 'None':

        zmin = z.min()
        zmax = z.max()

        if zLog == True:
            plt.imshow(zi, norm=mpl.colors.LogNorm(), origin='lower',
                        extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

        elif zLog == False:
            plt.imshow(zi, vmin=zmin, vmax=zmax, origin='lower',
                        extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
        
    else:
        zmin = vmin
        zmax = vmax

        if zLog == True:
            plt.imshow(zi, norm=mpl.colors.LogNorm(vmin=zmin, vmax=zmax), origin='lower',
                        extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

        elif zLog == False:
            plt.imshow(zi, vmin=zmin, vmax=zmax, origin='lower',
                        extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    plt.xlabel('r$M_{S}$')
    plt.ylabel('r$M_{X}$')
    plt.title(title)
    plt.xlim(xbounds)
    plt.ylim(ybounds)


if __name__ == '__main__':

    #### BP2 ####
    
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
    plt.title(r"BP2: $BR(X\to SH)$ with $M_{S}$, $M_{X}$ free")
    plt.xlabel(r"$M_{S}$")
    plt.ylabel(r"$M_{X}$")
    plt.xlim(0,124)        
    plt.ylim(124,500)
    plt.colorbar()

    plt.plot(boundaryx, np.array([2* 125.09 for i in range(500)]), label = r'$m_{X} = 2 \cdot m_{H}$', ls = 'dashed')
    plt.text(3, 235, r'$M_{X} = 2\cdot M_{H}$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

    plt.plot(boundaryx, boundaryx + 125.09, label = r'$M_{X} = M_{S} + M_{H}$', ls = 'dashed')
    plt.text(26, 134, r'$M_{X} = M_{S} + M_{H}$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))#, rotation=18)

    plt.plot(boundaryx, 2*boundaryx, label = r'$m_{X} = 2 \cdot m_{S}$', ls = 'dashed')
    plt.text(75, 134, r'$M_{X} = 2\cdot M_{S}$', size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))#, rotation=32)

    plt.show()
    plt.savefig('BP2_BR_XSH_fig.pdf')
    plt.close()


    #### BP3 ####

    # checkCreator2d(100, 'plots2D/BP3_BR_XSH/config_BP3_BR_XSH.tsv', (255, 650), (126, 500), 'mH3', 'mH2', 'mH1',
    #              # ths=-0.129, thx=0.226, tsx=-0.899, vs=140, vx=100)

    # runTRSM('../../../TRSMBroken', 'plots2D/BP3_BR_XSH', 'config_BP3_BR_XSH.tsv', 'output_BP3_BR_XSH.tsv', 'check')

    # H1H2, H1H1, H2H2 = parameterData.dataCalculator('XNP', 'mH1', 'plots2D/BP3_BR_XSH/output_BP3_BR_XSH.tsv')

    # # code from stackexchange
    # x = H1H2[1]
    # y = H1H2[2]
    # n = H1H2[3]

    # # convert to arrays to make use of previous answer to similar question
    # x = np.asarray(x)
    # y = np.asarray(y)
    # z = np.asarray(n)

    # # Set up a regular grid of interpolation points
    # nInterp = 500
    # xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    # xi, yi = np.meshgrid(xi, yi)
    # boundaryx = np.linspace(x.min(), 500)


    # # Interpolate; there's also method='cubic' for 2-D data such as here
    # #rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
    # #zi = rbf(xi, yi)
    # zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # # with np.printoptions(threshold=np.inf):
    # #     print(zi)


    # # plt.imshow(zi, vmin=0, vmax=0.6, origin='lower',
    # #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.title(r"BP3: $BR(X\to SH)$ ")
    # plt.xlim(124, 400)
    # plt.ylim(255, 600)
    # plt.xlabel(r"$M_{S}$")
    # plt.ylabel(r"$M_{X}$")        
    # plt.colorbar(label = r'$BR(X\to SH)$')

    # plt.plot(boundaryx, 2*boundaryx, color = 'C0', label = r'$M_{X} = 2M_{S}$')
    # plt.text(298, 575, r'$M_{X} = 2\cdot M_{S}$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

    # plt.plot(boundaryx, boundaryx + 125.09, color = 'C1', label = r'$M_{X} = M_{S} + M_H$')
    # plt.text(337, 445, r'$M_{X} = M_{S} + M_{H}$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))

    # plt.plot(boundaryx, boundaryx, color = 'C2', label = r'$M_{X} = M_{S}$')
    # plt.text(353, 336, r'$M_{X} = M_{S}$', size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))


    # plt.savefig('plots2D/BP3_BR_XSH/BP3_BR_XSH_fig.pdf')
    # plt.show()

    # plt.scatter(x, y, c=n, cmap='viridis')
    # plt.colorbar()
    # plt.show()



    #### BP5 ####
    
    # checkCreator2d(100, 'plots2D/BP5_BR_XSH/config_BP5_BR_XSH.tsv', (126, 500), (1, 124), 'mH3', 'mH1', 'mH2',
    #                ths=-1.498, thx=0.251, tsx=0.271, vs=50, vx=720)

    # runTRSM('../../../TRSMBroken', 'plots2D/BP5_BR_XSH/', 'config_BP5_BR_XSH.tsv', 'output_BP5_BR_XSH.tsv', 'check', capture_output=False)

    # H1H2, H1H1, H2H2 = parameterData.dataCalculator('XNP', 'mH1', 'plots2D/BP5_BR_XSH/output_BP5_BR_XSH.tsv')

    # x = H1H2[0]
    # y = H1H2[2]
    # n = H1H2[3]

    # # convert to arrays to make use of previous answer to similar question
    # x = np.asarray(x)
    # y = np.asarray(y)
    # z = np.asarray(n)

    # # Set up a regular grid of interpolation points
    # nInterp = 500
    # xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    # xi, yi = np.meshgrid(xi, yi)
    # boundaryx = np.linspace(0, 600, nInterp)

    # # Interpolate; there's also method='cubic' for 2-D data such as here
    # #rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
    # #zi = rbf(xi, yi)
    # zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')



    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # # plt.imshow(zi, vmin=0.80, vmax=1.0, origin='lower',
    #             # extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # # plt.imshow(zi, vmin=0, vmax=1, origin='lower',
    # #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.title(r"BP5: $BR(X\to SH)$ with $M_{S}$, $M_{X}$ free")
    # plt.xlabel(r"$M_{S}$")
    # plt.ylabel(r"$M_{X}$")
    # plt.xlim(0,124)        
    # plt.ylim(124,500)
    # plt.colorbar()

    # plt.plot(boundaryx, np.array([2* 125.09 for i in range(500)]), label = r'$m_{X} = 2 \cdot m_{H}$', ls = 'dashed')
    # plt.text(3, 235, r'$M_{X} = 2\cdot M_{H}$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

    # plt.plot(boundaryx, boundaryx + 125.09, label = r'$M_{X} = M_{S} + M_{H}$', ls = 'dashed')
    # plt.text(26, 134, r'$M_{X} = M_{S} + M_{H}$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))#, rotation=18)

    # plt.plot(boundaryx, 2*boundaryx, label = r'$m_{X} = 2 \cdot m_{S}$', ls = 'dashed')
    # plt.text(75, 134, r'$M_{X} = 2\cdot M_{S}$', size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))#, rotation=32)

    # plt.savefig('plots2D/BP5_BR_XSH/BP5_BR_XSH_fig.pdf')
    # plt.show()
    # plt.close()


    #### BP6 ####

    # checkCreator2d(50, 'plots2D/BP6_BR_XSH/config_BP6_BR_XSH.tsv', (255, 850), (126, 400), 'mH3', 'mH2', 'mH1',
    #                ths=0.207, thx=0.146, tsx=0.782, vs=220, vx=150)

    # runTRSM('../../../TRSMBroken', 'plots2D/BP6_BR_XSH/', 'config_BP6_BR_XSH.tsv', 'output_BP6_BR_XSH.tsv', 'check', capture_output=False)

    # H1H2, H1H1, H2H2 = parameterData.dataCalculator('XNP', 'mH1', 'plots2D/BP6_BR_XSH/output_BP6_BR_XSH.tsv')

    ## try2 start ##

    # checkCreator2d(100, 'plots2D/BP6_BR_XSH_try2/config_BP6_BR_XSH.tsv', (255, 850), (126, 400), 'mH3', 'mH2', 'mH1',
    #                ths=0.207, thx=0.146, tsx=0.782, vs=220, vx=150)

    # runTRSM('../../../TRSMBroken', 'plots2D/BP6_BR_XSH_try2/', 'config_BP6_BR_XSH.tsv', 'output_BP6_BR_XSH.tsv', 'check', capture_output=False)

    # H1H2, H1H1, H2H2 = parameterData.dataCalculator('XNP', 'mH1', 'plots2D/BP6_BR_XSH_try2/output_BP6_BR_XSH.tsv')

    ## try2 end ##

    # # code from stackexchange
    # x = H1H2[1]
    # y = H1H2[2]
    # n = H1H2[3]

    # # convert to arrays to make use of previous answer to similar question
    # x = np.asarray(x)
    # y = np.asarray(y)
    # z = np.asarray(n)

    # # Set up a regular grid of interpolation points
    # nInterp = 500
    # xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    # xi, yi = np.meshgrid(xi, yi)
    # boundaryx = np.linspace(x.min(), 500)


    # # Interpolate; there's also method='cubic' for 2-D data such as here
    # #rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
    # #zi = rbf(xi, yi)
    # zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # # with np.printoptions(threshold=np.inf):
    # #     print(zi)


    # plt.imshow(zi, vmin=0.50, vmax=0.85, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.title(r"BP6: $BR(X\to SH)$ ")
    # plt.xlim(124, 500)
    # plt.ylim(255, 1000)
    # plt.xlabel(r"$M_{S}$")
    # plt.ylabel(r"$M_{X}$")        
    # plt.colorbar(label = r'$BR(X\to SH)$')

    # plt.plot(boundaryx, 2*boundaryx, color = 'C0', label = r'$M_{X} = 2M_{S}$')
    # plt.text(298, 575, r'$M_{X} = 2\cdot M_{S}$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

    # plt.plot(boundaryx, boundaryx + 125.09, color = 'C1', label = r'$M_{X} = M_{S} + M_H$')
    # plt.text(337, 445, r'$M_{X} = M_{S} + M_{H}$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))

    # plt.plot(boundaryx, boundaryx, color = 'C2', label = r'$M_{X} = M_{S}$')
    # plt.text(353, 336, r'$M_{X} = M_{S}$', size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))


    # plt.savefig('plots2D/BP6_BR_XSH/BP6_BR_XSH_fig.pdf')
    # # plt.savefig('plots2D/BP6_BR_XSH_try2/BP6_BR_XSH_fig.pdf')
    # plt.show()
    # plt.close()

    # plt.scatter(x,y, c=z)
    # plt.show()
    # plt.close()


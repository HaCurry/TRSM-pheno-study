#-*- coding: utf-8 -*-
import pandas

import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.interpolate
mpl.rcParams.update(mpl.rcParamsDefault)
import mplhep as hep

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
import twoDPlotter as twoDPlot



if __name__ == '__main__':

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19

    ### BP2 ####

    BP2 = {'mH3_lb': 126,       'mH3_ub': 1000,   'mH3Points': 100,
            'mH1_lb': 1,         'mH1_ub': 124,    'mH1Points': 100,
            'mH2_lb': 125.09,    'mH2_ub': 125.09,
            'thetahS_lb': 1.352, 'thetahS_ub': 1.352,
            'thetahX_lb': 1.175, 'thetahX_ub': 1.175,
            'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407,
            'vs_lb': 120, 'vs_ub': 120,
            'vx_lb': 890, 'vx_ub': 890, } 

    # twoDPlot.checkCreatorNew('plots2D/BP2_BR_XSH/BP2_extendedMass/config_BP2_BR_XSH_extendedMass.tsv', BP2, 
    #                          modelParams=['mH3', 'mH1', 'mH2', 'thetahS', 'thetahX', 'thetaSX', 'vs', 'vx'])

    # twoDPlot.runTRSM('../../../../TRSMBroken', 'plots2D/BP2_BR_XSH/BP2_extendedMass', 'config_BP2_BR_XSH_extendedMass.tsv', 'output_BP2_BR_XSH_extendedMass.tsv', 'check', capture_output=False)

    # twoDPlot.calculateSort2D('plots2D/BP2_BR_XSH/BP2_extendedMass/output_BP2_BR_XSH_extendedMass.tsv', 'plots2D/BP2_BR_XSH/BP2_extendedMass', 'calc_BP2_extendedMass.tsv', 'bb', 'gamgam')


    BP2_mH1, BP2_mH2, BP2_mH3, BP2_b_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/BP2_extendedMass/calc_BP2_extendedMass.tsv', 'mH1', 'mH2', 'mH3', 'b_H3_H1H2')
    # # BP2_mH1, BP2_mH2, BP2_mH3, BP2_b_H3_H1H2 = twoDPlot.kineticExcluder(BP2_mH1, BP2_mH2, BP2_mH3, BP2_b_H3_H1H2)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_b_H3_H1H2)

    plt.scatter(x, y, c=z)
    plt.colorbar()
    plt.xlim(1,124)
    plt.ylim(126,1000)
    plt.savefig('plots2D/BP2_BR_XSH/BP2_extendedMass/BP2_BR_XSH_fig_extendedmass.pdf')
    # plt.show()
    plt.close()

    # df_1 = pandas.read_table('plots2D/BP2_BR_XSH/BP2_extendedMass/calc_BP2_extendedMassTEST.tsv')
    # df_2 = pandas.read_table('plots2D/BP2_BR_XSH/BP2_extendedMass/calc_BP2_extendedMass.tsv')
    # df_1 = pandas.read_table('plots2D/BP2_BR_XSH/BP2_extendedMass/config_BP2_BR_XSH_extendedMass.tsv')
    # df_2 = pandas.read_table('plots2D/BP2_BR_XSH/BP2_extendedMass/config_BP2_BR_XSH_extendedMassTEST.tsv')
    # print(df_1.columns.tolist())
    # print(df_2.columns.tolist())
    # lines below are from
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html
    # https://stackoverflow.com/a/55358370/17456342
    # df11 = df_1.sort_values(by=df_1.columns.tolist()).reset_index(drop=True)
    # df21 = df_2.sort_values(by=df_2.columns.tolist()).reset_index(drop=True)
    
    # print(df11.equals(df21))


    ### BP3 ####

    BP3 =  {'mH1_lb': 125.09,    'mH1_ub': 125.09,
            'mH2_lb': 126,       'mH2_ub': 500, 'mH2Points': 100,
            'mH3_lb': 255,       'mH3_ub': 650, 'mH3Points': 100,
            'thetahS_lb': -0.129, 'thetahS_ub': -0.129,
            'thetahX_lb': 0.226,  'thetahX_ub': 0.226,
            'thetaSX_lb': -0.899, 'thetaSX_ub': -0.899,
            'vs_lb': 140, 'vs_ub': 140,
            'vx_lb': 100, 'vx_ub': 100, } 

    # twoDPlot.checkCreatorNew('plots2D/BP3_BR_XSH/BP3_extendedMass/config_BP3_BR_XSH_extendedMass.tsv', BP3, massOrder=True)
    #                          # modelParams=['mH3', 'mH2', 'mH1', 'thetahS', 'thetahX', 'thetaSX', 'vs', 'vx'], massOrder=True)

    # twoDPlot.runTRSM('../../../../TRSMBroken', 'plots2D/BP3_BR_XSH/BP3_extendedMass', 'config_BP3_BR_XSH_extendedMass.tsv', 'output_BP3_BR_XSH_extendedMass.tsv', 'check', capture_output=False,
    #                  BFB=1, Uni=1, STU=1, Higgs=1)

    # twoDPlot.calculateSort2D('plots2D/BP3_BR_XSH/BP3_extendedMass/output_BP3_BR_XSH_extendedMass.tsv', 'plots2D/BP3_BR_XSH/BP3_extendedMass', 'calc_BP3_extendedMass.tsv', 'bb', 'gamgam')


    BP3_mH1, BP3_mH2, BP3_mH3, BP3_b_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/BP3_extendedMass/calc_BP3_extendedMass.tsv', 'mH1', 'mH2', 'mH3', 'b_H3_H1H2')
    # # BP3_mH1, BP3_mH2, BP3_mH3, BP3_b_H3_H1H2 = twoDPlot.kineticExcluder(BP3_mH1, BP3_mH2, BP3_mH3, BP3_b_H3_H1H2)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_b_H3_H1H2)

    plt.scatter(x, y, c=z, vmin=0.0, vmax=0.7788997810065152)
    # [plt.annotate("{:.2f}".format(z[i]) ,(x[i],y[i])) for i in range(len(z))]
    print(np.nanmin(z), np.nanmax(z))
    plt.colorbar()
    plt.xlim(126,500)
    plt.ylim(255,650)
    plt.savefig('plots2D/BP3_BR_XSH/BP3_extendedMass/BP3_BR_XSH_fig_extendedmass.pdf')
    # plt.show()

    df_1_con = pandas.read_table('plots2D/BP3_BR_XSH/BP3_extendedMass/config_BP3_BR_XSH_extendedMass.tsv')
    df_1_con = df_1_con[['mH1', 'mH2', 'mH3', 'thetahS', 'thetahX', 'thetaSX', 'vs', 'vx']]
    df_2_con = pandas.read_table('plots2D/BP3_BR_XSH/BP3_extendedMass/config_BP3_BR_XSH_extendedMassTEST.tsv')
    df_2_con = df_2_con[['mH1', 'mH2', 'mH3', 'thetahS', 'thetahX', 'thetaSX', 'vs', 'vx']]

    df_1_out = pandas.read_table('plots2D/BP3_BR_XSH/BP3_extendedMass/output_BP3_BR_XSH_extendedMass.tsv')
    df_1_out = df_1_out[['mH1', 'mH2', 'mH3', 'thetahS', 'thetahX', 'thetaSX', 'vs', 'vx']]
    df_2_out = pandas.read_table('plots2D/BP3_BR_XSH/BP3_extendedMass/output_BP3_BR_XSH_extendedMassTEST.tsv')
    df_2_out = df_2_out[['mH1', 'mH2', 'mH3', 'thetahS', 'thetahX', 'thetaSX', 'vs', 'vx']]

    df_1_cal = pandas.read_table('plots2D/BP3_BR_XSH/BP3_extendedMass/calc_BP3_extendedMassTEST.tsv')
    df_1_cal = df_1_cal[['mH1', 'mH2', 'mH3']]
    df_2_cal = pandas.read_table('plots2D/BP3_BR_XSH/BP3_extendedMass/calc_BP3_extendedMass.tsv')
    df_2_cal = df_2_cal[['mH1', 'mH2', 'mH3']]

    print(df_1_con.columns.tolist())
    print(len(df_1_con))
    print(df_2_con.columns.tolist())
    print(len(df_2_con))
    # lines below are from
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html
    # https://stackoverflow.com/a/55358370/17456342
    df11_con = df_1_con.sort_values(by=df_1_con.columns.tolist()).reset_index(drop=True)
    df21_con = df_2_con.sort_values(by=df_2_con.columns.tolist()).reset_index(drop=True)

    df11_out = df_1_out.sort_values(by=df_1_out.columns.tolist()).reset_index(drop=True)
    df21_out = df_2_out.sort_values(by=df_2_out.columns.tolist()).reset_index(drop=True)

    df11_cal = df_1_cal.sort_values(by=df_1_cal.columns.tolist()).reset_index(drop=True)
    df21_cal = df_2_cal.sort_values(by=df_2_cal.columns.tolist()).reset_index(drop=True)

    print(df_1_con)
    print(df_2_con)
    print('config equal?', df11_con.equals(df21_con))
    # df11_out = df_1_out.sort_values(by=df_1_out.columns.tolist()).reset_index(drop=True)
    # df21_out = df_2_out.sort_values(by=df_2_out.columns.tolist()).reset_index(drop=True)
    print('output equal?', df11_out.equals(df21_out))
    # df11_cal = df_1_cal.sort_values(by=df_1_cal.columns.tolist()).reset_index(drop=True)
    # df21_cal = df_2_cal.sort_values(by=df_2_cal.columns.tolist()).reset_index(drop=True)
    print('calculate equal?', df11_cal.equals(df21_cal))
# 342.77777777777777	292

##### testing #####

    # twoDPlot.runTRSM('../../../../TRSMBroken', 'plots2D/BP3_BR_XSH/BP3_extendedMass', 'test.tsv', 'testoutput.tsv', 'check', capture_output=False)

    # twoDPlot.calculateSort2D('plots2D/BP3_BR_XSH/BP3_extendedMass/testoutput.tsv', 'plots2D/BP3_BR_XSH/BP3_extendedMass', 'testcalc.tsv', 'bb', 'gamgam')

    # BP3_mH1, BP3_mH2, BP3_mH3, BP3_b_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/BP3_extendedMass/testcalc.tsv', 'mH1', 'mH2', 'mH3', 'b_H3_H1H2')
    # # BP3_mH1, BP3_mH2, BP3_mH3, BP3_b_H3_H1H2 = twoDPlot.kineticExcluder(BP3_mH1, BP3_mH2, BP3_mH3, BP3_b_H3_H1H2)

    # x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_b_H3_H1H2)

    # plt.scatter(x, y, c=z, vmin=0.0, vmax=0.7788997810065152)
    # [plt.annotate("{:.2f}".format(z[i]) ,(x[i],y[i])) for i in range(len(z))]
    # print(np.nanmin(z), np.nanmax(z))
    # plt.colorbar()
    # plt.xlim(126,500)
    # plt.ylim(255,650)
    # # plt.savefig('plots2D/BP3_BR_XSH/BP3_extendedMass/BP2_BR_XSH_fig_extendedmass.pdf')
    # plt.show()

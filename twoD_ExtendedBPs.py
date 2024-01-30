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

    # twoDPlot.checkCreator2d(100, 'plots2D/BP2_BR_XSH/BP2_extendedMass/config_BP2_BR_XSH_extendedMass.tsv', (126, 1000), (1, 124), 'mH3', 'mH1', 'mH2',
    #              ths=1.352, thx=1.175, tsx=-0.407, vs=120, vx=890)

    # twoDPlot.runTRSM('../../../../TRSMBroken', 'plots2D/BP2_BR_XSH/BP2_extendedMass', 'config_BP2_BR_XSH_extendedMass.tsv', 'output_BP2_BR_XSH_extendedMass.tsv', 'check', capture_output=False)

    twoDPlot.calculateSort2D('plots2D/BP2_BR_XSH/BP2_extendedMass/output_BP2_BR_XSH_extendedMass.tsv', 'plots2D/BP2_BR_XSH/BP2_extendedMass', 'calc_BP2_extendedMass.tsv', 'bb', 'gamgam')

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_b_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/BP2_extendedMass/calc_BP2_extendedMass.tsv', 'mH1', 'mH2', 'mH3', 'b_H3_H1H2')
    # BP2_mH1, BP2_mH2, BP2_mH3, BP2_b_H3_H1H2 = twoDPlot.kineticExcluder(BP2_mH1, BP2_mH2, BP2_mH3, BP2_b_H3_H1H2)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_b_H3_H1H2)

    plt.scatter(x, y, c=z)
    plt.colorbar()
    plt.xlim(1,124)
    plt.ylim(126,1000)
    plt.savefig('plots2D/BP2_BR_XSH/BP2_extendedMass/BP2_BR_XSH_fig_extendedmass.pdf')
    # plt.show()


    ### BP3 ####

    # twoDPlot.checkCreator2d(100, 'plots2D/BP3_BR_XSH/BP3_extendedMass/config_BP3_BR_XSH_extendedMass.tsv', (255, 1000), (126, 500), 'mH3', 'mH2', 'mH1',
    #              ths=-0.129, thx=0.226, tsx=-0.899, vs=140, vx=100)

    # twoDPlot.runTRSM('../../../../TRSMBroken', 'plots2D/BP3_BR_XSH/BP3_extendedMass', 'config_BP3_BR_XSH_extendedMass.tsv', 'output_BP3_BR_XSH_extendedMass.tsv', 'check', capture_output=False)

    twoDPlot.calculateSort2D('plots2D/BP3_BR_XSH/BP3_extendedMass/output_BP3_BR_XSH_extendedMass.tsv', 'plots2D/BP3_BR_XSH/BP3_extendedMass', 'calc_BP3_extendedMass.tsv', 'bb', 'gamgam')

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_b_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/BP3_extendedMass/calc_BP3_extendedMass.tsv', 'mH1', 'mH2', 'mH3', 'b_H3_H1H2')
    # BP3_mH1, BP3_mH2, BP3_mH3, BP3_b_H3_H1H2 = twoDPlot.kineticExcluder(BP3_mH1, BP3_mH2, BP3_mH3, BP3_b_H3_H1H2)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_b_H3_H1H2)

    plt.scatter(x, y, c=z)
    plt.colorbar()
    plt.xlim(126,500)
    plt.ylim(255,1000)
    plt.savefig('plots2D/BP3_BR_XSH/BP3_extendedMass/BP2_BR_XSH_fig_extendedmass.pdf')
    # plt.show()


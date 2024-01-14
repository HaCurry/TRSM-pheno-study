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
import twoDPlotter as twoDPlot


if __name__ == '__main__':

    ### BP2:
    
    ### create dict with settings: repackingProgramParametersDict
    # BP2dict = parameterData.repackingProgramParamDict({'mHa_lb': 1, 'mHa_ub': 124, 'mHb_lb': 125.09, 'mHb_ub': 125.09, 'mHc_lb': 250, 'mHc_ub':250}, BP='BP2')

    # parameterData.checkCreator('thesisAuxiliaryData/config_BP2_bbgamgam.tsv', BP2dict, 1000)
    # runTRSM = ['../../TRSMBroken', '--BFB', '0', '--Uni', '0', '--STU', '0', '--Higgs', '0', 'output_BP2_bbgamgam.tsv', 'check', 'config_BP2_bbgamgam.tsv']
    # shell_output = subprocess.run(runTRSM, cwd = 'thesisAuxiliaryData/')
    
    H1H2, H1H1, H2H2 = TRSM.NPSM_massfree('thesisAuxiliaryData/output_BP2_bbgamgam.tsv', 'mH1', 'mH2', 'mH3', 'bb', 'gamgam')

    plt.plot(H1H2[0], H1H2[3], ls='solid', label=r'$h_{1}h_{2} \ \to \ b\bar{b}\gamma\gamma$')
    # plt.text(100, 0.0037, r'$h_{1}h_{2}\to b\bar{b}\gamma\gamma$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))
    # plt.text((H1H2[0])[-100], (H1H2[3])[-100], r'$h_{1}h_{2}\to b\bar{b}\to\gamma\gamma$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

    plt.plot(H1H2[0], H1H2[4], ls='solid', label=r'$h_{1} \ \to \ b\bar{b}, \ h_{2} \ \to \ \gamma\gamma$')
    # plt.text(67.5, 0.0012, r'$h_{1}\to b\bar{b},h_{2}\to\gamma\gamma$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))
    # plt.text((H1H2[0])[-100], (H1H2[4])[-100], r'$h_{1}\to b\bar{b},h_{2}\to\gamma\gamma$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))

    plt.plot(H1H2[0], H1H2[5], ls='solid', label=r'$h_{1} \ \to \ \gamma\gamma, \ h_{2} \ \to \ b\bar{b}$')
    # plt.text(87.5, 0.0004, r'$h_{1}\to \gamma\gamma, h_{2}\to b\bar{b}$', size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))

    plt.yscale('log')
    plt.legend()
    plt.ylim(10**(-4), 10**(0))
    plt.xlim(1,124)
    plt.xlabel('$M_{1}$')
    plt.ylabel('$\mathrm{BR}$')
    plt.title(r'BP3: branching ratio of Higgs to $b\bar{b}$, $\gamma\gamma$')
    plt.savefig('thesisAuxiliaryData/plot_BP2_bbgamgam.pdf')
    plt.show()
    plt.close()

    ### BP3: 
    
    ### create dict with settings: repackingProgramParametersDict
    # BP3dict = parameterData.repackingProgramParamDict({'mHa_lb': 125.09, 'mHa_ub': 125.09, 'mHb_lb': 126, 'mHb_ub': 500, 'mHc_lb': 640, 'mHc_ub':640}, BP='BP3')

    # parameterData.checkCreator('thesisAuxiliaryData/config_BP3_bbgamgam.tsv', BP3dict, 1000)
    # runTRSM = ['../../TRSMBroken', '--BFB', '0', '--Uni', '0', '--STU', '0', '--Higgs', '0', 'output_BP3_bbgamgam.tsv', 'check', 'config_BP3_bbgamgam.tsv']
    # shell_output = subprocess.run(runTRSM, cwd = 'thesisAuxiliaryData/')
    
    H1H2, H1H1, H2H2 = TRSM.NPSM_massfree('thesisAuxiliaryData/output_BP3_bbgamgam.tsv', 'mH1', 'mH2', 'mH3', 'bb', 'gamgam')

    plt.plot(H1H2[1], H1H2[3], ls='solid', label=r'$h_{1}h_{2} \ \to \ b\bar{b}\gamma\gamma$')
    # plt.text(100, 0.0037, r'$h_{1}h_{2}\to b\bar{b}\gamma\gamma$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))
    # plt.text((H1H2[0])[-100], (H1H2[3])[-100], r'$h_{1}h_{2}\to b\bar{b}\to\gamma\gamma$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

    plt.plot(H1H2[1], H1H2[4], ls='solid', label=r'$h_{1} \ \to \ b\bar{b}, \ h_{2} \ \to \ \gamma\gamma$')
    # plt.text(67.5, 0.0012, r'$h_{1}\to b\bar{b},h_{2}\to\gamma\gamma$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))
    # plt.text((H1H2[0])[-100], (H1H2[4])[-100], r'$h_{1}\to b\bar{b},h_{2}\to\gamma\gamma$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))

    plt.plot(H1H2[1], H1H2[5], ls='solid', label=r'$h_{1} \ \to \ \gamma\gamma, \ h_{2} \ \to \ b\bar{b}$')
    # plt.text(87.5, 0.0004, r'$h_{1}\to \gamma\gamma, h_{2}\to b\bar{b}$', size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))

    plt.yscale('log')
    plt.legend()
    # plt.ylim(10**(-4), 10**(0))
    plt.xlim(126,500)
    plt.xlabel('$M_{2}$')
    plt.ylabel('$\mathrm{BR}$')
    plt.title(r'BP2: branching ratio of Higgs to $b\bar{b}$, $\gamma\gamma$')
    plt.savefig('thesisAuxiliaryData/plot_BP3_bbgamgam.pdf')
    plt.show()
    plt.close()

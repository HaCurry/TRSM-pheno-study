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


if __name__ == "__main__":
    twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP2_check_prel_Mproc', 'compiled_AtlasBP2_check_prel_Mproc.tsv',
                      msKey='mHa_ub', mxKey='mHc_ub')   
    twoDPlot.exclusionPlotter('compiled_AtlasBP2_check_prel_Mproc.tsv', 'plotsLimits', 0, 
                     xlims=(1, 124), ylims=(126, 500), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1H2_SM_1')


    twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP3_check_prel_Mproc', 'compiled_AtlasBP3_check_prel_Mproc.tsv',
                      msKey='mHb_ub', mxKey='mHc_ub')   
    twoDPlot.exclusionPlotter('compiled_AtlasBP3_check_prel_Mproc.tsv', 'plotsLimits', 0, 
                     xlims=(126, 500), ylims=(255, 650), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1H2_SM_1')


    twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP5_check_prel_Mproc', 'compiled_AtlasBP5_check_prel_Mproc.tsv',
                      msKey='mHa_ub', mxKey='mHc_ub')   
    twoDPlot.exclusionPlotter('compiled_AtlasBP5_check_prel_Mproc.tsv', 'plotsLimits', 0, 
                     xlims=(1, 124), ylims=(126, 500), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1H2_SM_1')


    twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP6_check_prel_Mproc', 'compiled_AtlasBP6_check_prel_Mproc.tsv',
                      msKey='mHb_ub', mxKey='mHc_ub')   
    twoDPlot.exclusionPlotter('compiled_AtlasBP6_check_prel_Mproc.tsv', 'plotsLimits', 0, 
                     xlims=(126, 500), ylims=(255, 1000), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1H2_SM_1')

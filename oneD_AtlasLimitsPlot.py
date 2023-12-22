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
import parameterPlotter

if __name__ == "__main__":

    parameterPlotter.parameterPlot('calc_AtlasBP2_check_prel', '/**/settingsCalc_*.json', 'plot_AtlasBP2_check_prel', 'H1H2', True, True, 
                  ppXNPSM=True,ShowObsLimit=True, SM1='bb', SM2='gamgam', SMmode='1', saveStep=True, yscale='log', ylims=(10**(-8),8*10**(-2)))

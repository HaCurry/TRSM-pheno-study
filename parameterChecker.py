# -*- coding: utf-8 -*-
import csv
import pandas

import numpy as np
from scipy.interpolate import CubicSpline

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

targetDir = 'test6'
test = os.listdir(targetDir)
# print(test)
# for i in test:
    # print(i)

# test2 = os.listdir(targetDir + '/' + test[0])

test2 = glob.glob(targetDir + '/**/output_*.tsv', recursive = True)
test3 = glob.glob(targetDir + '/**/config_*.ts', recursive = True)

for i in test2:
    print(i)

print('===============================')

for i in test3:
    print(i)














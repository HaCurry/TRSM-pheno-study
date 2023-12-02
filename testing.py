# -*- coding: utf-8 -*-
# import csv
# import pandas
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib as mpl
# import scipy.interpolate
# from scipy.interpolate import CubicSpline
# mpl.rcParams.update(mpl.rcParamsDefault)
# from numpy import ma
# from subprocess import call
# import subprocess

import functions as TRSM

# #lista = ['../TRSMBroken', 'regionTesting.tsv', '--config', 'TRSMBroken_regionTesting.ini', 'scan', '-n', '100']
# lista = ['../TRSMBroken', 'regionTesting.tsv', '--config', '12-412.ini', 'scan', '-n', '100']
# #test = subprocess.run(lista, stdout = subprocess.PIPE)
# test = subprocess.run(lista, capture_output = True)
# print('+-----------------------------------------------------------+')
# print('+-----------------------------------------------------------+')
# #print(test)
# print('+-----------------------------------------------------------+')
# print('+-----------------------------------------------------------+')
# test = test.stdout.decode('utf-8')
# print(test[-450:])

# test = (-0.1,0.1)
def test():
    TRSM.mixingMatrix(1.352, 1.175, -0.407, np.linspace(-np.pi/2, np.pi, 100), 'ths')
# plt.xlim(test)

test()
plt.show()
plt.close()
# plt.plot(np.linspace(-np.pi/2, np.pi, 100), np.linspace(-np.pi/2, np.pi, 100))
# plt.show()

#for i in test:
#    print(i)
##print(test.stdout)


#subprocess.run(toShell, timeout = 180)

#0.24757907662653156
#0.099353079531563693

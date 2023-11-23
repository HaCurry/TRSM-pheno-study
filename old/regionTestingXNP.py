# -*- coding: utf-8 -*-
import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.interpolate
from scipy.interpolate import CubicSpline
mpl.rcParams.update(mpl.rcParamsDefault)
from numpy import ma
from subprocess import call
import subprocess

import regionTestingFunctions.py as TRSM_rt

#### BP2 REGION 2

#pointlist = TRSM_rt.pointGen("BP2", 2, 5, "grid")

#dictPointlist = []

#for element in pointlist:
#    dictPointlist.append({ "ms": element[0], "mx": element[1] })

#TRSM_rt.regionTestingFunc("BP2", "XSH", dictPointlist, "vev", "plotting/XSH_region2_5x5", "BP2_XSHvev_region2", individualPlots = True)
#TRSM_rt.regionTestingFunc("BP2", "XSH", dictPointlist, "angle", "plotting/XSH_region2_5x5", "BP2_XSHangle_region2", individualPlots = True)



#### BP2 REGION 3

#pointlist = TRSM_rt.pointGen("BP2", 3, 5, "grid")

#dictPointlist = []

#for element in pointlist:
#    dictPointlist.append({ "ms": element[0], "mx": element[1] })

#TRSM_rt.regionTestingFunc("BP2", "XSS", dictPointlist, "vev", "plotting/XSS_region3_5x5", "BP2_XSSvev_region3", individualPlots = True)
#TRSM_rt.regionTestingFunc("BP2", "XSS", dictPointlist, "angle", "plotting/XSS_region3_5x5", "BP2_XSSangle_region3", individualPlots = True)


#TRSM_rt.regionTestingFunc("BP2", "XSH", [{"ms": 80, "mx": 350}, {"ms": 100, "mx": 300}], "angle", "temp", "check_angle", individualPlots = True)
#TRSM_rt.regionTestingFunc("BP2", "XSH", [{"ms": 80, "mx": 350}, {"ms": 100, "mx": 300}], "vev", "temp", "check_vev", individualPlots = True)



#### BP3 REGION 1

#pointlist = TRSM_rt.pointGen("BP3", 1, 5, "grid")

#dictPointlist = []

#for element in pointlist:
#    dictPointlist.append({ "ms": element[0], "mx": element[1] })

#TRSM_rt.regionTestingFunc("BP3", "XSH", dictPointlist, "vev",   "plotting/BP3_BR_XNP/BP3_XSH_region1_5x5", "BP3_XSHvev_region1",   individualPlots = True)
#TRSM_rt.regionTestingFunc("BP3", "XSH", dictPointlist, "angle", "plotting/BP3_BR_XNP/BP3_XSH_region1_5x5", "BP2_XSHangle_region1", individualPlots = True)



### BP3 REGION 2

pointlist = TRSM_rt.pointGen("BP3", 2, 8, "grid")

dictPointlist = []

for element in pointlist:
    dictPointlist.append({ "ms": element[0], "mx": element[1] })

TRSM_rt.regionTestingFunc("BP3", "XSH", dictPointlist, "vev",   "plotting/BP3_BR_XNP/BP3_XSH_region2_8x8", "BP3_XSHvev_region2",   individualPlots = True)
TRSM_rt.regionTestingFunc("BP3", "XSH", dictPointlist, "angle", "plotting/BP3_BR_XNP/BP3_XSH_region2_8x8", "BP2_XSHangle_region2", individualPlots = True)

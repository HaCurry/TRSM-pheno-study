# -*- coding: utf-8 -*-

import json
import argparse
import glob
import pandas
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
# import matplotlib
# import atlas_mpl_style as ampl
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
# laptop
# sys.path.insert(1, r"C:/Users/Iram Haque/My Drive/Master's thesis/TRSM Coding 13")
# pc
sys.path.insert(1, r"G:/My Drive/Master's thesis/TRSM Coding 13/")

from helpScannerS import functions as TRSM




def constrained_observed_lim(ms, mx, limit_obs, ms_lb = 1, ms_ub = 124, mx_lb = 126, mx_ub = 500, LessThanOrEqualTo = True):
    ms_BP2constrained = []
    mx_BP2constrained = []
    limit_obs_BP2constrained = []
    if LessThanOrEqualTo == True:
        for i in range(len(limit_obs)):
            # if (BP2_x_min < ms[i]) and  (ms[i] < BP2_x_max) and (BP2_y_min < mx[i]) and (mx[i] < BP2_y_max):
            # MAKE SURE TO PLOT THIS SO YOU HAVE YOUR DESIRED POINTS BECAUSE THE EQUALITY MIGHT INCLUDE SOME
            # UNDESIRED POINTS IF THE FLOAT VALUE IS VERY CLOSE TO HE BOUNDS. OTHERWISE SET LessThanOrEqualTo = False
            if (ms_lb <= ms[i]) and  (ms[i] <= ms_ub) and (mx_lb <= mx[i]) and (mx[i] <= mx_ub):
                ms_BP2constrained.append(ms[i])
                mx_BP2constrained.append(mx[i])
                limit_obs_BP2constrained.append(limit_obs[i])
            else:
                continue
        
        return np.array(ms_BP2constrained), np.array(mx_BP2constrained), np.array(limit_obs_BP2constrained)
    
    else:
        for i in range(len(limit_obs)):
            # if (BP2_x_min < ms[i]) and  (ms[i] < BP2_x_max) and (BP2_y_min < mx[i]) and (mx[i] < BP2_y_max):
            # MAKE SURE TO PLOT THIS SO YOU HAVE YOUR DESIRED POINTS BECAUSE THE EQUALITY MIGHT INCLUDE SOME
            # UNDESIRED POINTS IF THE FLOAT VALUE IS VERY CLOSE TO HE BOUNDS. OTHERWISE SET LessThanOrEqualTo = False
            if (ms_lb < ms[i]) and  (ms[i] < ms_ub) and (mx_lb < mx[i]) and (mx[i] < mx_ub):
                ms_BP2constrained.append(ms[i])
                mx_BP2constrained.append(mx[i])
                limit_obs_BP2constrained.append(limit_obs[i])
            else:
                continue
        
        return np.array(ms_BP2constrained), np.array(mx_BP2constrained), np.array(limit_obs_BP2constrained)
    
    

def remove_nan(ms, mx, limit_obs, removeNan = False):
    ''' If removeNan is set to False (default) outputs list elements where limit_obs
    is equal to np.nan, otherwise when set to True, outputs the same lists BUT
    with np.nan elements removed.'''
    
    
    if removeNan == False:

        nanned_ms = []
        nanned_mx = []
        nanned_limit_obs = []
        
        for i in range(len(limit_obs)):
            
            if np.isnan(limit_obs[i]):
                nanned_limit_obs.append(limit_obs[i])
                nanned_ms.append(ms[i])
                nanned_mx.append(mx[i])
        
        return nanned_ms, nanned_mx, nanned_limit_obs
    
    
    
    elif removeNan == True:
        
        nanned_index = []

        for i in range(len(limit_obs)):
            
            if np.isnan(limit_obs[i]):
                nanned_index.append(i)
            
            else:
                continue
        
        removed_nanned_ms = []
        removed_nanned_mx = []
        removed_nanned_limit_obs = []
        
        for i in range(len(limit_obs)):
            
            if i in nanned_index:
                continue
            
            else:
                removed_nanned_ms.append(ms[i])
                removed_nanned_mx.append(mx[i])
                removed_nanned_limit_obs.append(limit_obs[i])
        
        return removed_nanned_ms, removed_nanned_mx, removed_nanned_limit_obs
    
    
    
def smallval_remove(arr1,arr2,arr3,arr4, epsilon = 10**(-9), divide = True):
    ''' If divide == True, removes elements less than epsilon and divides arr3 and arr4
    otherwise does not divide arr3 and arr4 and instead returns lists with elements less
    than epsilon removed.'''
        
    x = []
    y = []
    z = []
    
    ## rough check if arrays are of equal length
    if abs( (len(arr1) + len(arr3) + len(arr4))/ (3 * len(arr1)) - 1 ) > 10**(-9):
        raise Exception('arrays not equal length')
    
    ## return arr1, arr2 and arr3/arr4 with small (epsilon) values in each array removed
    if divide == True:
    
        for i in range(len(arr1)):
            
            if (abs(arr3[i]) < epsilon) and (abs(arr4[i]) < epsilon):
                continue
            
            else:
                x.append(arr1[i])
                y.append(arr2[i])
                z.append( (arr3)[i]/(arr4)[i] )
                
        return x, y, z

    ## return arr1, arr2, arr3 and arr4 with small (epsilon) values in each array removed
    elif divide == False :
        
        z1 = []
        z2 = []
        
        for i in range(len(arr1)):
            
            if (abs(arr3[i]) < epsilon) and (abs(arr4[i]) < epsilon):
                continue
            
            else:
                x.append(arr1[i])
                y.append(arr2[i])
                z1.append( (arr3)[i] )
                z2.append( (arr4)[i] )
    
        return x, y, z1, z2
    
    else:
        raise Exception('divide set to invalid value')

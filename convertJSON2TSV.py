# -*- coding: utf-8 -*-
import json
import pandas
import numpy as np

limits = pandas.read_json('Atlas2023Limits.json')

mx, ms, limit_obs, limit_exp = [], [], [], []

for element in limits:
    mx.append((limits[element])[0])
    ms.append((limits[element])[1])
#    limit_exp.append((limits[element])[2] * 10 **(-3))
#    limit_obs.append((limits[element])[3] * 10 **(-3))
    # limit_exp.append((limits[element])[2] * 10 **(-3))
    # limit_obs.append((limits[element])[3] * 10 **(-3))
    limit_exp.append((limits[element])[2] )
    limit_obs.append((limits[element])[3] )

mx = np.array(mx)
ms = np.array(ms)
limit_exp = np.array(limit_exp)
limit_obs = np.array(limit_obs)

d = {'ms': ms, 'mx': mx, 'limit_obs': limit_obs, 'limit_exp': limit_exp}

df = pandas.DataFrame(data = d)

print(df)
print('===============')
print(df.dtypes)

df.to_csv('Atlas2023Limits.tsv', sep = "\t")


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
        
        return ms_BP2constrained, mx_BP2constrained, limit_obs_BP2constrained
    
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
        
        return ms_BP2constrained, mx_BP2constrained, limit_obs_BP2constrained

ms_BP2constrained, mx_BP2constrained, limit_obs_BP2constrained = constrained_observed_lim(ms, mx, limit_obs)

dBP2 = {'ms_BP2': ms_BP2constrained, 'mx_BP2': mx_BP2constrained, 'limit_obs_BP2': limit_obs_BP2constrained}

dfBP2 = pandas.DataFrame(data = dBP2)

print(dfBP2)
print('===================')
print(df.dtypes)

dfBP2.to_csv('Atlas2023Limits_BP2lessThanOrEqualTo.tsv', sep = "\t")


















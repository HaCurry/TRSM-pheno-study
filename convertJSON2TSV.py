# -*- coding: utf-8 -*-
import json
import pandas
import numpy as np

# !!IMPORTANT: ALL VALUES FROM Atlas2023Limits.json ARE IN FB SO ARE ALSO THE CONVERTED .tsv FILES!!



def constrained_observed_lim(ms, mx, limit_obs, ms_lb, ms_ub, mx_lb, mx_ub, LessThanOrEqualTo = True):

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



def convert(path, output, constraint, constraintLessThanOrEqualTo = True, **kwargs):

    # BP2 mass constraints ms_lb = 1, ms_ub = 124, mx_lb = 126, mx_ub = 500
    
    #################### kwargs ####################

    if constraint == True:

        if ('ms_lb' in kwargs) and ('ms_ub' in kwargs) and ('mx_lb' in kwargs) and ('mx_ub' in kwargs):
            ms_lb = kwargs['ms_lb']
            ms_ub = kwargs['ms_ub']
            mx_lb = kwargs['mx_lb']
            mx_ub = kwargs['mx_ub']

        else:
            raise Exception('constraint set to true but no constraint values ms_lb, ms_ub, mx_lb, mx_ub given \n or one value is missing.')

    else:
        constraint = False
                             
     ################################################

    
    limits = pandas.read_json(path)
    
    mx, ms, limit_obs, limit_exp = [], [], [], []
    
    for element in limits:
        mx.append((limits[element])[0])
        ms.append((limits[element])[1])
        limit_exp.append((limits[element])[2] )
        limit_obs.append((limits[element])[3] )
    
    mx = np.array(mx)
    ms = np.array(ms)
    limit_exp = np.array(limit_exp)
    limit_obs = np.array(limit_obs)

    if constraint == True:
        ms, mx, limit_obs = constrained_observed_lim(ms, mx, limit_obs, ms_lb, ms_ub, mx_lb, mx_ub, LessThanOrEqualTo = constraintLessThanOrEqualTo)

    else:
        pass
    
    
    d = {'ms': ms, 'mx': mx, 'limit_obs': limit_obs}
    
    df = pandas.DataFrame(data = d)

    df.to_csv(output, sep = "\t")

    return df
    
if __name__ == "__main__":

    # BP2 mass points in Atlas2023Limits
    dfBP2 = convert('Atlas2023Limits.json', 'Atlas2023Limits_BP2lessThanOrEqualToTrue.tsv', True, constraintLessThanOrEqualTo = True, ms_lb = 1, ms_ub = 124, mx_lb = 126, mx_ub = 500)

    # BP3 mass points in Atlas2023Limits
    dfBP3 = convert('Atlas2023Limits.json', 'Atlas2023Limits_BP3lessThanOrEqualToTrue.tsv', True, constraintLessThanOrEqualTo = True, ms_lb = 126, ms_ub = 500, mx_lb = 255, mx_ub = 650)
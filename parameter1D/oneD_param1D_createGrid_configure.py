import os

import numpy as np
import pandas

def createGrid(ms_lowerbound,
               ms_upperbound,
               mx_lowerbound, 
               mx_upperbound,
               ms_lowerbound_constrain, 
               ms_upperbound_constrain, 
               mx_lowerbound_constrain, 
               mx_upperbound_constrain,
               size,
               condition):
    
    mslist = np.linspace(ms_lowerbound, ms_upperbound, size)
    mxlist = np.linspace(mx_lowerbound, mx_upperbound, size)
    pointlist = []

    for i in range(size):
        for j in range(size):
            if condition(mslist[i], mxlist[j], ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain):
                pointlist.append([mslist[i], mxlist[j]])
            else:
                continue
    return np.array(pointlist)


def BP2conditionRegion1(ms, mx, ms_lb_con, ms_ub_con, mx_lb_con, mx_ub_con):
    if (5.3 * ms + 100.09 > mx) and (ms_ub_con > ms) and (ms > ms_lb_con) and (mx_ub_con > mx > mx_lb_con):
        return True
    else: 
        return False

def BP2conditionRegion2(ms, mx, ms_lb_con, ms_ub_con, mx_lb_con, mx_ub_con):
    if (5.2 * ms + 100.09 > mx) and (mx > ms + 140.09) and (ms_ub_con > ms) and (ms > ms_lb_con) and (mx_ub_con > mx > mx_lb_con) and (ms > 15):
        return True
    else: 
        return False

def BP3conditionRegion1(ms, mx, ms_lb_con, ms_ub_con, mx_lb_con, mx_ub_con):
    if (mx > 2 * ms + 20) and (3.27 * ms + 58 > mx) and (-0.34 * ms + 636 > mx) and (mx > 2 * ms) and (ms_ub_con > ms) and (ms > ms_lb_con) and (mx_ub_con > mx > mx_lb_con):
        return True
    else:
        return False

def BP3conditionRegion2(ms, mx, ms_lb_con, ms_ub_con, mx_lb_con, mx_ub_con):
    if (2 * ms - 20 > mx) and ((-0.72) * ms + 735 > mx) and (mx > ms + 145.09 ) and (ms_ub_con > ms) and (ms > ms_lb_con) and (mx_ub_con > mx > mx_lb_con):
        return True
    else:
        return False

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to the directory containing this script
    pathParam1D = os.path.join(pathRepo, 'parameter1D')

    # path to plots
    pathPlots = os.path.join(pathParam1D, 'plots')

    # path to the directory where the points for the grid are saved
    pathGrids = os.path.join(pathParam1D, 'grids')

    # path to ScannerS output
    path13_BP = os.path.join(pathRepo, 'Benchmarkplanes', 'BPs_noconstraints')

    # path to 13 TeV TRSM ScannerS cross sections with BP2 settings
    # (will only be used for plotting)
    path13_BP2 = os.path.join(path13_BP, 'BP2', 'output_BP2_noconstraints.tsv')

    # path to 13 TeV TRSM ScannerS cross sections with BP3 settings
    # (will only be used for plotting)
    path13_BP3 = os.path.join(path13_BP, 'BP3', 'output_BP3_noconstraints.tsv')

    ## create grid for BP2:
    
    ms_lowerbound, ms_upperbound = 1, 124
    mx_lowerbound, mx_upperbound = 126, 500

    # region 1
    ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition = 1, 120, 263, 485, BP2conditionRegion1
        
    BP2R1_pointlist = createGrid(ms_lowerbound,
                                 ms_upperbound,
                                 mx_lowerbound, 
                                 mx_upperbound,
                                 ms_lowerbound_constrain, 
                                 ms_upperbound_constrain, 
                                 mx_lowerbound_constrain, 
                                 mx_upperbound_constrain,
                                 25,
                                 condition)

    BP2R1 = {'mH1': [BP2R1_pointlist[i][0] for i in range(len(BP2R1_pointlist))],
             'mH2': [125.09 for i in range(len(BP2R1_pointlist))],
             'mH3': [BP2R1_pointlist[i][1] for i in range(len(BP2R1_pointlist))]}

    df_BP2R1 = pandas.DataFrame(BP2R1)
    df_BP2R1.to_csv(os.path.join(pathGrids, 'BP2_region1.tsv'))

    # region 2
    ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition = 1, 124, 126, 245, BP2conditionRegion2
        
    BP2R2_pointlist = createGrid(ms_lowerbound,
                                 ms_upperbound,
                                 mx_lowerbound, 
                                 mx_upperbound,
                                 ms_lowerbound_constrain, 
                                 ms_upperbound_constrain, 
                                 mx_lowerbound_constrain, 
                                 mx_upperbound_constrain,
                                 25,
                                 condition)

    BP2R2 = {'mH1': [BP2R2_pointlist[i][0] for i in range(len(BP2R2_pointlist))],
             'mH2': [125.09 for i in range(len(BP2R2_pointlist))],
             'mH3': [BP2R2_pointlist[i][1] for i in range(len(BP2R2_pointlist))]}

    df_BP2R2 = pandas.DataFrame(BP2R2)
    df_BP2R2.to_csv(os.path.join(pathGrids, 'BP2_region2.tsv'))


    ## create grid for BP3

    ms_lowerbound, ms_upperbound = 126, 500
    mx_lowerbound, mx_upperbound = 255, 650

    # region 1
    ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition = 126, 290, 255, 650, BP3conditionRegion1

    BP3R1_pointlist = createGrid(ms_lowerbound,
                                 ms_upperbound,
                                 mx_lowerbound, 
                                 mx_upperbound,
                                 ms_lowerbound_constrain, 
                                 ms_upperbound_constrain, 
                                 mx_lowerbound_constrain, 
                                 mx_upperbound_constrain,
                                 25,
                                 condition)

    BP3R1 = {'mH1': [125.09 for i in range(len(BP3R1_pointlist))],
             'mH2': [BP3R1_pointlist[i][0] for i in range(len(BP3R1_pointlist))],
             'mH3': [BP3R1_pointlist[i][1] for i in range(len(BP3R1_pointlist))]}

    df_BP3R1 = pandas.DataFrame(BP3R1)
    df_BP3R1.to_csv(os.path.join(pathGrids, 'BP3_region1.tsv'))

    # region 2
    ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition = 126, 380, 255, 600, BP3conditionRegion2

    BP3R2_pointlist = createGrid(ms_lowerbound,
                                 ms_upperbound,
                                 mx_lowerbound, 
                                 mx_upperbound,
                                 ms_lowerbound_constrain, 
                                 ms_upperbound_constrain, 
                                 mx_lowerbound_constrain, 
                                 mx_upperbound_constrain,
                                 25,
                                 condition)

    BP3R2 = {'mH1': [125.09 for i in range(len(BP3R2_pointlist))],
             'mH2': [BP3R2_pointlist[i][0] for i in range(len(BP3R2_pointlist))],
             'mH3': [BP3R2_pointlist[i][1] for i in range(len(BP3R2_pointlist))]}

    df_BP3R2 = pandas.DataFrame(BP3R2)
    df_BP3R2.to_csv(os.path.join(pathGrids, 'BP3_region2.tsv'))


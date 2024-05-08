import os
import json

import scipy
import numpy as np
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import mplhep as hep
from helpScannerS import functions as TRSM
from helpScannerS import twoDPlotter as twoDPlot

def pointGen(BP, region, size, generator):
    
    def random(ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition):
        ms = np.random.uniform(ms_lowerbound_constrain, ms_upperbound_constrain, 1)
        mx = np.random.uniform(mx_lowerbound_constrain, mx_upperbound_constrain, 1)
        if condition(ms, mx):
            point = [ms, mx]
            return point
        else:
            point = random(ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition)
            return point
    
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
    
    def BP2conditionRegion3(ms, mx, ms_lb_con, ms_ub_con, mx_lb_con, mx_ub_con):
        if (ms + 125.09 > mx) and (2 * ms < mx) and (ms_ub_con > ms) and (ms > ms_lb_con) and (mx_ub_con > mx > mx_lb_con):
            return True
        else: 
            return False
    # temp, 2*temp + 20, temp, 3.27*temp + 58, temp, -0.34*temp + 621
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

    def BP3conditionRegion3(ms, mx, ms_lb_con, ms_ub_con, mx_lb_con, mx_ub_con):
        if (ms + 125.09 > mx) and ((-1.29) * ms + 949 > mx) and (mx > ms) and (ms_ub_con > ms) and (ms > ms_lb_con) and (mx_ub_con > mx > mx_lb_con):
            return True
        else:
            return False

    pointlist = []
    
    if BP == 'BP2':

        ms_lowerbound, ms_upperbound = 1, 124
        mx_lowerbound, mx_upperbound = 126, 500
    
        if region == 1:
            ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition = 1, 120, 263, 485, BP2conditionRegion1
            
        elif region == 2:
            ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition = 1, 124, 126, 245, BP2conditionRegion2
            
        elif region == 3:
            ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition = 1, 124, 126, 250, BP2conditionRegion3

        else:
            raise Exception('No region chosen')
    
    elif BP == 'BP3':

        ms_lowerbound, ms_upperbound = 126, 500
        mx_lowerbound, mx_upperbound = 255, 650
        
        if region == 1:
            ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition = 126, 290, 255, 650, BP3conditionRegion1
        
        elif region == 2:
            ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition = 126, 380, 255, 600, BP3conditionRegion2
            
        elif region == 3:
            ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain, condition = 126, 500, 255, 550, BP3conditionRegion3
        
        else:
            raise Exception('No region chosen')
    
    else:
        raise Exception('No BP chosen')
    
    if generator == 'random':
        
        for i in range(size):
            point = random(ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition)
            pointlist.append(point)
        return np.array(pointlist)
    
    elif generator == 'grid':
        
        mslist = np.linspace(ms_lowerbound, ms_upperbound, size)
        mxlist = np.linspace(mx_lowerbound, mx_upperbound, size)
        
        for i in range(size):
            for j in range(size):
                if condition(mslist[i], mxlist[j], ms_lowerbound_constrain, ms_upperbound_constrain, mx_lowerbound_constrain, mx_upperbound_constrain):
                    pointlist.append([mslist[i], mxlist[j]])
                else:
                    continue
        return np.array(pointlist)
    
    else:
        raise Exception('No generator chosen')




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

    ## plotting style
    with open(os.path.join(pathRepo, 'MatplotlibStyles.json')) as json_file:
        styles = json.load(json_file)    

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})

    # change label fontsize
    mpl.rcParams['axes.labelsize'] = styles['axes.labelsize']
    mpl.rcParams['axes.titlesize'] = styles['axes.titlesize']

    # change ticksize
    mpl.rcParams['xtick.minor.size'] = styles['xtick.minor.size']
    mpl.rcParams['xtick.major.size'] = styles['xtick.major.size']
    mpl.rcParams['ytick.minor.size'] = styles['ytick.minor.size']
    mpl.rcParams['ytick.major.size'] = styles['ytick.major.size']

    # change legend font size and padding
    mpl.rcParams['legend.borderpad'] = styles['legend.borderpad']
    mpl.rcParams['legend.fontsize'] = styles['legend.fontsize']
    mpl.rcParams['legend.title_fontsize'] = styles['legend.title_fontsize']
    mpl.rcParams['legend.frameon'] = styles['legend.frameon']
    mpl.rcParams['legend.fancybox'] = styles['legend.fancybox']
    mpl.rcParams['legend.edgecolor'] = styles['legend.edgecolor']
    mpl.rcParams['legend.edgecolor'] = styles['legend.edgecolor']

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

    
    ## plot the grids

    # BP2

    ScannerS_BP2 = TRSM.observables(path13_BP2, 
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    'valid_BFB', 'valid_Higgs', 'valid_STU', 'valid_Uni',
                                    kineticExclude=True)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP2['mH1'],
                                            ScannerS_BP2['mH3'],
                                            ScannerS_BP2['x_H3_H1_bb_H2_gamgam'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots(figsize=(6.75,6))

    # plot the BP2 region
    contf = ax.contourf(xi, yi, zi, 0, colors=['C0'])

    # the line M3 = M1 + M2
    ax.plot([1, 124], [1 + 125.09, 124 + 125.09],
            ls='dashed', color='k', linewidth=2)

    # the line M3 = 2M2
    ax.plot([1, 124], [250, 250],
            ls='dashdot', color='k', linewidth=2)

    # plot the constrained regions
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP2, 'mH1', 'mH3', f'valid_{key}',
                                            ax, constraints[key])

    # plot the grid regions
    ax.scatter(np.array(df_BP2R1['mH1']), np.array(df_BP2R1['mH3']), facecolor='C1', marker='x')
    ax.scatter(np.array(df_BP2R2['mH1']), np.array(df_BP2R2['mH3']), facecolor='C2', marker='x')

    # labels and x and ylims
    twoDPlot.plotAuxTitleAndBounds2D('',
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]',
                                     '',
                                     cbarvisible=False,
                                     xlims=(-3, 127), ylims=(110, 510))

    ax.legend(title='BP2:',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mlines.Line2D([], [], linestyle='none', marker='x', color='C1', label='Region 1'),
              mlines.Line2D([], [], linestyle='none', marker='x', color='C2', label='Region 2'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$'),
              mlines.Line2D([], [], linestyle='dashdot', color='black', label='$M_{3}=2\cdot M_{2}$')
              ], loc='lower right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP2gridPlot.pdf'))

    
    # BP3

    ScannerS_BP3 = TRSM.observables(path13_BP3, 
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    'valid_BFB', 'valid_Higgs', 'valid_STU', 'valid_Uni',
                                    kineticExclude=True)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(ScannerS_BP3['mH2'],
                                            ScannerS_BP3['mH3'],
                                            ScannerS_BP3['x_H3_H1_bb_H2_gamgam'])
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    fig, ax = plt.subplots(figsize=(6.75,6))

    # plot the BP3 region
    contf = ax.contourf(xi, yi, zi, 0, colors=['C0'])

    # the line M3 = M1 + M2
    ax.plot([126, 500], [126 + 125.09, 500 + 125.09],
            ls='dashed', color='k', linewidth=2)
    ax.plot([126, 500], [2 * 126, 2 * 500],
            ls='dashdot', color='k', linewidth=2)

    # plot the constrained regions
    constraints = {'BFB': '+++', 'Higgs': r'////', 'STU': r'\\\\ ', 'Uni': '...'}
    legendIconsAndLabels = []
    for key in constraints:
        contf = twoDPlot.plotAuxConstraints(ScannerS_BP3, 'mH2', 'mH3', f'valid_{key}',
                                            ax, constraints[key])

    twoDPlot.plotAuxTitleAndBounds2D(r'',
                                     r'$M_{2}$ [GeV]', r'$M_{3}$ [GeV]',
                                     r'',
                                     cbarvisible=False,
                                     xlims=(115, 510), ylims=(245, 660))
                                     
    # plot the grid regions
    ax.scatter(np.array(df_BP3R1['mH2']), np.array(df_BP3R1['mH3']), facecolor='C1', marker='x')
    ax.scatter(np.array(df_BP3R2['mH2']), np.array(df_BP3R2['mH3']), facecolor='C2', marker='x')

    ax.legend(title='BP3:',
              handles=[
              mpatches.Patch(linewidth=0, fill=None, hatch='++', label='Boundedness'),
              mpatches.Patch(linewidth=0, fill=None, hatch='//', label='HiggsBounds'),
              mpatches.Patch(linewidth=0, fill=None, hatch='..', label='Unitarity'),
              mlines.Line2D([], [], linestyle='none', marker='x', color='C1', label='Region 1'),
              mlines.Line2D([], [], linestyle='none', marker='x', color='C2', label='Region 2'),
              mlines.Line2D([], [], linestyle='dashed', color='black', label='$M_{3}=M_{1}+M_{2}$'),
              mlines.Line2D([], [], linestyle='dashdot', color='black', label='$M_{3}=2\cdot M_{2}$'),
              ], loc='lower right', alignment='left')

    ax.set_xlim(115, 510)
    ax.set_ylim(245, 660)

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, 'BP3gridPlot.pdf'))


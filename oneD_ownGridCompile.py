# -*- coding: utf-8 -*-
import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib as mpl
import scipy
# from scipy.interpolate import CubicSpline
# mpl.rcParams.update(mpl.rcParamsDefault)
# from numpy import ma
# from subprocess import call
# import subprocess

import functions as TRSM
import twoDPlotter as twoDPlot

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


def plotmarkerAuto(markers, manualmarkers, visible, decimals, fsize):#, x, y, n):
    for i in range(len(markers)):
        # pointS, pointX, br = pointfinder(5, (markers[i])[0], (markers[i])[1], x, y, n)
        plt.text((markers[i])[0], (markers[i])[1], r'%s'%str(round(1,decimals)), fontsize = fsize)
        if visible == True:
            plt.plot((markers[i])[0], (markers[i])[1], marker = 'o', mfc = 'none', color = 'r')


def msmxToTable(points, path):
    ms, mx  = [], []
    for i in range(len(points)):
        ms.append((points[i])[0])
        mx.append((points[i])[1])

    dictToTable = {}
    dictToTable['ms'] = ms
    dictToTable['mx'] = mx

    df = pandas.DataFrame(data = dictToTable)
    df.to_csv(path, sep = "\t")
    return df
    

if __name__ == '__main__':

   #  norm = 1
 
   #  ## BP2: ##

   #  BP2_mH1, BP2_mH2, BP2_mH3, BP2_x_H3_SM1SM2 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/calc_BP2.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    
   #  x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_x_H3_SM1SM2/norm)

   #  zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

   #  plt.imshow(zi, origin='lower',
   #              extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

   #  points_BP2_region1 = pointGen('BP2', 1, 25, 'grid')
   #  print(len(points_BP2_region1))
   #  # plotmarkerAuto(points_BP2_region1, [], True, 1, 8)#, x, y, n):

   #  df = msmxToTable(points_BP2_region1, 'ownGridRegion1BP2.tsv')

   #  plt.scatter(df['ms'], df['mx'], marker='o', facecolors='none', edgecolor = 'C1')
    
   #  twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\sigma(X\to S(b\bar{b})H(\gamma\gamma))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

   #  twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
   #                  ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))

   #  plt.savefig('BP2tb1.pdf')
   #  # plt.show()
   #  plt.close()

   #  del x, y, z, xi, yi, points_BP2_region1, df


   # ## BP2: ##

   #  # twoDPlot.calculateSort2D('plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 'plots2D/BP2_BR_XSH', 'calc_BP2', 'bb', 'gamgam')

   #  BP2_mH1, BP2_mH2, BP2_mH3, BP2_x_H3_SM1SM2 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/calc_BP2.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    
   #  x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_x_H3_SM1SM2/norm)

   #  zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

   #  plt.imshow(zi, origin='lower',
   #              extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

   #  points_BP2_region2 = pointGen('BP2', 2, 25, 'grid')
   #  print(len(points_BP2_region2))
   #  # plotmarkerAuto(points_BP2_region2, [], True, 2, 8)#, x, y, n):

   #  df = msmxToTable(points_BP2_region2, 'ownGridRegion2BP2.tsv')

   #  plt.scatter(df['ms'], df['mx'])
    
   #  twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\sigma(X\to S(b\bar{b})H(\gamma\gamma))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

   #  twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
   #                  ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))

   #  plt.savefig('BP2tb2.pdf')
   #  # plt.show()
   #  plt.close()

   #  del x, y, z, xi, yi, points_BP2_region2, df


   #  ## BP3: ##

   #  BP3_mH1, BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/calc_BP3.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')
      
   #  x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM1_H2_SM2/norm)

   #  zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


   #  plt.imshow(zi, origin='lower',
   #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

   #  points_BP3_region1 = pointGen('BP3', 1, 25, 'grid')
   #  print(len(points_BP3_region1))
   #  # plotmarkerAuto(points_BP3_region1, [], True, 2, 8)#, x, y, n):

   #  df = msmxToTable(points_BP3_region1, 'ownGridRegion1BP3.tsv')

   #  plt.scatter(df['ms'], df['mx'])
    
   #  twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\sigma(X\to S(b\bar{b})H(\gamma\gamma))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(126, 500), ylims=(255, 650))

   #  twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{S}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = M_{S}$', (298, 575), (337, 445), (353, 336),
   #                  ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
   
   #  plt.savefig('BP3tb1.pdf')
   #  # plt.show()
   #  plt.close()

   #  del x, y, z, xi, yi, points_BP3_region1, df


   #  ## BP3: ##

   #  BP3_mH1, BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/calc_BP3.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')
      
   #  x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM1_H2_SM2/norm)

   #  zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


   #  plt.imshow(zi, origin='lower',
   #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

   #  points_BP3_region2 = pointGen('BP3', 2, 25, 'grid')
   #  print(len(points_BP3_region2))
   #  # plotmarkerAuto(points_BP3_region2, [], True, 2, 8)#, x, y, n):

   #  df = msmxToTable(points_BP3_region2, 'ownGridRegion2BP3.tsv')

   #  plt.scatter(df['ms'], df['mx'])
    
   #  twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\sigma(X\to S(b\bar{b})H(\gamma\gamma))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(126, 500), ylims=(255, 650))

   #  twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{S}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = M_{S}$', (298, 575), (337, 445), (353, 336),
   #                  ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
   
   #  plt.savefig('BP3tb2.pdf')
   #  # plt.show()
   #  plt.close()

   #  del x, y, z, xi, yi, points_BP3_region2, df


    # norm = 1
    norm = (31.02 * 10**(-3)) * 0.0026
 
    ## BP2: ##

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_x_H3_SM1SM2 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/calc_BP2.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_x_H3_SM1SM2/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    ## Region 1 ##
    
    points_BP2_region1 = pointGen('BP2', 1, 25, 'grid')
    print(len(points_BP2_region1))
    # plotmarkerAuto(points_BP2_region1, [], True, 1, 8)#, x, y, n):

    df1 = msmxToTable(points_BP2_region1, 'ownGridRegion1BP2.tsv')

    plt.plot(df1['ms'], df1['mx'], ls='none', marker='o', mfc='none', color = 'black', alpha=0.7, label='Region 1')

    ## Region 2 ##
    
    points_BP2_region2 = pointGen('BP2', 2, 25, 'grid')
    print(len(points_BP2_region2))
    # plotmarkerAuto(points_BP2_region2, [], True, 2, 8)#, x, y, n):

    df2 = msmxToTable(points_BP2_region2, 'ownGridRegion2BP2.tsv')

    plt.plot(df2['ms'], df2['mx'], ls='none', marker='o', mfc='none', color = 'white', alpha=0.7, label='Region 2')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP2 grid: $\sigma_{gg \ \to \ h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma)} \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r'$\sigma_{gg \ \to \ h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma)} \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$', xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = 2 M_{2}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))

    plt.legend(facecolor='grey', loc='upper left')
    plt.tight_layout()
    plt.savefig('plots2D/BP2_BR_XSH/BP2ownGrid.pdf')
    # plt.show()
    plt.close()

    del x, y, z, xi, yi, points_BP2_region1, df1, df2


    ## BP3: ##

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/calc_BP3.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')
      
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM1_H2_SM2/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    plt.imshow(zi, origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    ## Region 1
    
    points_BP3_region1 = pointGen('BP3', 1, 25, 'grid')
    print(len(points_BP3_region1))
    # plotmarkerAuto(points_BP3_region1, [], True, 2, 8)#, x, y, n):

    df1 = msmxToTable(points_BP3_region1, 'ownGridRegion1BP3.tsv')

    plt.plot(df1['ms'], df1['mx'], ls='none', marker='o', mfc='none', color = 'black', alpha=0.7, label='Region 1')

    ## Region 2

    points_BP3_region2 = pointGen('BP3', 2, 25, 'grid')
    print(len(points_BP3_region2))
    # plotmarkerAuto(points_BP3_region2, [], True, 2, 8)#, x, y, n):

    df2 = msmxToTable(points_BP3_region2, 'ownGridRegion2BP3.tsv')

    plt.plot(df2['ms'], df2['mx'], ls='none', marker='o', mfc='none', color = 'white', alpha=0.7, label='Region2')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP3 grid: $\sigma_{gg \ \to \ h_{3} \ \to \ h_{1}(\gamma\gamma) \ h_{2}(b\bar{b})} \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$", r"$M_{2}$", r"$M_{3}$", r'$\sigma_{gg \ \to \ h_{3} \ \to \ h_{1}(\gamma\gamma) \ h_{2}(b\bar{b})} \ / \ \sigma_{gg \ \to \ h_{\mathrm{SM}} \ \to \ b\bar{b}\gamma\gamma }$', xlims=(126, 500), ylims=(255, 650))

    twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = M_{2}$', (298, 575), (337, 445), (353, 336),
                    ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))

    plt.legend(facecolor='grey', loc='lower right')
    plt.tight_layout()
    plt.savefig('plots2D/BP3_BR_XSH/BP3ownGrid.pdf')
    # plt.show()
    plt.close()

    del x, y, z, xi, yi, points_BP3_region1, df1, df2


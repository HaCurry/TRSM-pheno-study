import pandas
import numpy as np
import os
import re

import matplotlib
import matplotlib.patheffects
import matplotlib.pyplot as plt
import mplhep as hep

if __name__ == '__main__':

    ## paths
    # paths with the comment '#E:' requires the user to insert the path

    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to txt file containing dataIds
    # this file will be generated when twoD_mgConfigureCompareScannerS.py is executed
    pathTxtFileWithDataIds = os.path.join(pathRepo,
                               'testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_compareScannerS/dataIds.txt')

    # path to Atlas limits within BP2 and BP3 mass ranges
    pathAtlasBPpoints = os.path.join(pathRepo, 'testing', 'MadGraph_ResonVsNonReson', 'AtlasLimitsMax_AtlasNotation.tsv')

    # path containing the dataId directories (the mass points where each mass point directory 
    # contains a Madgraph Executable, see twoD_mgConfigure.py or 
    # twoD_mgConfigureCompareScannerS.py for more information)
    # E:
    pathDataIdParent = '/eos/user/i/ihaque/MadgraphResonVsNonReson/MadgraphResonVsNonReson'
    
    # path to where the figures will be saved
    pathSavefig = os.path.join(pathDataIdParent, 'plots')
    
    # create the directory pathSavefig if it already does not exist
    os.makedirs(pathSavefig, exist_ok=True)

    # read the Atlas limits
    limitsUntransposed = pandas.read_json(os.path.join(pathRepo, 'Atlas2023Limits.json'))
    print(limitsUntransposed)
    # transpose the dataframe
    limits = limitsUntransposed.T
    print(limits)

    ms = [element for element in limits['S']]
    mx = [element for element in limits['X']]

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    matplotlib.rcParams['axes.labelsize'] = 19
    matplotlib.rcParams['axes.titlesize'] = 19

    with open(pathTxtFileWithDataIds) as file:
        dataIds = [line.strip() for line in file]

    remasses = re.compile('\d+')

    # Atlas limit points where ScannerS constraints are applied
    df = pandas.read_table(pathAtlasBPpoints)


    ## compare ScannerS calculations and Madgraph

    # runName (see twoD_mgConfigureCompareScannerS.py or twoD_mgConfigure.py 
    # for more information)
    runName = 'compareScannerS'

    compareScannerS = {
    'ms': [],
    'mx': [],
    'crossSecScannerS': [],
    'crossSecMadgraph': []
    }

    for dataId in dataIds:
        
        ## read in ScannerS calculations
        pathScannerSCrossSection = os.path.join(pathDataIdParent, 
                                                dataId,
                                                'compareScannerS',
                                                f'calculation_{dataId}_{runName}_ScannerSExecutable.tsv')
        dfScannerS = pandas.read_table(pathScannerSCrossSection)

        compareScannerS['crossSecScannerS'].append(dfScannerS['gg_H3_H1H2'][0])

        ## read in Madgraph calculations
        pathMadgraphCrossSection = os.path.join(pathDataIdParent, 
                                                dataId,
                                                'compareScannerS',
                                                f'output_{dataId}_{runName}_MadgraphExecutable.tsv')
        dfMadgraph = pandas.read_table(pathMadgraphCrossSection)
        
        compareScannerS['crossSecMadgraph'].append(dfMadgraph['pp_iota0_eta0h'][0])

        # check Madgraph and ScannerS have the same model parameters as a sanity check
        if (abs(dfMadgraph['mH1'][0] - dfScannerS['mH1'][0]) < 10**(-10) and 
            abs(dfMadgraph['mH2'][0] - dfScannerS['mH2'][0]) < 10**(-10) and
            abs(dfMadgraph['mH3'][0] - dfScannerS['mH3'][0]) < 10**(-10) and
            abs(dfMadgraph['thetahS'][0] - dfScannerS['thetahS'][0]) < 10**(-10) and
            abs(dfMadgraph['thetahX'][0] - dfScannerS['thetahX'][0]) < 10**(-10) and
            abs(dfMadgraph['thetaSX'][0] - dfScannerS['thetaSX'][0]) < 10**(-10) and
            abs(dfMadgraph['vs'][0] - dfScannerS['vs'][0]) < 10**(-10) and
            abs(dfMadgraph['vx'][0] - dfScannerS['vx'][0]) < 10**(-10)):
            pass

        else: 
            print(
                  abs(dfMadgraph['mH1'][0] - dfScannerS['mH1'][0]),
                  abs(dfMadgraph['mH2'][0] - dfScannerS['mH2'][0]),
                  abs(dfMadgraph['mH3'][0] - dfScannerS['mH3'][0]),
                  abs(dfMadgraph['thetahS'][0] - dfScannerS['thetahS'][0]),
                  abs(dfMadgraph['thetahX'][0] - dfScannerS['thetahX'][0]),
                  abs(dfMadgraph['thetaSX'][0] - dfScannerS['thetaSX'][0]),
                  abs(dfMadgraph['vs'][0] - dfScannerS['vs'][0]),
                  abs(dfMadgraph['vx'][0] - dfScannerS['vx'][0]),
                   )


            raise Exception('Something went wrong, model parameters of madgraph and scannerS not same')

        ## save ms and mx
        if abs(dfScannerS['mH2'][0] - 125.09) < 10**(-6):
            ms = dfScannerS['mH1'][0]
            mx = dfScannerS['mH3'][0]

        
        elif abs(dfScannerS['mH1'][0] - 125.09) < 10**(-6):
            ms = dfScannerS['mH2'][0]
            mx = dfScannerS['mH3'][0]

        compareScannerS['ms'].append(ms)
        compareScannerS['mx'].append(mx)


    ## plot the points which will be investigated with Madgraph and compared with ScannerS

    # low mass
    # all Atlas limit points
    plt.scatter(np.array(limits['S']), np.array(limits['X'])) 
    # Atlas limit points where ScannerS constraints are applied
    plt.scatter(np.array(df['ms']), np.array(df['mx']), facecolors='C1') 
    # Atlas limit  points we are interested in calculating cross sections with
    # Madgraph and comparing with ScannerS
    plt.scatter(compareScannerS['ms'], compareScannerS['mx'],
                facecolors='none', edgecolors='red', s=200) 
    plt.axvline(125)
    plt.xlim(0, 270)
    plt.ylim(160, 420)
    plt.savefig(os.path.join(pathSavefig, 'mgLowMass.pdf'))
    plt.close()

    # medium mass
    plt.scatter(np.array(limits['S']), np.array(limits['X']))
    plt.scatter(np.array(df['ms']), np.array(df['mx']), facecolors='C1')
    plt.scatter(compareScannerS['ms'], compareScannerS['mx'],
                facecolors='none', edgecolors='red', s=200)
    plt.axvline(125)
    plt.xlim(0, 525)
    plt.ylim(420, 620)
    plt.savefig(os.path.join(pathSavefig, 'mgMediumMass.pdf'))
    plt.close()

    # high mass
    plt.scatter(np.array(limits['S']), np.array(limits['X']))
    plt.scatter(np.array(df['ms']), np.array(df['mx']), facecolors='C1')
    plt.scatter(compareScannerS['ms'], compareScannerS['mx'],
                facecolors='none', edgecolors='red', s=200)
    plt.axvline(125)
    plt.xlim(0, 525)
    plt.ylim(620, 1020)
    plt.savefig(os.path.join(pathSavefig, 'mgHighMass.pdf'))
    plt.close()

    
    ### plot the cross sections
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.supxlabel(r'$M_{S}$')
    fig.supylabel(r'$M_{X}$')

    ## BP2
    
    # Madgraph
    axes[0][0].scatter(np.array(df['ms']), np.array(df['mx']),
                       facecolors='none', edgecolor='grey', linestyle='dashed', s=10)
    axes[0][0].scatter(np.array(compareScannerS['ms']), np.array(compareScannerS['mx']), 
                    c=np.array(compareScannerS['crossSecMadgraph']),
                    facecolors='C1')

    for i in range(len(compareScannerS['crossSecMadgraph'])):
        annotation = (compareScannerS['crossSecMadgraph'])[i]
        axes[0][0].annotate(f'{annotation:.3f}',
                            (compareScannerS['ms'][i], compareScannerS['mx'][i]),
                            textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45)

    axes[0][0].set_xlim(1, 124)
    axes[0][0].set_ylim(126, 500)
    axes[0][0].set_title('BP2 Madgraph')
    
    # ScannerS
    axes[0][1].scatter(np.array(df['ms']), np.array(df['mx']),
                       facecolors='none', edgecolor='grey', linestyle='dashed', s=10)
    
    axes[0][1].scatter(compareScannerS['ms'], compareScannerS['mx'], 
                    c=np.array(compareScannerS['crossSecScannerS']), 
                    facecolors='C1')

    for i in range(len(compareScannerS['crossSecScannerS'])):
        annotation = compareScannerS['crossSecScannerS'][i]
        axes[0][1].annotate(f'{annotation:.3f}',
                            (compareScannerS['ms'][i], compareScannerS['mx'][i]),
                            textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45)
    
    axes[0][1].set_xlim(1, 124)
    axes[0][1].set_ylim(126, 500)
    axes[0][1].set_title('BP2 ScannerS')


    ## BP3
    
    # Madraph
    axes[1][0].scatter(np.array(df['ms']), np.array(df['mx']),
                       facecolors='none', edgecolor='grey', linestyle='dashed', s=10)
    axes[1][0].scatter(compareScannerS['ms'], compareScannerS['mx'], 
                    c=np.array(compareScannerS['crossSecMadgraph']),
                    facecolors='C1')

    for i in range(len(compareScannerS['crossSecMadgraph'])):
        annotation = compareScannerS['crossSecMadgraph'][i]
        axes[1][0].annotate(f'{annotation:.3f}',
                            (compareScannerS['ms'][i], compareScannerS['mx'][i]),
                            textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45)
    
    axes[1][0].set_xlim(126, 500)
    axes[1][0].set_ylim(255, 650)
    axes[1][0].set_title('BP3 Madgraph')
    
    # ScannerS
    axes[1][1].scatter(np.array(df['ms']), np.array(df['mx']),
                       facecolors='none', edgecolor='grey', linestyle='dashed', s=10)
    axes[1][1].scatter(compareScannerS['ms'], compareScannerS['mx'], 
                    c=np.array(compareScannerS['crossSecScannerS']),
                    facecolors='C1')

    for i in range(len(compareScannerS['crossSecScannerS'])):
        annotation = compareScannerS['crossSecScannerS'][i]
        axes[1][1].annotate(f'{annotation:.3f}',
                            (compareScannerS['ms'][i], compareScannerS['mx'][i]),
                            textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45)

    axes[1][1].set_xlim(126, 500)
    axes[1][1].set_ylim(255, 650)
    axes[1][1].set_title('BP3 ScannerS')
    
    plt.savefig(os.path.join(pathSavefig, 'MadgraphVsScannerS_CrossSec_BPs.pdf'))
    plt.close()


    ### plot the ratio of Madgraph and ScannerS cross sections
    fig, axes = plt.subplots(nrows=1, ncols=2)

    ## BP2
    axes[0].scatter(compareScannerS['ms'], compareScannerS['mx'], 
                    c=np.array(compareScannerS['crossSecMadgraph'])/np.array(compareScannerS['crossSecScannerS']),
                    facecolors='C1')

    for i in range(len(compareScannerS['crossSecScannerS'])):
        annotation = compareScannerS['crossSecMadgraph'][i]/compareScannerS['crossSecScannerS'][i]
        axes[0].annotate(f'{annotation:.3f}',
                            (compareScannerS['ms'][i], compareScannerS['mx'][i]),
                            textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45)

    axes[0].set_xlim(1, 124)
    axes[0].set_ylim(126, 500)
    axes[0].set_title('BP2 Madgraph/ScannerS')
    axes[0].set_xlabel(r'$M_{S}$')
    axes[0].set_ylabel(r'$M_{X}$')
    

    ## BP3
    axes[1].scatter(compareScannerS['ms'], compareScannerS['mx'], 
                    c=np.array(compareScannerS['crossSecMadgraph'])/np.array(compareScannerS['crossSecScannerS']),
                    facecolors='C1')

    for i in range(len(compareScannerS['crossSecScannerS'])):
        annotation = compareScannerS['crossSecMadgraph'][i]/compareScannerS['crossSecScannerS'][i]
        axes[1].annotate(f'{annotation:.3f}',
                            (compareScannerS['ms'][i], compareScannerS['mx'][i]),
                            textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45)

    axes[1].set_xlim(126, 500)
    axes[1].set_ylim(255, 650)
    axes[1].set_title('BP3 Madgraph/ScannerS')
    axes[1].set_xlabel(r'$M_{S}$')
    axes[1].set_ylabel(r'$M_{X}$')
    
    plt.savefig(os.path.join(pathSavefig, 'MadgraphVsScannerS_CrossSecRatio_BPs.pdf'))
    plt.close()
    

import pandas
import numpy as np
import os
import re
import json

import matplotlib as mpl
import matplotlib.patheffects as pe
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

    # read the Atlas limits
    limitsUntransposed = pandas.read_json(os.path.join(pathRepo, 'Atlas2023Limits.json'))
    print(limitsUntransposed)
    # transpose the dataframe
    limits = limitsUntransposed.T
    print(limits)

    ms = [element for element in limits['S']]
    mx = [element for element in limits['X']]

    with open(pathTxtFileWithDataIds) as file:
        dataIds = [line.strip() for line in file]

    remasses = re.compile('\d+')

    # Atlas limit points where ScannerS constraints are applied
    df = pandas.read_table(pathAtlasBPpoints)

    # Find the Atlas limit points within BP2 and BP3 mass ranges
    AtlasBP2pointsMs = [df['ms'][i] for i in range(len(df)) if (
        1 <= df['ms'][i] and
        df['ms'][i] <= 124 and
        126 <= df['mx'][i] and
        df['mx'][i] < 500
    )
    ]
    
    AtlasBP2pointsMx = [df['mx'][i] for i in range(len(df)) if (
        1 <= df['ms'][i] and
        df['ms'][i] <= 124 and
        126 <= df['mx'][i] and
        df['mx'][i] < 500
    )
    ]

    AtlasBP3pointsMs = [df['ms'][i] for i in range(len(df)) if ( 
        126 <= df['ms'][i] and
        df['ms'][i] <= 500 and
        255 <= df['mx'][i] and
        df['mx'][i] <= 650 
    )
    ]
    
    AtlasBP3pointsMx = [df['mx'][i] for i in range(len(df)) if (
        126 <= df['ms'][i] and
        df['ms'][i] <= 500 and
        255 <= df['mx'][i] and
        df['mx'][i] <= 650 
    )
    ]

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

    ## BP2
    fig, ax = plt.subplots()

    ax.scatter(AtlasBP2pointsMs, AtlasBP2pointsMx,
               facecolors='none', edgecolor='grey', linestyle='dashed',
               label='Atlas limits')

    scatter = ax.scatter(compareScannerS['ms'], compareScannerS['mx'], 
                    c=np.array(compareScannerS['crossSecMadgraph'])/np.array(compareScannerS['crossSecScannerS']),
                    facecolors='C1')

    for i in range(len(compareScannerS['crossSecScannerS'])):
        annotation = compareScannerS['crossSecMadgraph'][i]/compareScannerS['crossSecScannerS'][i]
        ax.annotate(f'{annotation:.3f}',
                            (compareScannerS['ms'][i], compareScannerS['mx'][i]),
                            textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45,
                    path_effects=[pe.withStroke(linewidth=2, foreground="white")])

    ax.set_xlim(1, 124)
    ax.set_ylim(126, 500)
    ax.set_xlabel(r'$M_{1}$ [GeV]')
    ax.set_ylabel(r'$M_{3}$ [GeV]')
    ax.legend(title='BP2 $\sqrt{s}=13$ TeV:\n$h_{1}=S$, $h_{2}=H$, $h_{3}=X$',
              alignment='left')
    
    fig.colorbar(scatter, ax=ax, label=r'$\sigma_{MG5}(gg \to h_{3}  \to h _{1} h _{2}) \ / \ \sigma_{SnS}(gg \to h _{3} \to h _{1}h _{2})$')

    plt.savefig(os.path.join(pathSavefig, 'MadgraphVsScannerS_CrossSecRatio_BP2.pdf'))
    plt.close()

    ## BP3
    fig, ax = plt.subplots()

    ax.scatter(AtlasBP3pointsMs, AtlasBP3pointsMx,
               facecolors='none', edgecolor='grey', linestyle='dashed',
               label='Atlas limits')

    scatter = ax.scatter(compareScannerS['ms'], compareScannerS['mx'], 
                    c=np.array(compareScannerS['crossSecMadgraph'])/np.array(compareScannerS['crossSecScannerS']),
                    facecolors='C1')

    for i in range(len(compareScannerS['crossSecScannerS'])):
        annotation = compareScannerS['crossSecMadgraph'][i]/compareScannerS['crossSecScannerS'][i]
        ax.annotate(f'{annotation:.3f}',
                            (compareScannerS['ms'][i], compareScannerS['mx'][i]),
                            textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45,
                    path_effects=[pe.withStroke(linewidth=2, foreground="white")])

    ax.set_xlim(126, 500)
    ax.set_ylim(255, 650)
    ax.set_xlabel(r'$M_{2}$ [GeV]')
    ax.set_ylabel(r'$M_{3}$ [GeV]')
    ax.legend(title='BP3 $\sqrt{s}=13$ TeV:\n$h_{1}=H$, $h_{2}=S$, $h_{3}=X$',
              alignment='left', loc='lower right')

    fig.colorbar(scatter, ax=ax, label=r'$\sigma_{MG5}(gg \to h_{3}  \to h _{1} h _{2}) \ / \ \sigma_{SnS}(gg \to h _{3} \to h _{1}h _{2})$')
    
    plt.savefig(os.path.join(pathSavefig, 'MadgraphVsScannerS_CrossSecRatio_BP3.pdf'))
    plt.close()
    

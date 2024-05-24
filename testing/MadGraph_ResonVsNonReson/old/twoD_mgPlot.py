import os
import json

import pandas
import numpy as np
import matplotlib as mpl
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import mplhep as hep

if __name__ == '__main__':

    ## paths
    # paths with the comment '#E:' requires the user to insert the path

    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # runName (see twoD_mgConfigureCompareScannerS.py or twoD_mgConfigure.py 
    # for more information)
    runName = 'nevents10000_triangleVsFull'

    # path to txt file containing dataIds
    # this file will be generated when twoD_mgConfigureCompareScannerS.py is executed
    pathTxtFileWithDataIds = os.path.join(pathRepo,
                               f'testing/MadGraph_ResonVsNonReson/MadgraphResonVsNonResonCondor/MadgraphResonVsNonReson_{runName}/dataIds.txt')

    # path to Atlas limits within BP2 and BP3 mass ranges
    pathAtlasBPpoints = os.path.join(pathRepo, 'testing', 'MadGraph_ResonVsNonReson',
                                     'AtlasLimitsMax_AtlasNotation.tsv')

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

    with open(pathTxtFileWithDataIds) as file:
        dataIds = [line.strip() for line in file]

    df = pandas.read_table(pathAtlasBPpoints)

    ## Find the Atlas limit points within BP2 and BP3 mass ranges
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

    ## plot the ratio of p p > eta0 h and p p > eta0 h / iota0

    ratio = {
    'ms': [],
    'mx': [],
    'pp_eta0h': [],
    'pp_iota0_eta0h': [],
    'ratio': []
    }

    for dataId in dataIds:
        ## read in Madgraph calculations
        pathMadgraphCrossSection = os.path.join(pathDataIdParent, 
                                                dataId,
                                                runName,
                                                f'output_{dataId}_{runName}.tsv')
        dfMadgraph = pandas.read_table(pathMadgraphCrossSection)

        # we do not want points which are right on the ms = 125 GeV line
        if (abs(dfMadgraph['mH1'][0] - 125) < 10**(-6) or
            abs(dfMadgraph['mH2'][0] - 125) < 10**(-6)):
            continue
        print(dataId)
        print(dfMadgraph)
        ratio['pp_iota0_eta0h'].append(dfMadgraph['pp_iota0_eta0h'][0])
        ratio['pp_eta0h'].append(dfMadgraph['pp_eta0h'][0])
        ratio['ratio'].append(dfMadgraph['ratio'][0])

        ## save ms and mx
        if abs(dfMadgraph['mH2'][0] - 125.09) < 10**(-6):
            ms = dfMadgraph['mH1'][0]
            mx = dfMadgraph['mH3'][0]


        elif abs(dfMadgraph['mH1'][0] - 125.09) < 10**(-6):
            ms = dfMadgraph['mH2'][0]
            mx = dfMadgraph['mH3'][0]

        ratio['ms'].append(ms)
        ratio['mx'].append(mx)

    ### plot the ratio of Madgraph and ScannerS cross sections

    ## BP2
    fig, ax = plt.subplots()
    # plot all the Atlas limit points just to see which ones were picked
    # to calculate with Madgraph
    ax.scatter(AtlasBP2pointsMs, AtlasBP2pointsMx,
               facecolors='none', edgecolor='grey', linestyle='dashed',
               label='Atlas limits')
    # plot the points calculated with Madgraph
    scatter = ax.scatter(ratio['ms'], ratio['mx'], 
                    c=np.array(ratio['ratio']),
                    facecolors='C1')

    for i in range(len(ratio['ratio'])):
        annotation = ratio['ratio'][i]
        ax.annotate(f'{annotation:.3f}',
                            (ratio['ms'][i], ratio['mx'][i]),
                            textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45,
                    path_effects=[pe.withStroke(linewidth=2, foreground="white")])


    ax.set_xlim(1, 124)
    ax.set_ylim(126, 500)
    ax.set_xlabel(r'$M_{1}$ [GeV]')
    ax.set_ylabel(r'$M_{3}$ [GeV]')
    ax.legend(title='BP2 $\sqrt{s}=13$ TeV:\n$h_1=S$, $h_{2}=H$, $h_{3}=X$',
              alignment='left')

    fig.colorbar(scatter, ax=ax, label=r'$\sigma(gg \to h _{1} h _{2}) \ / \ \sigma(gg \to h _{3} \to h _{1}h _{2})$')
    plt.savefig(os.path.join(pathSavefig, 'Madgraph_ResonVsNonResonRatio_BP2.pdf'))
    plt.savefig(os.path.join(pathSavefig, 'Madgraph_ResonVsNonResonRatio_BP2.png'))
    plt.close()

    ## BP3
    fig, ax = plt.subplots()
    ax.scatter(AtlasBP3pointsMs, AtlasBP3pointsMx,
               facecolors='none', edgecolor='grey', linestyle='dashed',
               label='Atlas limits')
    scatter = ax.scatter(ratio['ms'], ratio['mx'], 
                    c=np.array(ratio['ratio']),
                    facecolors='C1')

    for i in range(len(ratio['ratio'])):
        annotation = ratio['ratio'][i]
        ax.annotate(f'{annotation:.3f}',
                            (ratio['ms'][i], ratio['mx'][i]),
                            textcoords='offset points', xytext=(-3,-2), fontsize=10, rotation=45,
                    path_effects=[pe.withStroke(linewidth=2, foreground="white")])

    ax.set_xlim(126, 500)
    ax.set_ylim(255, 650)
    ax.set_xlabel(r'$M_{2}$ [GeV]')
    ax.set_ylabel(r'$M_{3}$ [GeV]')
    ax.legend(title='BP3 $\sqrt{s}=13$ TeV:\n$h_1=H$, $h_{2}=S$, $h_{3}=X$',
              alignment='left', loc='lower right')

    fig.colorbar(scatter, ax=ax, label=r'$\sigma(gg \to h _{1} h _{2}) \ / \ \sigma(gg \to h _{3} \to h _{1} h _{2})$')
    plt.savefig(os.path.join(pathSavefig, 'Madgraph_ResonVsNonResonRatio_BP3.pdf'))
    plt.savefig(os.path.join(pathSavefig, 'Madgraph_ResonVsNonResonRatio_BP3.png'))
    plt.close()

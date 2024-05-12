import glob
import os
import json

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import mplhep as hep
from helpScannerS import functions as TRSM

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to plots
    # E: (or you can leave it as is)
    pathPlots = os.path.join(pathRepo, 'parameter1D', 'plots')

    # path to condor job output
    # E:
    pathOutputParent = '/eos/user/i/ihaque/parameter1DPlots' 

    # plotting style
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

    os.makedirs(os.path.join(pathPlots, 'BP2', 'region1'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, 'BP2', 'region2'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, 'BP3', 'region1'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, 'BP3', 'region2'), exist_ok=True)

    processLatex = {'x_H3_H1_bb_H2_gamgam': 'gg\\to h_{3} \\to h_{1}(\gamma\gamma)h_{2}(b\\bar{b})',
                    'x_H3_H1_gamgam_H2_bb': 'gg\\to h_{3} \\to h_{1}(b\\bar{b})h_{2}(\gamma\gamma)'}

    regionLatex = {'region1': 'region 1',
                   'region2': 'region 2'}

    xlabelLatex = {'thetahS': '$\\theta_{hS}$',
                   'thetahX': '$\\theta_{hX}$',
                   'thetaSX': '$\\theta_{SX}$',
                   'vs': '$v_{s}$ [GeV]',
                   'vx': '$v_{x}$ [GeV]'}

    freeLatex = {'thetahS': '\\theta_{hS}',
                 'thetahX': '\\theta_{hX}',
                 'thetaSX': '\\theta_{SX}',
                 'vs': 'v_{s}',
                 'vx': 'v_{x}'}

    lims = {'thetahS': [-np.pi/2, +np.pi/2],
            'thetahX': [-np.pi/2, +np.pi/2],
            'thetaSX': [-np.pi/2, +np.pi/2],
            'vs': [1, 1000],
            'vx': [1, 1000]}

    AtlasNotation = {'BP2': '$h_{1}=S$, $h_{2}=H$, $h_{3}=X$',
                     'BP3': '$h_{1}=H$, $h_{2}=S$, $h_{3}=X$'}

    BPXvals = {'BP2_thetahS': 1.352,
               'BP2_thetahX': 1.175,
               'BP2_thetaSX': -0.407,
               'BP2_vs': '120~\\text{GeV}',
               'BP2_vx': '890~\\text{GeV}',
               'BP3_thetahS': -0.129,
               'BP3_thetahX': 0.226,
               'BP3_thetaSX': -0.899,
               'BP3_vs': '140~\\text{GeV}',
               'BP3_vx': '100~\\text{GeV}'}


    for BPX in ['BP2', 'BP3']:

        for regionX in ['region1', 'region2']:

            for free in ['thetahS', 'thetahX', 'thetaSX', 'vs', 'vx']:

                # note that the the process does not matter here, either mode
                # gives the same result (see thesis), both modes are included
                # as a sanity check.
                for process in ['x_H3_H1_bb_H2_gamgam', 'x_H3_H1_gamgam_H2_bb']:

                    TRSMOutput_BPX_regionX_paths = glob.glob(os.path.join(pathOutputParent, BPX, regionX, 'X*S*'),
                                                             recursive=True)

                    fig, ax = plt.subplots()

                    for path in TRSMOutput_BPX_regionX_paths:
                        print(path)

                        pathNofree = glob.glob(os.path.join(path, 'nofree', 'output*'))[0]
                        obs_nofree = TRSM.observables(pathNofree, 'bb', 'gamgam', free)

                        pathFree = glob.glob(os.path.join(path, free, 'output_*'))[0]
                        obs = TRSM.observables(pathFree, 'bb', 'gamgam', free)

                        ax.plot(obs[free], np.array(obs[process])/obs_nofree[process][0], color='C0', alpha=0.2)
                        ax.plot(obs_nofree[free][0], 1, marker='o', color='black')
                        ax.set_xlabel(f'{xlabelLatex[free]}')
                        ax.set_ylabel(f'$\delta({freeLatex[free]}, M_{1}, M_{2}, M_{3})$')
                        ax.set_xlim(lims[free][0], lims[free][1])
                        ax.legend(title=f'{BPX}: {regionLatex[regionX]}\n{AtlasNotation[BPX]}',
                                  handles=[
                                  mlines.Line2D([], [], color='C0', alpha=0.2, label=f'$\delta({freeLatex[free]}, M_{1}, M_{2}, M_{3})$'),
                                  mlines.Line2D([], [], color='black', linestyle='none', marker='o', label=f'${freeLatex[free]}={BPXvals[f"{BPX}_{free}"]}$'),
                                  ], alignment='left')

                    plt.tight_layout()
                    plt.savefig(os.path.join(pathPlots, BPX, regionX, f'{BPX}_{regionX}_{free}_{process}.pdf'))
                    plt.close()


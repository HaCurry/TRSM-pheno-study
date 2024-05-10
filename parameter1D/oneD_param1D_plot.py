import glob
import os

import numpy as np
import pandas
import matplotlib
import matplotlib.pyplot as plt
from helpScannerS import functions as TRSM

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to condor job output
    # E:
    pathOutputParent = '/eos/user/i/ihaque/parameter1DPlots' 
    
    # path to plots
    # E: (or you can leave it as is)
    pathPlots = os.path.join(pathOutputParent, 'plots')

    os.makedirs(os.path.join(pathPlots, 'BP2', 'region1'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, 'BP2', 'region2'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, 'BP3', 'region1'), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, 'BP3', 'region2'), exist_ok=True)

    processLatex = {'x_H3_H1_bb_H2_gamgam': 'gg\\to h_{3} \\to h_{1}(\gamma\gamma)h_{2}(b\\bar{b})',
                    'x_H3_H1_gamgam_H2_bb': 'gg\\to h_{3} \\to h_{1}(b\\bar{b})h_{2}(\gamma\gamma)'}

    regionLatex = {'region1': 'R1',
                   'region2': 'R2'}

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
    
    # angles

    for BPX in ['BP2', 'BP3']:

        for regionX in ['region1', 'region2']:

            for free in ['thetahS', 'thetahX', 'thetaSX', 'vs', 'vx']:

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
                        ax.set_title(f'{BPX} {regionLatex[regionX]}: $\sigma_{{{processLatex[process]}}}/\sigma^{{fixed}}_{{{processLatex[process]}}}$')
                        ax.set_xlabel(f'${freeLatex[free]}$')
                        ax.set_ylabel(f'$\sigma_{{{processLatex[process]}}}/\sigma^{{fixed}}_{{{processLatex[process]}}}$')
                        ax.set_xlim(lims[free][0], lims[free][1])

                    plt.tight_layout()
                    plt.savefig(os.path.join(pathPlots, BPX, regionX, f'{BPX}_{regionX}_{free}_{process}.pdf'))
                    plt.close()


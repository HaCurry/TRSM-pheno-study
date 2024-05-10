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
    pathPlots = os.path.join(pathRepo, 'parameter1D', 'plots')

    processLatex = {'x_H3_H1_bb_H2_gamgam': 'gg\\to h_{1}(\gamma\gamma)h_{2}(b\\bar{b})',
                    'x_H3_H1_gamgam_H2_bb': 'gg\\to h_{1}(b\\bar{b})h_{2}(\gamma\gamma)'}

    regionLatex = {'region1': 'R1',
                   'region2': 'R2'}

    freeLatex = {'thetahS': '\\theta_{hS}',
                 'thetahX': '\\theta_{hX}',
                 'thetaSX': '\\theta_{SX}',
                 'vs': 'v_{s}',
                 'vx': 'v_{x}'}
    
    # angles

    for BPX in ['BP2', 'BP3']:

        for regionX in ['region1', 'region2']:

            for angle in ['thetahS', 'thetahX', 'thetaSX']:

                for process in ['x_H3_H1_bb_H2_gamgam', 'x_H3_H1_gamgam_H2_bb']:
    
                    TRSMOutput_BPX_regionX_paths = glob.glob(os.path.join(pathOutputParent, BPX, regionX, 'X*S*'),
                                                             recursive=True)

                    fig, ax = plt.subplots()

                    for path in TRSMOutput_BPX_regionX_paths:
                        print(path)
                        pathNofree = glob.glob(os.path.join(path, 'nofree', 'output*'))[0]
                        obs_nofree = TRSM.observables(pathNofree, 'bb', 'gamgam')
        
                        free = angle
                        pathFree = glob.glob(os.path.join(path, free, 'output_*'))[0]
                        obs = TRSM.observables(pathFree, 'bb', 'gamgam', free)
                        process = 'x_H3_H1_bb_H2_gamgam'
                        ax.plot(obs[free], np.array(obs[process])/obs_nofree[process][0], color='C0', alpha=0.5)
                        # ax.legend(title=f'{BPX} $\sqrt{{s}}=13$\n')
                        ax.set_title(f'{BPX} {regionLatex[regionX]}: $\sigma_{{{processLatex[process]}}}/\sigma^{{fixed}}_{processLatex[process]}$')
                        ax.set_xlabel(f'${freeLatex[angle]}$')
                        ax.set_ylabel(f'$\sigma_{processLatex[process]}/\sigma^{{fixed}}_{processLatex[process]}$')

                plt.savefig(os.path.join(pathPlots, f'{BPX}_{regionX}_{angle}_{process}.pdf'))
                plt.close()

    # vevs


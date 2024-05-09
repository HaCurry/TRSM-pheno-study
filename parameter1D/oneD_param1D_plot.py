import glob
import os

import numpy as np
import pandas
import matplotlib
import matplotlib.pyplot as plt
from helpScannerS import functions as TRSM

if __name__ == '__main__':

    ## paths

    # path to condor job output
    # E:
    pathOutputParent = '/eos/user/i/ihaque/parameter1DPlots' 
    
    ## BP2

    # region 1


    # for path in TRSMOutput_BP2_R1_paths:
    #     df = pandas.read_table(path)
    #     obs = TRSM.observables(path, 'bb', 'gamgam', 'thetahS')
    #     plt.plot(obs['thetahS'], obs['x_H3_H1_gamgam_H2_bb'])

    plt.savefig('test2.pdf')
    plt.close()

    # region 2

    TRSMOutput_BP2_R2_paths = glob.glob(os.path.join(pathOutputParent, 'BP2', 'region2', 'X*S*'),
                                                recursive=True)

    for path in TRSMOutput_BP2_R2_paths:
        print(path)
        pathNofree = glob.glob(os.path.join(path, 'nofree', 'output*'))[0]
        obs_nofree = TRSM.observables(pathNofree, 'bb', 'gamgam')
        
        free = 'thetahS'
        pathFree = glob.glob(os.path.join(path, free, 'output_*'))[0]
        obs = TRSM.observables(pathFree, 'bb', 'gamgam', 'thetahS')
        process = 'x_H3_H1_bb_H2_gamgam'
        plt.plot(obs[free], np.array(obs[process])/obs_nofree[process][0])

    plt.savefig('test.pdf')
    plt.close()

    ## BP3

    # region 1

    # region 2

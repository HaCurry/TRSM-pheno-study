import os
import json

import numpy as np
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import mplhep as hep

from helpScannerS import functions as TRSM

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/'

    # path to condor job output
    # E:
    pathOutputParent = '/eos/user/i/ihaque/AtlasLimitsGridSearchOutput'

    # path to plots
    # E:
    pathPlots = os.path.join(pathRepo, 'AtlasLimitsGridSearch', 'plots', 'plotDist')

    # create plotting directory
    os.makedirs(pathPlots, exist_ok=True)

    df = pandas.read_table(os.path.join(pathRepo, 'AtlasLimitsGridSearch', 'AtlasLimitsGridSearchMax.tsv'))

    ms = np.array([element for element in df['ms']])
    mx = np.array([element for element in df['mx']])
    ObsLim = np.array([element for element in df['ObsLim']])
    max = np.array([element for element in df['x_X_S_bb_H_gamgam_max']])

    norm = (31.02 * 0.0026) * 10**(-3)

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

    # ## read in the 2023 Atlas limits
    # limitsUntransposed = pandas.read_json(os.path.join(pathRepo, 'Atlas2023Limits.json'))
    # print(limitsUntransposed)
    # limits=limitsUntransposed.T
    # print(limits)

    # ms = [element for element in limits['S']]
    # mx = [element for element in limits['X']]

    # # save it in pb
    # XS = [element for element in 10**(-3) *limits['ObservedLimit']]
    # dataIds = [element for element in limits.index]

    # # dataId below will be the name of the folder containing all
    # # the output (i.e cross sections and madgraph output) from execution
    # # of the corresponding model parameters in listModelTuples
    # listModelTuples = []
    # for i in range(len(dataIds)):

    #     if 125.09 < ms[i]:
    #         listModelTuples.append((125.09, ms[i], mx[i], XS[i], dataIds[i], ms[i], mx[i]))

    #     elif ms[i] < 125.09:
    #         listModelTuples.append((ms[i], 125.09, mx[i], XS[i], dataIds[i], ms[i], mx[i]))

    #     else:
    #         raise Exception('Something went wrong')
    df_AtlasGSMax = pandas.read_table(os.path.join(pathRepo, 'AtlasLimitsGridSearch',
                                              'AtlasLimitsGridSearchMax.tsv'))

    # for (mH1, mH2, mH3, XS, dataId, ms, mx) in listModelTuples:
    for i in range(len(df_AtlasGSMax)):

        ObsLimExclusions = df_AtlasGSMax['ObsLimExclusions'][i]
        if ObsLimExclusions > 0:

            dataId = df_AtlasGSMax['dataId'][i]
            numOfModels = df_AtlasGSMax['numOfModels'][i]
            numOfNans = df_AtlasGSMax['numOfNans'][i]
            ObsLimExclusions = df_AtlasGSMax['ObsLimExclusions'][i]
            ObsLim = df_AtlasGSMax['ObsLim'][i]
            
            pathOutput = os.path.join(pathOutputParent, dataId, f'output_{dataId}.tsv')
            obs = TRSM.observables(pathOutput, 'bb', 'gamgam', normSM=1)

            mH1, mH2, mH3 = df_AtlasGSMax['mH1'][i], df_AtlasGSMax['mH2'][i], df_AtlasGSMax ['mH3'][i]

            # BP2
            if abs(mH2 - 125.09) < 10**(-6):
                x_X_S_bb_H_gamgam = 'x_H3_H1_bb_H2_gamgam'

            # BP3
            elif abs(mH1 - 125.09) < 10**(-6):
                x_X_S_bb_H_gamgam = 'x_H3_H1_gamgam_H2_bb'

            fig, ax = plt.subplots()
            count, edges, bars = ax.hist(obs[x_X_S_bb_H_gamgam], bins=15)
            ax.bar_label(bars)
            ax.axvline(ObsLim, color='red', ls='dashed')
            ax.legend(title=f"total generated $\sigma$'s = {numOfModels}\n\
number of np.nan's = {numOfNans}\n\
number of exclusions = {ObsLimExclusions}\n\
$\sigma(obs) = {ObsLim:.5f}$ pb",
                      alignment='left')

            ax.set_ylim(0,100)
            ax.set_title(dataId)
            ax.set_xlabel(r'$\sigma$ [pb]', labelpad=25)
            ax.set_ylabel(r'count')
            plt.savefig(os.path.join(pathPlots, f'{dataId}.pdf'))
            plt.close()

            fig, ax = plt.subplots()
            ax.hist(obs[x_X_S_bb_H_gamgam], bins=15)
            ax.axvline(ObsLim, color='red', ls='dashed')
            ax.set_title(f'{dataId} - full window')
            ax.set_xlabel(r'$\sigma$ [pb]')
            ax.set_ylabel(r'count')
            plt.savefig(os.path.join(pathPlots, f'{dataId}_large.pdf'))
            plt.close()



        else:
            continue
        

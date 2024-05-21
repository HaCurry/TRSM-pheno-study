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

    df_AtlasGSMax = pandas.read_table(os.path.join(pathRepo, 'AtlasLimitsGridSearch',
                                              'AtlasLimitsGridSearchMax.tsv'))

    norm = (31.05 * 10**(-3)) * 0.002637
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

            count, edges, bars = ax.hist(np.array(obs[x_X_S_bb_H_gamgam])/norm, bins=15)
            ax.bar_label(bars)
            ax.axvline(ObsLim/norm, color='red', ls='dashed')
            ax.set_ylim(0,100)
            ax.set_xlabel(r'$\sigma(gg\to X \to S(b\bar{b})~H(\gamma\gamma))/\sigma(ref)$')
            ax.set_ylabel(r'Surviving models')

            ax.legend(title=f"Zoomed in\n\
$M_{{S}}={df_AtlasGSMax['ms'][i]}$, $M_{{X}}={df_AtlasGSMax['mx'][i]}$\n\
Fraction of surviving models (out of $10^{{5}}$): {numOfModels/100000:.2f}\n\
Number of exclusions: {ObsLimExclusions}\n\
$\sigma(obs)/\sigma(ref) = {ObsLim/norm:.1f}$\n\
$ref=gg\\to h_{{SM}}h_{{SM}}\\to b\\bar{{b}}\gamma\gamma$",
                      loc='upper right', alignment='left')
            plt.tight_layout()
            plt.savefig(os.path.join(pathPlots, f'{dataId}.pdf'))
            plt.close()

            fig, ax = plt.subplots()

            ax.hist(np.array(obs[x_X_S_bb_H_gamgam])/norm, bins=15)
            ax.axvline(ObsLim/norm, color='red', ls='dashed')
            ax.set_xlabel(r'$\sigma(gg\to X \to S(b\bar{b})~H(\gamma\gamma))/\sigma(ref)$')
            ax.set_ylabel(r'Surviving models')


            ax.legend(title=f"Full window\n\
$M_{{S}}={df_AtlasGSMax['ms'][i]}$, $M_{{X}}={df_AtlasGSMax['mx'][i]}$\n\
Fraction of surviving models (out of $10^{{5}}$): {numOfModels/100000:.2f}\n\
Number of exclusions: {ObsLimExclusions}\n\
$\sigma(obs)/\sigma(ref) = {ObsLim/norm:.1f}$\n\
$ref=gg\\to h_{{SM}}h_{{SM}}\\to b\\bar{{b}}\gamma\gamma$",
                      loc='upper right', alignment='left')
            plt.tight_layout()
            plt.savefig(os.path.join(pathPlots, f'{dataId}_large.pdf'))
            plt.close()



        else:
            continue
        

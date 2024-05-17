import os
import json

import numpy as np
import pandas
import matplotlib as mpl
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import mplhep as hep
from helpScannerS import configurer as config
from helpScannerS import functions as TRSM
from helpScannerS import twoDPlotter as twoDPlot

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/'

    # path to plots
    # E: (or you can leave as is)
    pathPlots = os.path.join(pathRepo, 'AtlasLimitsBenchmarkplanes', 'plots')

    # path to ScannerS values at Atlas limit points
    pathAtlasBP = os.path.join(pathRepo, 'AtlasLimitsBenchmarkplanes', 'AtlasLimitsBenchmarkplanes.tsv')
    
    os.makedirs(pathPlots, exist_ok=True)

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

    
    obs = TRSM.observables(pathAtlasBP, 'bb', 'gamgam', 'mH1', 'mH2', 'mH3', 'ObsLim',
                           normSM=1)

    ms_BP2 = []
    mx_BP2 = []
    XS_BP2 = []
    ObsLim_BP2 = []

    ms_BP3 = []
    mx_BP3 = []
    XS_BP3 = []
    ObsLim_BP3 = []

    for i in range(len(obs['mH1'])):

        # BP2
        if abs(obs['mH2'][i] - 125.09) < 10**(-6):
            ms_BP2.append(obs['mH1'][i])
            mx_BP2.append(obs['mH3'][i])
            XS_BP2.append(obs['x_H3_H1_bb_H2_gamgam'][i])
            ObsLim_BP2.append(obs['ObsLim'][i])

        # BP3
        elif abs(obs['mH1'][i] - 125.09) < 10**(-6):
            ms_BP3.append(obs['mH2'][i])
            mx_BP3.append(obs['mH3'][i])
            XS_BP3.append(obs['x_H3_H1_gamgam_H2_bb'][i])
            ObsLim_BP3.append(obs['ObsLim'][i])

        else:
            raise Exception('Something went wrong...')
            

    # BP2
    
    fig, ax = plt.subplots()

    scatter = ax.scatter(ms_BP2, mx_BP2, c=np.array(ObsLim_BP2)/np.array(XS_BP2))
    print((np.array(ObsLim_BP2)/np.array(XS_BP2))[0])
    print(ms_BP2[0])
    print(mx_BP2[0])
    print(np.array(XS_BP2)[0])
    print(np.array(ObsLim_BP2)[0])
    for i in range(len(XS_BP2)):
        print(f'XS: {XS_BP2[i]}')
        print(f'ObsLim: {ObsLim_BP2[i]}')
        print(f'ObsLim/XS: {(np.array(ObsLim_BP2)/np.array(XS_BP2))[i]}')
        ax.annotate('{:.0f}'.format((np.array(ObsLim_BP2)/np.array(XS_BP2))[i]), (ms_BP2[i], mx_BP2[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=9, rotation=45, 
                     path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground='w')])
    
    ax.legend(title='BP2 @ $13$ TeV:\n$h_1=S$, $h_2=H$, $h_3=X$',
              alignment='left')

    twoDPlot.plotAuxTitleAndBounds2D('', '$M_{1}$ [GeV]', '$M_{3}$ [GeV]',
                                     '$\sigma(lim)/\sigma(gg\\to h_{3} \\to h_{1}(b\\bar{b})~h_{2}(\gamma\gamma))$', 
                                     fig=fig, im=scatter, ax=ax)

    plt.savefig(os.path.join(pathPlots, 'BP2.pdf'))
    plt.close()


    # BP3
    
    fig, ax = plt.subplots()

    scatter = ax.scatter(ms_BP3, mx_BP3, c=np.array(ObsLim_BP3)/np.array(XS_BP3))

    for i in range(len(XS_BP3)):
        print(f'XS: {XS_BP3[i]}')
        print(f'ObsLim: {ObsLim_BP3[i]}')
        print(f'ObsLim/XS: {(np.array(ObsLim_BP3)/np.array(XS_BP3))[i]}')
        ax.annotate('{:.0f}'.format((np.array(ObsLim_BP3)/np.array(XS_BP3))[i]), (ms_BP3[i], mx_BP3[i]),
                     textcoords='offset points', xytext=(-3,-2), fontsize=9, rotation=45, 
                     path_effects=[pe.withStroke(linewidth=1.5, foreground='w')])
    
    ax.legend(title='BP3 @ $13$ TeV:\n$h_1=S$, $h_2=H$, $h_3=X$',
              alignment='left')

    twoDPlot.plotAuxTitleAndBounds2D('', '$M_{2}$ [GeV]', '$M_{3}$ [GeV]',
                                     '$\sigma(lim)/\sigma(gg\\to h_{3} \\to h_{1}(\gamma\gamma)~h_{2}(b\\bar{b}))$', 
                                     fig=fig, im=scatter, ax=ax)

    plt.savefig(os.path.join(pathPlots, 'BP3.pdf'))
    plt.close()

import configurer as config

import subprocess
import os
import json

import scipy.interpolate
import numpy as np
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import matplotlib.lines as mlines

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/'

    # path to plotting directory
    # E:
    pathPlots = '/eos/user/i/ihaque/SusHiPlots'

    # path to ScannerS TRSM executable
    # E:
    pathTRSM = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken'

    # create plotting directory if they do not already exist
    os.makedirs(os.path.join(pathPlots), exist_ok=True)
    os.makedirs(os.path.join(pathPlots, '13TeV'), exist_ok=True)

    # create directories which ScannerS will store output and input
    # if they do not already exist
    pathTemp = os.path.join(pathRepo,
                            'testing/SusHi_HiggsCrossSections/TRSMOutputsTemp')
    os.makedirs(pathTemp, exist_ok=True)

    with open(os.path.join(pathRepo,
              'testing/SusHi_HiggsCrossSections/ggH_bbH.dat')) as f:
        first_line = f.readline()

    # create dictionary where all output from ScannerS will be stored
    massesAndCrossSec = {}
    massesAndCrossSec['mass'] = []
    massesAndCrossSec['TRSMCrossSec'] = []
    massesAndCrossSec['SMCrossSec'] = []

    # masses which ScannerS will generate cross sections for
    masses = ([float(i) for i in first_line.split()])

    # disable all ScannerS TRSM constraints
    BFB, Uni, STU, Higgs = 0, 0, 0, 0

    # path to where the output and input of ScannerS is stored
    pathTemp = os.path.join(pathRepo,
                            'testing/SusHi_HiggsCrossSections/TRSMOutputsTemp')
    pathExecutionConfig = os.path.join(pathTemp, 'temp_config.tsv')
    pathExecutionOutput = os.path.join(pathTemp, 'temp_output.tsv')

    for mass in masses:

        dictModelParams = {'mH1_lb': 1, 'mH1_ub': 1,
                           'mH2_lb': 2, 'mH2_ub': 2,
                           'mH3_lb': mass, 'mH3_ub': mass,
                           'thetahS_lb': 1.352,  'thetahS_ub': 1.352,
                           'thetahX_lb': 1.175,  'thetahX_ub': 1.175,
                           'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407,
                           'vs_lb': 120, 'vs_ub': 120,
                           'vx_lb': 890, 'vx_ub': 890}

        # creates a .tsv file with model parameters in pathExecutionConfig
        # given by dictModelParams, the TRSM executable will take this as
        # input
        config.checkCreatorNew(pathExecutionConfig, dictModelParams)

        # command line arguments required when running the ScannerS
        # TRSM executable
        runTRSM = [pathTRSM, '--BFB', str(BFB), '--Uni', str(Uni),
                   '--STU', str(STU), '--Higgs', str(Higgs), 
                   pathExecutionOutput, 'check', pathExecutionConfig]

        # run the ScannerS TRSM executable
        shell_output = subprocess.run(runTRSM, cwd=pathTemp)

        df = pandas.read_table(pathExecutionOutput)
        TRSMCrossSec = df['x_H3_gg'][0]
        SMCrossSec = df['x_H3_gg'][0]/(df['R31'][0]**2)

        # crossSec.append((mass, TRSMCrossSec, SMCrossSec))
        massesAndCrossSec['mass'].append(mass)
        massesAndCrossSec['SMCrossSec'].append(SMCrossSec)
        massesAndCrossSec['TRSMCrossSec'].append(TRSMCrossSec)

    dfOut = pandas.DataFrame(massesAndCrossSec)
    print(dfOut)
    dfOut.to_csv('13TeV_ScannerSCrossSections.tsv', sep='\t')

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
    
    # plot the TRSM cross sections
    plt.plot(np.array(dfOut['mass']), np.array(dfOut['TRSMCrossSec']),
             marker='o')
    plt.yscale('log')
    plt.savefig(os.path.join(pathPlots, '13TeV',
                '13TeV_ScannerSTRSMCrossSections.pdf'))
    plt.close()

    # plot the SM cross sections
    plt.plot(np.array(dfOut['mass']), np.array(dfOut['SMCrossSec']),
             marker='o')
    plt.yscale('log')
    plt.savefig(os.path.join(pathPlots, '13TeV',
                '13TeV_ScannerSSMCrossSections.pdf'))
    plt.close()

    ## create 13.6 (ScannerS * SusHiFactor) SM cross sections

    dfSusHi_13 = pandas.read_table('13TeV_SusHiCrossSections.tsv')
    XSSusHi_13 = np.array(dfSusHi_13['crossSec'])

    dfSusHi_13_6 = pandas.read_table('13_6TeV_SusHiCrossSections.tsv')
    XSSusHi_13_6 = np.array(dfSusHi_13_6['crossSec'])

    XS_13_to_13_6_factor = XSSusHi_13_6/XSSusHi_13

    XSScannerS_13_6 = np.array(dfOut['SMCrossSec']) * XS_13_to_13_6_factor

    dfOut_13_6 = pandas.DataFrame({'mass': dfOut['mass'],
                                  'SMCrossSec': XSScannerS_13_6})
    dfOut_13_6.to_csv('13_6TeV_ScannerSCrossSections.tsv', sep='\t')

    # create dataframe with 14 TeV cross sections for comparison below
    dfOut_14 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                 'SusHi_HiggsCrossSections',
                                 '14TeV_YR4CrossSections.tsv'))

    # plot the 13.6 TeV (ScannerS * SusHiFactor) SM cross sections
    fig, axes = plt.subplots(1, 2)
    fig.suptitle('13.6 TeV ScannerS')
    fig.supylabel(r'$\sigma$ [pb]')
    fig.supxlabel(r'$M_{h_{SM}}$ [GeV]')

    axes[0].plot(np.array(dfOut_13_6['mass']), np.array(dfOut_13_6['SMCrossSec']))
    axes[0].set_xlim(0, 500)
    axes[0].set_ylim(10**(0), 10**(4))
    axes[0].set_yscale('log')

    axes[1].plot(np.array(dfOut_13_6['mass']), np.array(dfOut_13_6['SMCrossSec']))
    axes[1].set_xlim(500, 1000)
    axes[1].set_ylim(10**(0), 10**(1))
    axes[1].set_yscale('log')

    plt.savefig(os.path.join(pathPlots, '13_6TeV',
                '13_6TeV_ScannerSSMCrossSections.pdf'))
    plt.close()

    # plot the 13.6 TeV (SusHi), 13 TeV (ScannerS) and 14 TeV (YR4)
    # SM cross sections together

    fig, ax = plt.subplots()

    ax.plot(np.array(dfOut['mass']), np.array(dfOut['SMCrossSec']),
                 label='13 TeV ScannerS', color='C0', linewidth=0.5)
    ax.plot(np.array(dfSusHi_13_6['mass']), np.array(dfSusHi_13_6['crossSec']),
                 label='13.6 TeV ScannerS', color='C1', linewidth=0.5)
    ax.plot(np.array(dfOut_14['mass']), np.array(dfOut_14['SMCrossSec']),
                 label='14 TeV YR4', color='C2', linewidth=0.5)
    ax.set_xlim(0, 100)
    ax.set_ylim(5 * 10**(1), 10**(4))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '13_6TeV',
                '13_6TeV_13TeV_14TeV_ScannerSSMAndSusHiPureAndYR4CrossSections_1.pdf'))
    plt.close()


    fig, ax = plt.subplots()

    ax.plot(np.array(dfOut['mass']), np.array(dfOut['SMCrossSec']),
                 label='13 TeV ScannerS', color='C0', linewidth=0.5)
    ax.plot(np.array(dfSusHi_13_6['mass']), np.array(dfSusHi_13_6['crossSec']),
                 label='13.6 TeV ScannerS', color='C1', linewidth=0.5)
    ax.plot(np.array(dfOut_14['mass']), np.array(dfOut_14['SMCrossSec']),
                 label='14 TeV YR4', color='C2', linewidth=0.5)
    ax.set_xlim(100, 500)
    ax.set_ylim(4 * 10**(0), 7 * 10**(1))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '13_6TeV',
                '13_6TeV_13TeV_14TeV_ScannerSSMAndSusHiPureAndYR4CrossSections_2.pdf'))
    plt.close()


    fig, ax = plt.subplots()

    ax.plot(np.array(dfOut['mass']), np.array(dfOut['SMCrossSec']),
                 label='13 TeV ScannerS', color='C0', linewidth=0.5)
    ax.plot(np.array(dfSusHi_13_6['mass']), np.array(dfSusHi_13_6['crossSec']),
                 label='13.6 TeV ScannerS (SusHi)', color='C1', linewidth=0.5)
    ax.plot(np.array(dfOut_14['mass']), np.array(dfOut_14['SMCrossSec']),
                 label='14 TeV YR4', color='C2', linewidth=0.5)
    ax.set_xlim(500, 1000)
    ax.set_ylim(10**(-1), 6 * 10**(0))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '13_6TeV',
                '13_6TeV_13TeV_14TeV_ScannerSSMAndSusHiPureAndYR4CrossSections_3.pdf'))
    plt.close()


    # plot the 13.6 TeV (ScannerS * SusHiFactor), 13 TeV (ScannerS) and 14 TeV (YR4)
    # SM cross sections together

    fig, ax = plt.subplots()

    ax.plot(np.array(dfOut['mass']), np.array(dfOut['SMCrossSec']),
                 label='13 TeV ScannerS', color='C0', linewidth=0.5)
    ax.plot(np.array(dfOut_13_6['mass']), np.array(dfOut_13_6['SMCrossSec']),
                 label='13.6 TeV ScannerS', color='C1', linewidth=0.5)
    ax.plot(np.array(dfOut_14['mass']), np.array(dfOut_14['SMCrossSec']),
                 label='14 TeV YR4', color='C2', linewidth=0.5)
    ax.set_xlim(0, 100)
    ax.set_ylim(5 * 10**(1), 10**(4))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1 (improved)'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '13_6TeV',
                '13_6TeV_13TeV_14TeV_ScannerSSMAndSusHiandYR4CrossSections_1.pdf'))
    plt.close()

    fig, ax = plt.subplots()

    ax.plot(np.array(dfOut['mass']), np.array(dfOut['SMCrossSec']),
                 label='13 TeV ScannerS', color='C0', linewidth=0.5)
    ax.plot(np.array(dfOut_13_6['mass']), np.array(dfOut_13_6['SMCrossSec']),
                 label='13.6 TeV ScannerS', color='C1', linewidth=0.5)
    ax.plot(np.array(dfOut_14['mass']), np.array(dfOut_14['SMCrossSec']),
                 label='14 TeV YR4', color='C2', linewidth=0.5)
    ax.set_xlim(100, 500)
    ax.set_ylim(4 * 10**(0), 7 * 10**(1))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1 (improved)'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '13_6TeV',
                '13_6TeV_13TeV_14TeV_ScannerSSMAndSusHiandYR4CrossSections_2.pdf'))
    plt.close()

    fig, ax = plt.subplots()

    ax.plot(np.array(dfOut['mass']), np.array(dfOut['SMCrossSec']),
                 label='13 TeV ScannerS', color='C0', linewidth=0.5)
    ax.plot(np.array(dfOut_13_6['mass']), np.array(dfOut_13_6['SMCrossSec']),
                 label='13.6 TeV ScannerS (SusHi)', color='C1', linewidth=0.5)
    ax.plot(np.array(dfOut_14['mass']), np.array(dfOut_14['SMCrossSec']),
                 label='14 TeV YR4', color='C2', linewidth=0.5)
    ax.set_xlim(500, 1000)
    ax.set_ylim(10**(-1), 6 * 10**(0))
    ax.set_yscale('log')

    ax.set_xlabel(r'$M_{h_{SM}}$ [GeV]')
    ax.set_ylabel(r'$\sigma(gg \to h _{SM})$ [pb]')

    ax.legend(title='ggF cross sections',
              handles=[
              mlines.Line2D([], [], color='C0', label='13 TeV LHCHWG (ScannerS)'),
              mlines.Line2D([], [], color='C1', label='13.6 TeV SusHi-1.6.1 (improved)'),
              mlines.Line2D([], [], color='C2', label='14 TeV LHCHWG'),
              ], loc='upper right', alignment='left')

    plt.tight_layout()
    plt.savefig(os.path.join(pathPlots, '13_6TeV',
                '13_6TeV_13TeV_14TeV_ScannerSSMAndSusHiandYR4CrossSections_3.pdf'))
    plt.close()

    # print the cross section for comparison
    SM14TeV = scipy.interpolate.CubicSpline(dfOut_14['mass'], dfOut_14['SMCrossSec'])
    print('mass, 13 TeV ScannerS, 13.6 TeV ScannerS, 14 TeV YR4 cross sections')
    [print(dfOut['mass'][i], dfOut['SMCrossSec'][i],
           dfOut_13_6['SMCrossSec'][i], SM14TeV(dfOut['mass'][i]))
     for i in range(len(dfOut))]

    # print the ratios of the cross sections for comparison
    print('mass, (13.6 TeV ScannerS)/(13 TeV ScannerS),\
(14 TeV YR4)/(13.6 TeV ScannerS) ratios of cross sections')
    [print(dfOut['mass'][i], dfOut_13_6['SMCrossSec'][i]/dfOut['SMCrossSec'][i],
           SM14TeV(dfOut['mass'][i])/dfOut_13_6['SMCrossSec'][i])
     for i in range(len(dfOut))]

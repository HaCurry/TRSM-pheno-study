import pandas
import numpy as np

import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep

if __name__ == '__main__':

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to plotting directory
    # E:
    pathPlots = '/eos/user/i/ihaque/SusHiPlots'

    # create directories if they do not already exist
    os.makedirs(pathPlots, exist_ok=True)
    os.makedirs(os.path.join(pathPlots, '13_6TeV/scaleUncert'), exist_ok=True)

    # read in all .tsv files with varied muR and muF
    pathOutput_025mh_025mh = os.path.join(pathRepo,
                                          'testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections_ScaleUncert/13_6TeV_SusHiCrossSections_025mh_025mh.tsv')
    df_025mh_025mh = pandas.read_table(pathOutput_025mh_025mh)
    
    pathOutput_025mh_1mh = os.path.join(pathRepo, 
                                        'testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections_ScaleUncert/13_6TeV_SusHiCrossSections_025mh_1mh.tsv')
    df_025mh_1mh = pandas.read_table(pathOutput_025mh_1mh)
    
    pathOutput_1mh_1mh = os.path.join(pathRepo,
                                      'testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections_ScaleUncert/13_6TeV_SusHiCrossSections_1mh_1mh.tsv')
    df_1mh_1mh = pandas.read_table(pathOutput_1mh_1mh)
    
    pathOutput_1mh_025mh = os.path.join(pathRepo,
                                        'testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections_ScaleUncert/13_6TeV_SusHiCrossSections_1mh_025mh.tsv')
    df_1mh_025mh = pandas.read_table(pathOutput_1mh_025mh)
    
    pathOutput_05mh_05mh = os.path.join(pathRepo,
                                        'testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections_ScaleUncert/13_6TeV_SusHiCrossSections_05mh_05mh.tsv')
    df_05mh_05mh = pandas.read_table(pathOutput_05mh_05mh)

    # check that the dataframes are of equal length
    print(len(df_025mh_025mh['crossSec']),
          len(df_025mh_1mh['crossSec']), 
          len(df_1mh_1mh['crossSec']), 
          len(df_1mh_025mh['crossSec']), 
          len(df_05mh_05mh['crossSec']))
    # check that the length of the dataframes are the same length as the cross sections
    print(len(df_025mh_025mh), 
          len(df_025mh_1mh), 
          len(df_1mh_1mh), 
          len(df_1mh_025mh), 
          len(df_05mh_05mh))

    # save max and min for each mass point to create envelope plots
    maxList = []
    minList = []
    for i in range(len(df_025mh_025mh)):
        maxCrossSec = max(df_025mh_025mh['crossSec'][i],
                          df_025mh_1mh['crossSec'][i], 
                          df_1mh_1mh['crossSec'][i], 
                          df_1mh_025mh['crossSec'][i], 
                          df_05mh_05mh['crossSec'][i] )
        maxList.append(maxCrossSec)
        
        minCrossSec = min(df_025mh_025mh['crossSec'][i],
                          df_025mh_1mh['crossSec'][i],
                          df_1mh_1mh['crossSec'][i],
                          df_1mh_025mh['crossSec'][i],
                          df_05mh_05mh['crossSec'][i])
        minList.append(minCrossSec)

    # plotting style
    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19
    
    # plot envelope plots
    plt.plot(np.array(df_025mh_025mh['mass']), np.array(df_025mh_025mh['crossSec']),
             linewidth=0.1, label='$\mu_{R} = 0.25M_{h_{SM}}$, $\mu_{F} = 0.25M_{h_{SM}}$')
         
    plt.plot(np.array(df_025mh_1mh['mass']), np.array(df_025mh_1mh['crossSec']),
             linewidth=0.1, label='$\mu_{R} = 0.25M_{h_{SM}}$, $\mu_{F} = M_{h_{SM}}$')
         
    plt.plot(np.array(df_1mh_1mh['mass']), np.array(df_1mh_1mh['crossSec']),
             linewidth=0.1, label='$\mu_{R} = M_{h_{SM}}$, $\mu_{F} = M_{h_{SM}}$')
         
    plt.plot(np.array(df_1mh_025mh['mass']), np.array(df_1mh_025mh['crossSec']),
             linewidth=0.1, label='$\mu_{R} = M_{h_{SM}}$, $\mu_{F} = 0.25M_{h_{SM}}$')
         
    plt.plot(np.array(df_05mh_05mh['mass']), np.array(df_05mh_05mh['crossSec']),
             linewidth=0.1, label='$\mu_{R} = 0.5M_{h_{SM}}$, $\mu_{F} = 0.5M_{h_{SM}}$ (nominal)')

    plt.fill_between(df_025mh_025mh['mass'], minList, maxList, alpha=0.2)

    plt.legend()
    plt.title('SusHi 13.6 TeV scale uncertainties')
    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma^{13.6~TeV}(gg\to h_{SM})$ [pb]')
    plt.yscale('log')
    plt.xlim(0,1000)
    plt.ylim(0.1, 2*10000)
    plt.savefig(os.path.join(pathPlots, 
                             '13_6TeV/scaleUncert/13_6TeV_SusHiCrossSections_ScaleUncert.pdf'))
    plt.close()
    
    print('ratio of max and min scale uncertainties at 13.6 TeV')
    print(np.array(maxList)/np.array(minList))

    plt.plot(df_025mh_025mh['mass'], np.array(maxList)/np.array(minList))
    plt.title('SusHi 13.6 TeV ratio of maximum and minimum scale uncert.')
    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma^{13.6~TeV}_{max}/\sigma^{13.6~TeV}_{min}$')
    plt.savefig(os.path.join(pathPlots,
                             '13_6TeV/scaleUncert/13_6TeV_SusHiCrossSections_ScaleUncert_MinMaxRatio.pdf'))

    print('ratio of max scale uncertainty and default SusHi 13.6 TeV gluon fusion cross section')
    print(np.array(maxList)/np.array(df_025mh_025mh['crossSec']))

    print('ratio of default SusHi 13.6 TeV gluon fusion cross section and min scale uncertainty')
    print(np.array(minList)/np.array(df_025mh_025mh['crossSec']))

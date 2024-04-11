import pandas
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep

if __name__ == '__main__':

    # read in all .tsv files with varied muR and muF
    pathOutput_muR05_muF05 = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections_ScaleUncert/13_6TeV_SusHiCrossSections_muR05_muF05.tsv'
    df_muR05_muF05 = pandas.read_table(pathOutput_muR05_muF05)
    
    pathOutput_muR2_muF05 = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections_ScaleUncert/13_6TeV_SusHiCrossSections_muR2_muF05.tsv'  
    df_muR2_muF05 = pandas.read_table(pathOutput_muR2_muF05)
    
    pathOutput_muR2_muF2 = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections_ScaleUncert/13_6TeV_SusHiCrossSections_muR2_muF2.tsv'  
    df_muR2_muF2 = pandas.read_table(pathOutput_muR2_muF2)
    
    pathOutput_muR05_muF2 = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections_ScaleUncert/13_6TeV_SusHiCrossSections_muR05_muF2.tsv'  
    df_muR05_muF2 = pandas.read_table(pathOutput_muR05_muF2)
    
    pathOutput_muR1_muF1 = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/13_6TeV_SusHiCrossSections_ScaleUncert/13_6TeV_SusHiCrossSections_muR1_muF1.tsv'
    df_muR1_muF1 = pandas.read_table(pathOutput_muR1_muF1)

    # check that the dataframes are of equal length
    print(len(df_muR05_muF05['crossSec']), len(df_muR2_muF05['crossSec']), len(df_muR2_muF2['crossSec']), len(df_muR05_muF2['crossSec']), len(df_muR1_muF1['crossSec']))
    # check that the length of the dataframes are the same length as the cross sections
    print(len(df_muR05_muF05), len(df_muR2_muF05), len(df_muR2_muF2), len(df_muR05_muF2), len(df_muR1_muF1))

    # save max and min for each mass point to create envelope plots
    maxList = []
    minList = []
    for i in range(len(df_muR05_muF05)):
        maxCrossSec = max(
            df_muR05_muF05['crossSec'][i], 
            df_muR2_muF05['crossSec'][i],
            df_muR2_muF2['crossSec'][i],
            df_muR05_muF2['crossSec'][i],
            df_muR1_muF1['crossSec'][i]
            )
        maxList.append(maxCrossSec)
        
        minCrossSec = min(
            df_muR05_muF05['crossSec'][i], 
            df_muR2_muF05['crossSec'][i],
            df_muR2_muF2['crossSec'][i],
            df_muR05_muF2['crossSec'][i],
            df_muR1_muF1['crossSec'][i]
            )
        minList.append(minCrossSec)

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19
    
    # plot envelope plots
    plt.plot(np.array(df_muR05_muF05['mass']), np.array(df_muR05_muF05['crossSec']), linewidth=0.1, label='$\mu_{R} = 0.5$, $\mu_{F} = 0.5$ (default)')
    plt.plot(np.array(df_muR2_muF05['mass']), np.array(df_muR2_muF05['crossSec']), linewidth=0.1, label='$\mu_{R} = 2$, $\mu_{F} = 0.5$')
    plt.plot(np.array(df_muR2_muF2['mass']), np.array(df_muR2_muF2['crossSec']), linewidth=0.1, label='$\mu_{R} = 2$, $\mu_{F} = 2$')
    plt.plot(np.array(df_muR05_muF2['mass']), np.array(df_muR05_muF2['crossSec']), linewidth=0.1, label='$\mu_{R} = 0.5$, $\mu_{F} = 2$')
    plt.plot(np.array(df_muR1_muF1['mass']), np.array(df_muR1_muF1['crossSec']), linewidth=0.1, label='$\mu_{R} = 1$, $\mu_{F} = 1$')
    plt.fill_between(df_muR05_muF05['mass'], minList, maxList, alpha=0.2)

    plt.legend()
    plt.title('SusHi 13.6 TeV scale uncertainties')
    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma^{13.6~TeV}(gg\to h_{SM})$ [pb]')
    plt.yscale('log')
    plt.xlim(0,1000)
    plt.ylim(0.1, 2*10000)
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/scaleUncert/13_6TeV/13_6TeV_SusHiCrossSections_ScaleUncert.pdf')
    plt.close()
    
    print('ratio of max and min scale uncertainties at 13.6 TeV')
    print(np.array(maxList)/np.array(minList))

    plt.plot(df_muR05_muF05['mass'], np.array(maxList)/np.array(minList))
    plt.title('SusHi 13.6 TeV ratio of maximum and minimum scale uncert.')
    plt.xlabel(r'$M_{h_{SM}}$ [GeV]')
    plt.ylabel(r'$\sigma^{13.6~TeV}_{max}/\sigma^{13.6~TeV}_{min}$')
    plt.savefig('/eos/user/i/ihaque/SusHiPlots/scaleUncert/13_6TeV/13_6TeV_SusHiCrossSections_ScaleUncert_MinMaxRatio.pdf')

    print('ratio of max scale uncertainty and default SusHi 13.6 TeV gluon fusion cross section')
    print(np.array(maxList)/np.array(df_muR05_muF05['crossSec']))

    print('ratio of default SusHi 13.6 TeV gluon fusion cross section and min scale uncertainty')
    print(np.array(minList)/np.array(df_muR05_muF05['crossSec']))

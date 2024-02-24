import configurer as config
from parameterData import directorySearcher

import pandas
import numpy as np
import os

import matplotlib
import matplotlib.pyplot as plt
import mplhep as hep

if __name__ == '__main__':

    df = pandas.read_table('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_AtlasNotation.tsv', sep='\t')

    ms = df['ms']
    mx = df['mx']
    max = df['maximum']
    ObsLim = df['ObservedLimit']

    mH1 = df['mH1']
    mH2 = df['mH2']
    mH3 = df['mH3']
    thetahS = df['thetahS']
    thetahX = df['thetahX']
    thetaSX = df['thetaSX']
    vs = df['vs']
    vx = df['vx']

    msExcl = []
    mxExcl = []
    ObsLimExcl = []
    maxExcl = []

    mH1Excl = []
    mH2Excl = []
    mH3Excl = []
    thetahSExcl = []
    thetahXExcl = []
    thetaSXExcl = []
    vsExcl = []
    vxExcl = []

    for i in range(len(ObsLim/max)):
        excluded = ObsLim[i]/max[i]
        if excluded < 1:
            msExcl.append(ms[i])
            mxExcl.append(mx[i])
            ObsLimExcl.append(ObsLim[i])
            maxExcl.append(max[i])

            mH1Excl.append(mH1[i])
            mH2Excl.append(mH2[i])
            mH3Excl.append(mH3[i])
            thetahSExcl.append(thetahS[i])
            thetahXExcl.append(thetahX[i])
            thetaSXExcl.append(thetaSX[i])
            vsExcl.append(vs[i])
            vxExcl.append(vx[i])
        else:
            continue
    print('printing excluded values') 

    df2 = pandas.DataFrame({'mH1': np.array(mH1Excl), 'mH2': np.array(mH2Excl), 'mH3': np.array(mH3Excl), 
                           'thetahS': np.array(thetahSExcl), 'thetahX': np.array(thetahXExcl), 'thetaSX': np.array(thetaSXExcl),
                           'vsExcl': np.array(vsExcl), 'vxExcl': np.array(vxExcl),
                           'ms': np.array(msExcl), 'mx': np.array(mxExcl), 'Excl': np.array(ObsLimExcl)/np.array(maxExcl)})

    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df2)

    excludedScannerS = []
    excludedLimitsRatio = []
    NansInXS = []
    lenXS = []
    keys = []
    dictDistribution = {}
    pathEos = '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3' 
    for i in range(len(ObsLimExcl)):
        dataId = f'X{mxExcl[i]:.0f}_S{msExcl[i]:.0f}'

        if 125.09 < msExcl[i]:
            XSKey = 'pp_X_H1_gamgam_H2_bb'

        elif msExcl[i] < 125.09:
            XSKey = 'pp_X_H1_bb_H2_gamgam'

        else: raise Exception(f'something went wrong at index {i}')
        # keys.append(XSKey)

        path = os.path.join(pathEos, dataId, f'{dataId}_calculation.tsv')    
        dfCalc = pandas.read_table(path)
        XS = [element for element in dfCalc[XSKey]]
        dictDistribution[dataId] = {}
        dictDistribution[dataId]['XS'] = XS

        # excludedScannerS.append(dfCalc[XSKey]/100000)
        numExclusions = 0
        numNans = 0
        CheckMaxInExcluded = False

        for j in range(len(XS)):

            # fix this if statement or handle the nans somehow,
            # should they even be considered..?
            if np.isnan(ObsLimExcl[i]/XS[j]):
                numNans = numNans + 1 

            elif ObsLimExcl[i]/XS[j] < 1:

                numExclusions  = numExclusions + 1
                if abs(XS[j] - maxExcl[i]) < 10**(-12):
                    CheckMaxInExcluded = True

                else: pass

            else:
                continue

        # hmmm, make sure to check that XS is only np.non nan values, otherwise this ratio is considering np.nan values as well...
        if CheckMaxInExcluded == False:
            raise Exception(f'Something went wrong... {maxExcl[i]} was not found in XS of {msExcl[i]}, {mxExcl[i]}')

        dictDistribution[dataId]['ObservedLimit'] = ObsLimExcl[i]
        dictDistribution[dataId]['num exclusions'] = excludedLimitsRatio
        dictDistribution[dataId]['num nans'] = NansInXS
        dictDistribution[dataId]['num tot generated XS'] = len(XS)

        # excludedLimitsRatio.append(numExclusions)
        # NansInXS.append(numNans)
        # lenXS.append(len(XS))


    # print(pandas.DataFrame({'ms': msExcl, 'mx': mxExcl, 'XS ratio': excludedLimitsRatio}))
    # print(len(vsExcl), len(vxExcl), len(ObsLimExcl), len(msExcl), len(mxExcl), len(np.array(ObsLimExcl)/np.array(maxExcl)), len(mH1Excl), len(mH2Excl), len(mH3Excl), len(thetahSExcl), len(thetahXExcl), len(thetaSXExcl), len(lenXS), len(keys), len(excludedLimitsRatio))
    # dfExcludedWithMoreInfo = pandas.DataFrame({'mH1': np.array(mH1Excl), 'mH2': np.array(mH2Excl), 'mH3': np.array(mH3Excl), 
    #                                     'thetahS': np.array(thetahSExcl), 'thetahX': np.array(thetahXExcl), 'thetaSX': np.array(thetaSXExcl),
    #                                     'vs': np.array(vsExcl), 'vx': np.array(vxExcl),
    #                                     'ms': msExcl, 'mx': mxExcl, 'ratio obs max': np.array(ObsLimExcl)/np.array(maxExcl), 
    #                                     'max excluded': maxExcl, 'Observed Limit': ObsLimExcl, 'num exclusions': excludedLimitsRatio,'num nans': NansInXS, 'num tot generated XS': lenXS, 'keys': keys})   
        
    # with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(dfExcludedWithMoreInfo)

    # x = dfExcludedWithMoreInfo['num exclusions'] == 1
    # dfExcludedOnlySingles = dfExcludedWithMoreInfo[x]
    # with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(dfExcludedOnlySingles)

    # dfExcludedOnlySingles.to_csv('testing/AtlasLimitsMax_OnlySingles.tsv', sep='\t')

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    matplotlib.rcParams['axes.labelsize'] = 19
    matplotlib.rcParams['axes.titlesize'] = 19

    for key in dictDistribution:
        plt.hist(dictDistribution[key]['XS'], bins=15)
        plt.axvline(dictDistribution[key]['ObservedLimit'],color='red', ls='dashed')
        plt.ylim(0,100)
        plt.title(key)
        plt.xlabel(r'$\sigma$ [pb]')
        plt.ylabel(r'count')
        plt.savefig(os.path.join(pathEos, 'plots', 'plotsTemp', f'{key}.png'))
        plt.close()

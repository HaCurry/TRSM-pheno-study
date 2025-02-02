import configurer as config
from parameterData import directorySearcher
import pandas
import numpy as np
import os



if __name__ == '__main__':
    
    # submission path
    afsPath ='/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_ScriptTesting/AtlasLimitsMaxCondor_ScriptTesting/AtlasLimitsMax_configure_ScriptTesting'
    # input and output path
    eosPath = '/eos/user/i/ihaque/testing/AtlasLimitsMax_ScriptTesting/AtlasLimitsMax_configure_ScriptTesting'   

 
    # calculate each dataId
    paths = directorySearcher(eosPath, '/**/output_*.tsv')
    # print(paths)
    paths = [path for path in paths if os.path.getsize(path) > 0]
    config.calculator(paths, 'bb', 'gamgam')

    # find the max for each dataId and save it in AtlasLimitsMax_max
    paths = directorySearcher(eosPath, '/**/*_calculation.tsv')

    config.maxCompiler(paths, os.path.join(eosPath, 'AtlasLimitsMax_H1_bb_H2_gamgam_Max.tsv'), 
                       'pp_X_H1_bb_H2_gamgam', 
                       limitsKey='ObservedLimit')

    config.maxCompiler(paths, os.path.join(eosPath,'AtlasLimitsMax_H1_gamgam_H2_bb_Max.tsv'), 
                       'pp_X_H1_gamgam_H2_bb', 
                       limitsKey='ObservedLimit')

    config.maxCompiler(paths, os.path.join(eosPath,'AtlasLimitsMax_H1H2_bbgamgam_Max.tsv'), 
                       'pp_X_H1H2_bbgamgam', 
                       limitsKey='ObservedLimit')

    ### compile cross sections from AtlasLimitsMax_H1_bb_H2_gamgam_Max.tsv, 
    ### AtlasLimitsMax_H1_gamgam_H2_bb_Max.tsv in terms of Atlas notation 
    ### i.e ms, mx, S(bb) H(gamgam) in a single file

    ms = []
    mx = []
    max = []
    ObsLim = []

    mH1 = []
    mH2 = []
    mH3 = []
    thetahS = []
    thetahX = []
    thetaSX = []
    vs = []
    vx = []

    df_H1_bb_H2_gamgam = pandas.read_table(os.path.join(eosPath, 'AtlasLimitsMax_H1_bb_H2_gamgam_Max.tsv'))
    
    print(df_H1_bb_H2_gamgam)

    mH1_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH1']]
    mH2_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH2']]
    mH3_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH3']]
    thetahS_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['thetahS']]
    thetahX_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['thetahX']]
    thetaSX_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['thetaSX']]
    vs_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['vs']]
    vx_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['vx']]
    
    x_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['pp_X_H1_bb_H2_gamgam']]
    ObsLim_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['ObservedLimit']]
    
    for i in range(len(x_H1_bb_H2_gamgam)):
        if abs(mH1_H1_bb_H2_gamgam[i] - 125.09) < 10**(-10):
            # ms.append(mH2_H1_bb_H2_gamgam[i])
            # mx.append(mH3_H1_bb_H2_gamgam[i])
            # max.append(x_H1_bb_H2_gamgam[i])
            # ObsLim.append(ObsLim_H1_bb_H2_gamgam[i])
            continue
        
        elif abs(mH2_H1_bb_H2_gamgam[i] - 125.09) < 10**(-10):
            ms.append(mH1_H1_bb_H2_gamgam[i])
            mx.append(mH3_H1_bb_H2_gamgam[i])
            max.append(x_H1_bb_H2_gamgam[i])
            ObsLim.append(ObsLim_H1_bb_H2_gamgam[i])
            
            mH1.append(mH1_H1_bb_H2_gamgam[i])
            mH2.append(mH2_H1_bb_H2_gamgam[i])
            mH3.append(mH3_H1_bb_H2_gamgam[i])
            thetahS.append(thetahS_H1_bb_H2_gamgam[i])
            thetahX.append(thetahX_H1_bb_H2_gamgam[i])
            thetaSX.append(thetaSX_H1_bb_H2_gamgam[i])
            vs.append(vs_H1_bb_H2_gamgam[i])
            vx.append(vx_H1_bb_H2_gamgam[i])
            
        else:
            raise Exception(f'Something went wrong at H1_bb_H2_gamgam at\n\
                            index {i},\n\
                            mH1 = {mH1_H1_bb_H2_gamgam[i]}\n\
                            mH2 = {mH2_H1_bb_H2_gamgam}\n\
                            mH3 = {mH3_H1_bb_H2_gamgam}\n\
                            max = {x_H1_bb_H2_gamgam}\n\
                            ObsLim = {ObsLim_H1_bb_H2_gamgam}')

    del df_H1_bb_H2_gamgam, mH1_H1_bb_H2_gamgam, mH2_H1_bb_H2_gamgam, mH3_H1_bb_H2_gamgam, x_H1_bb_H2_gamgam, ObsLim_H1_bb_H2_gamgam
    
    df_H1_gamgam_H2_bb = pandas.read_table(os.path.join(eosPath, 'AtlasLimitsMax_H1_gamgam_H2_bb_Max.tsv'))
    
    print(df_H1_gamgam_H2_bb)

    mH1_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH1']]
    mH2_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH2']]
    mH3_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH3']]
    thetahS_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['thetahS']]
    thetahX_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['thetahX']]
    thetaSX_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['thetaSX']]
    vs_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['vs']]
    vx_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['vx']]

    x_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['pp_X_H1_gamgam_H2_bb']]
    ObsLim_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['ObservedLimit']]


    for i in range(len(x_H1_gamgam_H2_bb)):
        if abs(mH1_H1_gamgam_H2_bb[i] - 125.09) < 10**(-10):
            ms.append(mH2_H1_gamgam_H2_bb[i])
            mx.append(mH3_H1_gamgam_H2_bb[i])
            max.append(x_H1_gamgam_H2_bb[i])
            ObsLim.append(ObsLim_H1_gamgam_H2_bb[i])
            
            mH1.append(mH1_H1_gamgam_H2_bb[i])
            mH2.append(mH2_H1_gamgam_H2_bb[i])
            mH3.append(mH3_H1_gamgam_H2_bb[i])
            thetahS.append(thetahS_H1_gamgam_H2_bb[i])
            thetahX.append(thetahX_H1_gamgam_H2_bb[i])
            thetaSX.append(thetaSX_H1_gamgam_H2_bb[i])
            vs.append(vs_H1_gamgam_H2_bb[i])
            vx.append(vx_H1_gamgam_H2_bb[i])
        
        elif abs(mH2_H1_gamgam_H2_bb[i] - 125.09) < 10**(-10):
            # ms.append(mH1_H1_gamgam_H2_bb[i])
            # mx.append(mH3_H1_gamgam_H2_bb[i])
            # max.append(x_H1_gamgam_H2_bb[i])
            # ObsLim.append(ObsLim_H1_gamgam_H2_bb[i])
            continue

        else:
            raise Exception(f'Something went wrong at H1_gamgam_H2_bb at\n\
                            index {i},\n\
                            mH1 = {mH1_H1_gamgam_H2_bb[i]}\n\
                            mH2 = {mH2_H1_gamgam_H2_bb}\n\
                            mH3 = {mH3_H1_gamgam_H2_bb}\n\
                            max = {x_H1_gamgam_H2_bb}\n\
                            ObsLim = {ObsLim_H1_gamgam_H2_bb}')

    print(f'# of elements: ms: {len(ms)}, mx: {len(mx)}, max: {len(max)}, ObsLim: {len(ObsLim)}')

    ms = np.array(ms)
    mx = np.array(mx)
    max = np.array(max)
    ObsLim = np.array(ObsLim)

    # save ms, mx, maximum and ObsLim in a tsv file
    dictToDataFrame = {'mH1': mH1, 'mH2': mH2, 'mH3': mH3, 'thetahS': thetahS, 'thetahX': thetahX, 'thetaSX': thetaSX, 'vs': vs, 'vx': vx, 
                       'ms': ms, 'mx': mx, 'ObservedLimit': ObsLim, 'maximum': max}
    df = pandas.DataFrame(dictToDataFrame)
    df.to_csv(os.path.join(eosPath, 'AtlasLimitsMax_AtlasNotation.tsv'), sep='\t')

    ### Find what points are excluded ###
    
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
    for i in range(len(ObsLimExcl)):
        pathEos = eosPath
        dataId = f'X{mxExcl[i]:.0f}_S{msExcl[i]:.0f}'
       
        if 125.09  < msExcl[i]:
            XSKey = 'pp_X_H1_gamgam_H2_bb'

        elif msExcl[i] < 125.09:
            XSKey = 'pp_X_H1_bb_H2_gamgam'
        
        else: raise Exception(f'something went wrong at index {i}')
        keys.append(XSKey)        

        path = os.path.join(pathEos, dataId, f'{dataId}_calculation.tsv')    
        dfCalc = pandas.read_table(path)
        XS = [element for element in dfCalc[XSKey]]

        excludedScannerS.append(dfCalc[XSKey]/100000)
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
        excludedLimitsRatio.append(numExclusions)
        NansInXS.append(numNans)
        lenXS.append(len(XS))

    # print(pandas.DataFrame({'ms': msExcl, 'mx': mxExcl, 'XS ratio': excludedLimitsRatio}))
    print(len(vsExcl), len(vxExcl), len(ObsLimExcl), len(msExcl), len(mxExcl), len(np.array(ObsLimExcl)/np.array(maxExcl)), len(mH1Excl), len(mH2Excl), len(mH3Excl), len(thetahSExcl), len(thetahXExcl), len(thetaSXExcl), len(lenXS), len(keys), len(excludedLimitsRatio))
    dfExcludedWithMoreInfo = pandas.DataFrame({'mH1': np.array(mH1Excl), 'mH2': np.array(mH2Excl), 'mH3': np.array(mH3Excl), 
                                        'thetahS': np.array(thetahSExcl), 'thetahX': np.array(thetahXExcl), 'thetaSX': np.array(thetaSXExcl),
                                        'vs': np.array(vsExcl), 'vx': np.array(vxExcl),
                                        'ms': msExcl, 'mx': mxExcl, 'ratio obs max': np.array(ObsLimExcl)/np.array(maxExcl), 
                                        'max excluded': maxExcl, 'Observed Limit': ObsLimExcl, 'num exclusions': excludedLimitsRatio,'num nans': NansInXS, 'num tot generated XS': lenXS, 'keys': keys})   
        
    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(dfExcludedWithMoreInfo)

    x = dfExcludedWithMoreInfo['num exclusions'] == 1
    dfExcludedOnlySingles = dfExcludedWithMoreInfo[x]
    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(dfExcludedOnlySingles)

    # dfExcludedOnlySingles.to_csv('testing/AtlasLimitsMax_OnlySingles.tsv', sep='\t')

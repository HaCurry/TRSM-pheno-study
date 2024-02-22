import configurer as config
from parameterData import directorySearcher
import pandas
import numpy as np
import os



if __name__ == '__main__':

    
    # calculate each dataId
    # paths = directorySearcher('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3', '/**/output_*.tsv')
    # print(paths)
    # config.calculator(paths, 'bb', 'gamgam')

    # find the max for each dataId and save it in AtlasLimitsMax_max
    paths = directorySearcher('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3', '/**/*_calculation.tsv')

    # config.maxCompiler(paths, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_All_Max.tsv', 
    #                    'pp_X_H1H2_bbgamgam', 'pp_X_H1H1_bbgamgam', 'pp_X_H2H2_bbgamgam', 
    #                    limitsKey='ObservedLimit')

    # config.maxCompiler(paths, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_bb_H2_gamgam_Max.tsv', 
    #                    'pp_X_H1_bb_H2_gamgam', 
    #                    limitsKey='ObservedLimit')

    # config.maxCompiler(paths, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_gamgam_H2_bb_Max.tsv', 
    #                    'pp_X_H1_gamgam_H2_bb', 
    #                    limitsKey='ObservedLimit')

    # config.maxCompiler(paths, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1H1_bbgamgam_Max.tsv', 
    #                    'pp_X_H1H1_bbgamgam', 
    #                    limitsKey='ObservedLimit')

    # config.maxCompiler(paths, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H2H2_bbgamgam_Max.tsv', 
    #                    'pp_X_H2H2_bbgamgam', 
    #                    limitsKey='ObservedLimit')

    ### compile cross sections from AtlasLimitsMax_H1_bb_H2_gamgam_Max.tsv, 
    ### AtlasLimitsMax_H1_gamgam_H2_bb_Max.tsv in terms of Atlas notation 
    ### i.e ms, mx, S(bb) H(gamgam) in a single file

    ms = []
    mx = []
    max = []
    ObsLim = []

    df_H1_bb_H2_gamgam = pandas.read_table('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_bb_H2_gamgam_Max.tsv')
    
    print(df_H1_bb_H2_gamgam)

    mH1_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH1']]
    mH2_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH2']]
    mH3_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH3']]
    
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

        else:
            raise Exception(f'Something went wrong at H1_bb_H2_gamgam at\n\
                            index {i},\n\
                            mH1 = {mH1_H1_bb_H2_gamgam[i]}\n\
                            mH2 = {mH2_H1_bb_H2_gamgam}\n\
                            mH3 = {mH3_H1_bb_H2_gamgam}\n\
                            max = {x_H1_bb_H2_gamgam}\n\
                            ObsLim = {ObsLim_H1_bb_H2_gamgam}')

    del df_H1_bb_H2_gamgam, mH1_H1_bb_H2_gamgam, mH2_H1_bb_H2_gamgam, mH3_H1_bb_H2_gamgam, x_H1_bb_H2_gamgam, ObsLim_H1_bb_H2_gamgam
    
    df_H1_gamgam_H2_bb = pandas.read_table('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_gamgam_H2_bb_Max.tsv')
    
    print(df_H1_gamgam_H2_bb)

    mH1_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH1']]
    mH2_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH2']]
    mH3_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH3']]

    x_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['pp_X_H1_gamgam_H2_bb']]
    ObsLim_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['ObservedLimit']]


    for i in range(len(x_H1_gamgam_H2_bb)):
        if abs(mH1_H1_gamgam_H2_bb[i] - 125.09) < 10**(-10):
            ms.append(mH2_H1_gamgam_H2_bb[i])
            mx.append(mH3_H1_gamgam_H2_bb[i])
            max.append(x_H1_gamgam_H2_bb[i])
            ObsLim.append(ObsLim_H1_gamgam_H2_bb[i])
        
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
    dictToDataFrame = {'ms': ms, 'mx': mx, 'ObservedLimit': ObsLim, 'maximum': max}
    df = pandas.DataFrame(dictToDataFrame)
    df.to_csv('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_AtlasNotation.tsv', sep='\t')

    ### Find what points are excluded ###

    msExcl = []
    mxExcl = []
    ObsLimExcl = []
    maxExcl = []
    
    for i in range(len(ObsLim/max)):
        excluded = ObsLim[i]/max[i]
        if excluded < 1:
            msExcl.append(ms[i])
            mxExcl.append(mx[i])
            ObsLimExcl.append(ObsLim[i])
            maxExcl.append(max[i])

        else:
            continue
    print('printing excluded values') 
    df2 = pandas.DataFrame({'ms': np.array(msExcl), 'mx': np.array(mxExcl), 'Excl': np.array(ObsLimExcl)/np.array(maxExcl)})
    print(df2)
#    print(msExcl, mxExcl, ObsLimExcl, np.array(ObsLimExcl)/np.array(maxExcl))
    excludedScannerS = []
    excludedLimitsRatio = []
    NansInXS = []
    lenXS = []
    keys = []
    for i in range(len(ObsLimExcl)):
        pathEos = '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3' 
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
    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(pandas.DataFrame({'ms': msExcl, 'mx': mxExcl, 'ratio obs max': np.array(ObsLimExcl)/np.array(maxExcl), 'max excluded': maxExcl, 'num exclusions': excludedLimitsRatio,'num nans': NansInXS, 'num tot generated XS': lenXS, 'keys': keys}))

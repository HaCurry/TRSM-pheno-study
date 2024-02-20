import pandas
import python

if __name__ == '__main__':

    ms = []
    mx = []
    max = []
    ObsLim = []

    df_H1_bb_H2_gamgam = pandas.read_table('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_bb_H2_gamgam_Max.tsv')

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


    print(len(ms), len(mx), len(max), len())

    print('testing')

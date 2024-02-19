import pandas
import python

if __name__ == '__main__':
    df_H1_bb_H2_gamgam = pandas.read_table('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_bb_H2_gamgam_Max.tsv')

    mH1_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH1']]
    mH2_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH2']]
    mH3_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['mH3']]

    x_H1_bb_H2_gamgam = [element for element in df_H1_bb_H2_gamgam['pp_X_H1_bb_H2_gamgam']]
    
    df_H1_gamgam_H2_bb = pandas.read_table('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_gamgam_H2_bb_Max.tsv')

    mH1_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH1']]
    mH2_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH2']]
    mH3_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['mH3']]

    x_H1_gamgam_H2_bb = [element for element in df_H1_gamgam_H2_bb['pp_X_H1_gamgam_H2_bb']]

    ms = []
    mx = []
    max = []
    ObsLim = []

    for i in range(len(x_H1_bb_H2_gamgam)):
        if 
    
    print('testing')

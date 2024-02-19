import configurer as config




if __name__ == '__main__':

    # calculate each dataId
    paths = directorySearcher('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3', '/**/*_output.tsv')
    # print(paths)
    config.calculator(paths, 'bb', 'gamgam')

    # find the max for each dataId and save it in AtlasLimitsMax_max
    paths = directorySearcher('/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3', '/**/*_calculation.tsv')
    # print(paths)
    config.maxCompiler(paths, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_All_Max.tsv', 
                       'pp_X_H1H2_bbgamgam', 'pp_X_H1H1_bbgamgam', 'pp_X_H2H2_bbgamgam', 
                       limitsKey='ObservedLimit')

    config.maxCompiler(paths, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_bb_H2_gamgam_Max.tsv', 
                       'pp_X_H1_bb_H2_gamgam', 
                       limitsKey='ObservedLimit')

    config.maxCompiler(paths, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1_gamgam_H2_bb_Max.tsv', 
                       'pp_X_H1_gamgam_H2_bb', 
                       limitsKey='ObservedLimit')

    config.maxCompiler(paths, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H1H1_bbgamgam_Max.tsv', 
                       'pp_X_H1H1_bbgamgam', 
                       limitsKey='ObservedLimit')

    config.maxCompiler(paths, '/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure3/AtlasLimitsMax_H2H2_bbgamgam_Max.tsv', 
                       'pp_X_H2H2_bbgamgam', 
                       limitsKey='ObservedLimit')

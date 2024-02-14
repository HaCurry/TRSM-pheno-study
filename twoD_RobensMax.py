import pandas
import numpy as np
import twoD_MaximalXSCompile as twoDMax
import twoDPlotter as twoDPlot
import configurer as config
from parameterData import directorySearcher

if __name__ == '__main__':

    # # from comment of user user171780 in https://stackoverflow.com/a/19633103/17456342
    # df = pandas.read_table('RobensMax/RobensMaxNoDuplicates.txt', sep='\s+', usecols=[0,1,2,3], names=['index', 'ms', 'mx', 'xs'])
    # df.to_csv('RobensMax/RobensMaxNoDuplicates.tsv', sep='\t', index=False)
    # print(df)

    # indices = [index for index in df['index']]

    # # check if there are duplicates (there was previously but they are now removed hence the title NoDuplicates,
    # # the duplicates had same mass values and cross sections so nothing is lost)
    # if len(indices) > len(set(indices)):
    #     print(f"list: {len(indices)}, set: {len(set(indices))}")
    #     opt = [item for item in set(indices) if indices.count(item) > 1]
    #     print(f"duplicates: {opt}")
    #     print("Duplicates do not have different mass values nor cross sections (I have checked), \n\
    #           so this is no problem. But best is to remove them so no future issues arise.")

    # else:
    #     print('there are no duplicate rows')


    # ms = [element for element in df['ms']]
    # mx = [element for element in df['mx']]
    # XS = [element for element in df['xs']]
    # indices = [element for element in df['index']]

    # listModelTuples = []
    # for i in range(len(indices)):

    #     if 125.09 < ms[i]:
    #         listModelTuples.append((125.09, ms[i], mx[i], XS[i], indices[i]))

    #     elif ms[i] < 125.09:
    #         listModelTuples.append((ms[i], 125.09, mx[i], XS[i], indices[i]))

    #     else:
    #         raise Exception('Something went wrong')

    # print(f"\nms: {len(ms)}", f"mx: {len(mx)}", f"XS: {len(XS)}", f"indices: {len(indices)}", f"listModelTuples: {len(listModelTuples)}\n")

    # listModelParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
    #                  'mH2_lb': mH2, 'mH2_ub': mH2,
    #                  'mH3_lb': mH3, 'mH3_ub': mH3,
    #                  'thetahS_lb': -np.pi/2, 'thetahS_ub': np.pi/2, 'thetahSPoints':10,
    #                  'thetahX_lb': -np.pi/2, 'thetahX_ub': np.pi/2, 'thetahXPoints':10,
    #                  'thetaSX_lb': -np.pi/2, 'thetaSX_ub': np.pi/2, 'thetaSXPoints':10,
    #                  'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 10,
    #                  'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 10,
    #                  'extra': {'dataId': '{dataId}'.format(dataId=dataId), 'XS': XS} } for (mH1, mH2, mH3, XS, dataId) in listModelTuples]

    # twoDMax.configureDirs(listModelParams, 'RobensMax/RobensMax_configure')
    # twoDMax.condorScriptCreator('RobensMax/RobensMax_configure/scannerS.sh', 'RobensMax/RobensMax_configure/scannerS.sub', JobFlavour='testmatch')

    # use settings glob to get paths to all outputfiles and then output the results into a RobensMax_calculate 

    
    paths = directorySearcher('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/old/testMax0.9-0.04', '/**/*_output.tsv')
    print(paths)
    config.calculator(paths, 'bb', 'gamgam')

    pathsCalc = directorySearcher('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/old/testMax0.9-0.04', '/**/*_calculation.tsv')

    for path in pathsCalc:
        
        df = pandas.read_table(path)
        pp_X_H1H2_bbgamgam = np.nanmax(df['pp_X_H1H2_bbgamgam'])
        pp_X_H1_bb_H2_gamgam = np.nanmax(df['pp_X_H1_bb_H2_gamgam'])
        pp_X_H1_gamgam_H2_bb = np.nanmax(df['pp_X_H1_gamgam_H2_bb'])
        
        pp_X_H1H1_bbgamgam = np.nanmax(df['pp_X_H1H1_bbgamgam'])
        pp_X_H2H2_bbgamgam = np.nanmax(df['pp_X_H2H2_bbgamgam'])

        print('printing cross sections of file', path)
        print('$-----------------------------$')
        print('tot', pp_X_H1H2_bbgamgam)
        print('$-----------------------------$')
        print('H1->bb, H2->yy', pp_X_H1_bb_H2_gamgam)
        print('$-----------------------------$')
        print('H1->yy, H2->bb', pp_X_H1_gamgam_H2_bb)
        print('$-----------------------------$')
        print('all: {all}'.format(all=np.nanmax(df['pp_X_H1H2_bbgamgam'] + df['pp_X_H1H1_bbgamgam'] + df['pp_X_H2H2_bbgamgam'])))
        print('$-----------------------------$')
        print('# of np.nans in list XS lists, {a}, {b}, {c} '.format(a=sum(np.isnan(df['pp_X_H1H2_bbgamgam'])), b=sum(np.isnan(df['pp_X_H1_bb_H2_gamgam'])), c=sum(np.isnan(df['pp_X_H1_gamgam_H2_bb'])) ))
        print('*******************************\n')
 
    paths = directorySearcher('/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/old/testMax0.9-0.04', '/**/*_calculation.tsv')
    # print(paths)
    config.maxCompiler(paths, '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/old/testMax0.9-0.04/all_max.tsv', 
                       'pp_X_H1H2_bbgamgam', 'pp_X_H1H1_bbgamgam', 'pp_X_H2H2_bbgamgam')

    config.maxCompiler(paths, '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/old/testMax0.9-0.04/allIndividualModes_max.tsv', 
                       'pp_X_H1_bb_H2_gamgam', 'pp_X_H1_gamgam_H2_bb', 'pp_X_H1H1_bbgamgam', 'pp_X_H2H2_bbgamgam')

    config.maxCompiler(paths, '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/old/testMax0.9-0.04/H1_bb_H2_gamgam_max.tsv', 
                       'pp_X_H1_bb_H2_gamgam')

    config.maxCompiler(paths, '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/old/testMax0.9-0.04/H1_gamgam_H2_bb_max.tsv', 
                       'pp_X_H1_gamgam_H2_bb')

    config.maxCompiler(paths, '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/old/testMax0.9-0.04/H1H1_bbgamgam_max.tsv', 
                       'pp_X_H1H1_bbgamgam')

    config.maxCompiler(paths, '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/old/testMax0.9-0.04/H2H2_bbgamgam_max.tsv', 
                       'pp_X_H2H2_bbgamgam')




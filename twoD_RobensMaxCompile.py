import pandas
import numpy as np
import configurer as config

if __name__ == '__main__':

    # from comment of user user171780 in https://stackoverflow.com/a/19633103/17456342
    df = pandas.read_table('RobensMax/RobensMaxNoDuplicates.txt', sep='\s+', usecols=[0,1,2,3], names=['index', 'ms', 'mx', 'xs'])
    df.to_csv('RobensMax/RobensMaxNoDuplicates.tsv', sep='\t', index=False)
    print(df)

    indices = [index for index in df['index']]

    # check if there are duplicates (there was previously but they are now removed hence the title NoDuplicates,
    # the duplicates had same mass values and cross sections so nothing is lost)
    if len(indices) > len(set(indices)):
        print(f"list: {len(indices)}, set: {len(set(indices))}")
        opt = [item for item in set(indices) if indices.count(item) > 1]
        print(f"duplicates: {opt}")
        print("Duplicates do not have different mass values nor cross sections (I have checked), \n\
              so this is no problem. But best is to remove them so no future issues arise.")

    else:
        print('there are no duplicate rows')


    ms = [element for element in df['ms']]
    mx = [element for element in df['mx']]
    XS = [element for element in df['xs']]
    indices = [element for element in df['index']]

    listModelTuples = []
    for i in range(len(indices)):

        if 125.09 < ms[i]:
            listModelTuples.append((125.09, ms[i], mx[i], XS[i], indices[i]))

        elif ms[i] < 125.09:
            listModelTuples.append((ms[i], 125.09, mx[i], XS[i], indices[i]))

        else:
            raise Exception('Something went wrong')

    print(f"\nms: {len(ms)}", f"mx: {len(mx)}", f"XS: {len(XS)}", f"indices: {len(indices)}", f"listModelTuples: {len(listModelTuples)}\n")

    listModelParams = [{'mH1_lb': mH1, 'mH1_ub': mH1,
                     'mH2_lb': mH2, 'mH2_ub': mH2,
                     'mH3_lb': mH3, 'mH3_ub': mH3,
                     'thetahS_lb': -np.pi/2, 'thetahS_ub': np.pi/2, 'thetahSPoints':10,
                     'thetahX_lb': -np.pi/2, 'thetahX_ub': np.pi/2, 'thetahXPoints':10,
                     'thetaSX_lb': -np.pi/2, 'thetaSX_ub': np.pi/2, 'thetaSXPoints':10,
                     'vs_lb': 1, 'vs_ub': 1000, 'vsPoints': 10,
                     'vx_lb': 1, 'vx_ub': 1000, 'vxPoints': 10,
                     'extra': {'dataId': '{dataId}'.format(dataId=dataId), 'XS': XS} } for (mH1, mH2, mH3, XS, dataId) in listModelTuples]

    import os
#     os.path.abspath("mydir/myfile.txt")
# 'C:/example/cwd/mydir/myfile.txt'
    #config.configureDirs(listModelParams, 'RobensMax/RobensMax_configure3')
    #config.condorScriptCreator(os.path.abspath('RobensMax') + '/' + 'RobensMax_configure3', 
    #                            'RobensMax/RobensMax_configure3/scannerS.sh', 
    #                            'RobensMax/RobensMax_configure3/scannerS.sub', JobFlavour='testmatch')

    config.configureDirs(listModelParams, '/eos/user/i/ihaque/RobensMax/RobensMax_configure',
                         '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/RobensMaxCondor/RobensMax_configure/dataIds.txt')

    config.condorScriptCreator('/eos/user/i/ihaque/RobensMax/RobensMax_configure', 
                               '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/RobensMaxCondor/RobensMax_configure/scannerS.sh', 
                               '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/RobensMaxCondor/RobensMax_configure/scannerS.sub', 
                               '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/RobensMaxCondor/RobensMax_configure/dataIds.txt', 
                               JobFlavour='testmatch')

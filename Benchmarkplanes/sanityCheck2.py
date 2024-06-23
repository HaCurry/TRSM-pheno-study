import os

import pandas
from helpScannerS import functions as TRSM

if __name__ == '__main__':
    
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'
    path13_BP = os.path.join(pathRepo, 'Benchmarkplanes', 'BPs_noconstraints')

    # path to 13 TeV TRSM ScannerS cross sections with BP2 settings
    path13_BP2 = os.path.join(path13_BP, 'BP2', 'output_BP2_noconstraints.tsv')

    # path to 13 TeV TRSM ScannerS cross sections with BP3 settings
    path13_BP3 = os.path.join(path13_BP, 'BP3', 'output_BP3_noconstraints.tsv')

    ScannerS_BP3 = TRSM.observables(path13_BP3, 
                                    'bb', 'gamgam', 'mH1', 'mH2', 'mH3',
                                    'valid_BFB', 'valid_Higgs',
                                    'valid_STU', 'valid_Uni',
                                    kineticExclude=True)

    dfTest = pandas.read_table(path13_BP3)
    indexMan = 988

    # norm = 31.05 * 10 **(-3) * 0.002637
    norm = 1

    print('===============H1(bb), H2(gamgam)===============')

    print(dfTest['mH1'][indexMan], dfTest['mH2'][indexMan], dfTest['mH3'][indexMan],
          dfTest['x_H3_gg'][indexMan], dfTest['b_H3_H1H2'][indexMan],
          dfTest['b_H1_bb'][indexMan], dfTest['b_H2_gamgam'][indexMan])
    print(dfTest['x_H3_gg'][indexMan] * dfTest['b_H3_H1H2'][indexMan] *
          dfTest['b_H1_bb'][indexMan] * dfTest['b_H2_gamgam'][indexMan])

    print(ScannerS_BP3['mH1'][952], ScannerS_BP3['mH2'][952], ScannerS_BP3['mH3'][952])
    print(ScannerS_BP3['x_H3_H1_bb_H2_gamgam'][952] * norm)


    print('===============H1(gamgam), H2(bb)===============')

    print(dfTest['mH1'][indexMan], dfTest['mH2'][indexMan], dfTest['mH3'][indexMan],
          dfTest['x_H3_gg'][indexMan], dfTest['b_H3_H1H2'][indexMan],
          dfTest['b_H1_gamgam'][indexMan], dfTest['b_H2_bb'][indexMan])
    print(dfTest['x_H3_gg'][indexMan] * dfTest['b_H3_H1H2'][indexMan] *
          dfTest['b_H1_gamgam'][indexMan] * dfTest['b_H2_bb'][indexMan])

    print(ScannerS_BP3['mH1'][952], ScannerS_BP3['mH2'][952], ScannerS_BP3['mH3'][952])
    print(ScannerS_BP3['x_H3_H1_gamgam_H2_bb'][952] * norm)

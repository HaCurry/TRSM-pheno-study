import os
import numpy as np
import pandas
from helpScannerS import functions as TRSM

## paths

# path to repo
# E:
pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

# path to ScannerS TRSM executable output
pathBP = os.path.join(pathRepo, 'Benchmarkplanes/BPs_noconstraints/')

for BPX in ['BP2', 'BP3']: 
    path = os.path.join(pathBP, BPX, f'output_{BPX}_noconstraints.tsv')
    normSM = 1
    BPX_13 = TRSM.observables(path, 'bb', 'gamgam', 'mH1', 'mH2', 'mH3', normSM=normSM)

    row = -1

    print(f'\nDoing {BPX}:')

    print('\ncalculated with TRSM.observables')

    print(f'mH1: {BPX_13["mH1"][row]}')
    print(f'mH2: {BPX_13["mH2"][row]}')
    print(f'mH3: {BPX_13["mH3"][row]}')
    BPXbbgamgam = BPX_13["x_H3_H1_bb_H2_gamgam"][row]
    BPXgamgambb = BPX_13["x_H3_H1_gamgam_H2_bb"][row]
    print(f'\sigma(H3 -> H1(bb) H2(gamgam)): {BPXbbgamgam}')
    print(f'\sigma(H3 -> H1(gamgam) H2(bb)): {BPXgamgambb}')

    print('\ncalculated by hand')

    dfBPX = pandas.read_table(path)
    print(f'mH1: {np.array(dfBPX["mH1"])[row]}')
    print(f'mH2: {np.array(dfBPX["mH2"])[row]}')
    print(f'mH3: {np.array(dfBPX["mH3"])[row]}')

    BPXbbgamgam_byhand = np.array(dfBPX["x_H3_gg"])[row] * np.array(dfBPX["b_H3_H1H2"])[row] * np.array(dfBPX["b_H1_bb"])[row] * np.array(dfBPX["b_H2_gamgam"])[row]/normSM
    BPXgamgambb_byhand = np.array(dfBPX["x_H3_gg"])[row] * np.array(dfBPX["b_H3_H1H2"])[row] * np.array(dfBPX["b_H1_gamgam"])[row] * np.array(dfBPX["b_H2_bb"])[row]/normSM
    print(f'x_H3_gg * b_H3_H1H2 * b_H1_bb * b_H2_gamgam: {BPXbbgamgam_byhand}')
    print(f'x_H3_gg * b_H3_H1H2 * b_H1_gamgam * b_H2_bb: {BPXgamgambb_byhand}')

    print('\nchecking the difference:')
    print(f'\sigma(H3 -> H1(bb) H2(gamgam)): {BPXbbgamgam - BPXbbgamgam_byhand}')
    print(f'\sigma(H3 -> H1(gamgam) H2(bb)): {BPXgamgambb - BPXgamgambb_byhand}')

    print('==========================================')

print('Doing beyond 13 TeV')

path13_6 = os.path.join(pathRepo, 'testing/SusHi_HiggsCrossSections',
                        '13_6TeV_SusHiImprCrossSections.tsv')
path14 = os.path.join(pathRepo, 'testing/SusHi_HiggsCrossSections',
                      '14TeV_YR4CrossSections.tsv')

# E:
beyond13dict = {13.6: {'path': path13_6, 'BP2_x_HSM_gg': 5.049227246917398,
                                         'BP3_x_HSM_gg': 1.5207048620695935},
                14:   {'path': path14,   'BP2_x_HSM_gg': 5.401E+00,
                                         'BP3_x_HSM_gg': 1.636E+00}}

# E:
BPXdict = {'BP2': {'row':-1 },
           'BP3': {'row':-1}}

for keyBeyond in beyond13dict:

    print(f'Doing {keyBeyond} TeV')

    for keyBPX in BPXdict: 
        path = os.path.join(pathBP, keyBPX, f'output_{keyBPX}_noconstraints.tsv')
        normSM = 1
        BPX_13 = TRSM.observables(path, 'bb', 'gamgam', 'mH1', 'mH2', 'mH3', normSM=normSM,
                                  kineticExclude=True,
                                  pathRun3Data=beyond13dict[keyBeyond]['path'],
                                  keyCrossSecRun3='SMCrossSec')

        row = -1

        print(f'\nDoing {keyBPX}:')

        print(f'\ncalculated with TRSM.observables at {keyBeyond} TeV')

        print(f'mH1: {BPX_13["mH1"][BPXdict[keyBPX]["row"]]}')
        print(f'mH2: {BPX_13["mH2"][BPXdict[keyBPX]["row"]]}')
        print(f'mH3: {BPX_13["mH3"][BPXdict[keyBPX]["row"]]}')
        BPXbbgamgam = BPX_13["x_H3_H1_bb_H2_gamgam"][BPXdict[keyBPX]["row"]]
        BPXgamgambb = BPX_13["x_H3_H1_gamgam_H2_bb"][BPXdict[keyBPX]["row"]]
        print(f'\sigma(H3 -> H1(bb) H2(gamgam)): {BPXbbgamgam}')
        print(f'\sigma(H3 -> H1(gamgam) H2(bb)): {BPXgamgambb}')

        print(f'\ncalculated by hand at {keyBeyond} TeV')

        dfBPX = pandas.read_table(path)
        print(f'mH1: {np.array(dfBPX["mH1"])[BPXdict[keyBPX]["row"]]}')
        print(f'mH2: {np.array(dfBPX["mH2"])[BPXdict[keyBPX]["row"]]}')
        print(f'mH3: {np.array(dfBPX["mH3"])[BPXdict[keyBPX]["row"]]}')

        BPXbbgamgam_byhand = (np.array(dfBPX["R31"])[BPXdict[keyBPX]["row"]])**2 * beyond13dict[keyBeyond][f'{keyBPX}_x_HSM_gg'] * np.array(dfBPX["b_H3_H1H2"])[BPXdict[keyBPX]["row"]] * np.array(dfBPX["b_H1_bb"])[BPXdict[keyBPX]["row"]] * np.array(dfBPX["b_H2_gamgam"])[BPXdict[keyBPX]["row"]]/(normSM)
        BPXgamgambb_byhand = (np.array(dfBPX["R31"])[BPXdict[keyBPX]["row"]])**2 * beyond13dict[keyBeyond][f'{keyBPX}_x_HSM_gg'] * np.array(dfBPX["b_H3_H1H2"])[BPXdict[keyBPX]["row"]] * np.array(dfBPX["b_H1_gamgam"])[BPXdict[keyBPX]["row"]] * np.array(dfBPX["b_H2_bb"])[BPXdict[keyBPX]["row"]]/(normSM)
        print(f'x_H3_gg * b_H3_H1H2 * b_H1_bb * b_H2_gamgam: {BPXbbgamgam_byhand}')
        print(f'x_H3_gg * b_H3_H1H2 * b_H1_gamgam * b_H2_bb: {BPXgamgambb_byhand}')

        print('\nchecking the difference:')
        print(f'\sigma(H3 -> H1(bb) H2(gamgam)): {BPXbbgamgam - BPXbbgamgam_byhand}')
        print(f'\sigma(H3 -> H1(gamgam) H2(bb)): {BPXgamgambb - BPXgamgambb_byhand}')

        print('==========================================')

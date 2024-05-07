import os
import numpy as np
import pandas
from helpScannerS import functions as TRSM

## paths

# path to repo
# E:
pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

# path to ScannerS TRSM executable
path13_BP2 = os.path.join(pathRepo, 'Benchmarkplanes/BPs_noconstraints/BP2/output_BP2_noconstraints.tsv')
path13_BP3 = os.path.join(pathRepo, 'Benchmarkplanes/BPs_noconstraints/BP3/output_BP3_noconstraints.tsv')

## BP2

BP2_13 = TRSM.observables(path13_BP2, 'bb', 'gamgam', 'mH1', 'mH2', 'mH3', normSM=1)

row = -1

print('\nDoing BP2:')

print('\ncalculated with TRSM.observables')

print(f'mH1: {BP2_13["mH1"][row]}')
print(f'mH2: {BP2_13["mH2"][row]}')
print(f'mH3: {BP2_13["mH3"][row]}')
BP2bbgamgam = BP2_13["x_H3_H1_bb_H2_gamgam"][row]
BP2gamgambb = BP2_13["x_H3_H1_gamgam_H2_bb"][row]
print(f'\sigma(H3 -> H1(bb) H2(gamgam)): {BP2bbgamgam}')
print(f'\sigma(H3 -> H1(gamgam) H2(bb)): {BP2gamgambb}')

print('\ncalculated by hand')

dfBP2 = pandas.read_table(path13_BP2)
print(f'mH1: {np.array(dfBP2["mH1"])[row]}')
print(f'mH2: {np.array(dfBP2["mH2"])[row]}')
print(f'mH3: {np.array(dfBP2["mH3"])[row]}')

BP2bbgamgam_byhand = np.array(dfBP2["x_H3_gg"])[row] * np.array(dfBP2["b_H3_H1H2"])[row] * np.array(dfBP2["b_H1_bb"])[row] * np.array(dfBP2["b_H2_gamgam"])[row]
BP2gamgambb_byhand = np.array(dfBP2["x_H3_gg"])[row] * np.array(dfBP2["b_H3_H1H2"])[row] * np.array(dfBP2["b_H1_gamgam"])[row] * np.array(dfBP2["b_H2_bb"])[row]
print(f'x_H3_gg * b_H3_H1H2 * b_H1_bb * b_H2_gamgam: {BP2bbgamgam_byhand}')
print(f'x_H3_gg * b_H3_H1H2 * b_H1_gamgam * b_H2_bb: {BP2gamgambb_byhand}')

print('\nchecking the difference:')
print(f'\sigma(H3 -> H1(bb) H2(gamgam)): {BP2bbgamgam - BP2bbgamgam_byhand}')
print(f'\sigma(H3 -> H1(gamgam) H2(bb)): {BP2gamgambb - BP2gamgambb_byhand}')

print('==========================================')

## BP3

BP3_13 = TRSM.observables(path13_BP3, 'bb', 'gamgam', 'mH1', 'mH2', 'mH3', normSM=1)

row = -1

print('\nDoing BP3:')

print('\ncalculated with TRSM.observables')

print(f'mH1: {BP3_13["mH1"][row]}')
print(f'mH2: {BP3_13["mH2"][row]}')
print(f'mH3: {BP3_13["mH3"][row]}')
BP3bbgamgam = BP3_13["x_H3_H1_bb_H2_gamgam"][row]
BP3gamgambb = BP3_13["x_H3_H1_gamgam_H2_bb"][row]
print(f'\sigma(H3 -> H1(bb) H2(gamgam)): {BP3bbgamgam}')
print(f'\sigma(H3 -> H1(gamgam) H2(bb)): {BP3gamgambb}')

print('\ncalculated by hand')

dfBP3 = pandas.read_table(path13_BP3)
print(f'mH1: {np.array(dfBP3["mH1"])[row]}')
print(f'mH2: {np.array(dfBP3["mH2"])[row]}')
print(f'mH3: {np.array(dfBP3["mH3"])[row]}')

BP3bbgamgam_byhand = np.array(dfBP3["x_H3_gg"])[row] * np.array(dfBP3["b_H3_H1H2"])[row] * np.array(dfBP3["b_H1_bb"])[row] * np.array(dfBP3["b_H2_gamgam"])[row]
BP3gamgambb_byhand = np.array(dfBP3["x_H3_gg"])[row] * np.array(dfBP3["b_H3_H1H2"])[row] * np.array(dfBP3["b_H1_gamgam"])[row] * np.array(dfBP3["b_H2_bb"])[row]
print(f'x_H3_gg * b_H3_H1H2 * b_H1_bb * b_H2_gamgam: {BP3bbgamgam_byhand}')
print(f'x_H3_gg * b_H3_H1H2 * b_H1_gamgam * b_H2_bb: {BP3gamgambb_byhand}')

print('\nchecking the difference:')
print(f'\sigma(H3 -> H1(bb) H2(gamgam)): {BP3bbgamgam - BP3bbgamgam_byhand}')
print(f'\sigma(H3 -> H1(gamgam) H2(bb)): {BP3gamgambb - BP3gamgambb_byhand}')

print('==========================================')

print('\n\nCalculating at higher \sqrt{s} energies:')

print('\n')

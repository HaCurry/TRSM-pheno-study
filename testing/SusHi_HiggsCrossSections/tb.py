import pandas
import numpy as np

if __name__ == '__main__':
    df = pandas.read_table('output_testTB.tsv')
    print(f'ggF XS H1: {df["x_H1_gg"][0]}, kappa_1**2: {(df["R11"][0]**2)}')
    print(f'ggF XS H2: {df["x_H2_gg"][0]}, kappa_2**2: {(df["R21"][0]**2)}')
    print(f'ggF XS H3: {df["x_H3_gg"][0]}, kappa_3**2: {(df["R31"][0]**2)}')
    

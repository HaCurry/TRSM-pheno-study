import pandas
import numpy as np
import matplotlib.pyplot as plt

class Observables:

    ''' SM1 == SM2 is not treated '''
    
    def __init__(self, path, A, B, C, SM1, SM2, *args):
        # save arguments and create dataframe from path
        self.dataframe = pandas.read_table(path)
        self.args = args
        
        # dictCalc contains observables (XS & BRs)
        self.dictCalc = {}

        for arg in self.args:
            self.dictCalc[arg] = self.dataframe[arg]

        # A, B, C are set as the TRSM Higgs bosons H1, H2,
        # H3 by the user for the the process A -> B C
        self.A, self.B, self.C = A, B, C

        # SM1, SM2 are the Standard Model final states
        # of the particles B & C
        self.SM1, self.SM2 = SM1, SM2

    def bCalc(self):
        b_A_BC = np.array(self.dataframe[f'b_{self.A}_{self.B}{self.C}'])
        b_B_SM1 = np.array(self.dataframe[f'b_{self.B}_{self.SM1}'])
        b_B_SM2 = np.array(self.dataframe[f'b_{self.B}_{self.SM2}'])
        b_C_SM1 = np.array(self.dataframe[f'b_{self.C}_{self.SM1}'])
        b_C_SM2 = np.array(self.dataframe[f'b_{self.C}_{self.SM2}'])

        self.key_b_A_BC = f'b_{self.A}_{self.B}{self.C}'
        self.dictCalc[self.key_b_A_BC] = b_A_BC

        self.key_f_b_A_B_SM1_C_SM2 = f'b_{self.A}_{self.B}_{self.SM1}_{self.C}_{self.SM2}'
        self.dictCalc[self.key_f_b_A_B_SM1_C_SM2] = b_A_BC * (b_B_SM1 * b_C_SM2)

        self.key_b_A_B_SM2_C_SM1 = f'b_{self.A}_{self.B}_{self.SM2}_{self.C}_{self.SM1}'
        self.dictCalc[self.key_b_A_B_SM2_C_SM1] = b_A_BC * (b_B_SM2 * b_C_SM1)

        self.key_b_A_BC_SM1SM2 = f'b_{self.A}_{self.B}{self.C}_{self.SM1}{self.SM2}'
        self.dictCalc[self.key_b_A_BC_SM1SM2] = b_A_BC * (b_B_SM1 * b_C_SM2 
                                                          + b_B_SM2 * b_C_SM1)

    def xCalc(self, **kwargs):
        if 'prodMode' in kwargs:
            prodMode = kwargs['prodMode']

        else: prodMode = 'gg'

        # check if branching ratios are calculated
        if (f'b_{self.A}_{self.B}{self.C}' in self.dictCalc and
        f'b_{self.A}_{self.B}_{self.SM1}_{self.C}_{self.SM2}' in self.dictCalc and
        f'b_{self.A}_{self.B}_{self.SM2}_{self.C}_{self.SM1}' in self.dictCalc and
        f'b_{self.A}_{self.B}{self.C}_{self.SM1}{self.SM2}' in self.dictCalc):
            pass

        # otherwise calculate branching ratios for
        # calculating cross sections
        else:
            self.bCalc()


        self.dictCalc[f'x_{self.A}_{prodMode}'] = np.array(self.dataframe[f'x_{self.A}_{prodMode}'])
        self.dictCalc[f'x_{self.B}_{prodMode}'] = np.array(self.dataframe[f'x_{self.B}_{prodMode}'])
        self.dictCalc[f'x_{self.C}_{prodMode}'] = np.array(self.dataframe[f'x_{self.C}_{prodMode}'])

        self.dictCalc[f'x_{self.A}_{self.B}{self.C}'] = (self.dictCalc[f'x_{self.A}_{prodMode}'] 
            * self.dictCalc[f'b_{self.A}_{self.B}{self.C}']) 

        self.dictCalc[f'x_{self.A}_{self.B}_{self.SM1}_{self.C}_{self.SM2}'] = (self.dictCalc[f'x_{self.A}_{prodMode}'] 
            * self.dictCalc[f'b_{self.A}_{self.B}_{self.SM1}_{self.C}_{self.SM2}'])

        self.dictCalc[f'x_{self.A}_{self.B}_{self.SM2}_{self.C}_{self.SM1}'] = (self.dictCalc[f'x_{self.A}_{prodMode}'] 
            * self.dictCalc[f'b_{self.A}_{self.B}_{self.SM2}_{self.C}_{self.SM1}'])

        self.dictCalc[f'x_{self.A}_{self.B}{self.C}_{self.SM1}{self.SM2}'] = (self.dictCalc[f'x_{self.A}_{prodMode}'] 
            * self.dictCalc[f'b_{self.A}_{self.B}{self.C}_{self.SM1}{self.SM2}'])


if __name__ == '__main__':

    test = Observables(
                       'plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv',
                       'H3', 'H1', 'H2', 'bb', 'gamgam',
                       'mH1', 'mH2', 'mH3', 'thetahS', 'thetahX', 'thetaSX', 'vs', 'vx',
                       )

    test.xCalc()

    print(test.dictCalc['x_H3_H1_bb_H2_gamgam'][0:100])


    # test.bCalc('H3', 'H1', 'H2', 'bb', 'gamgam')
    # mH1 = test.b_NPSM['mH1']
    # mH3 = test.b_NPSM['mH3']
    # b_H3_H1H2_bbgamgam = test.b_NPSM['b_H3_H1H2_bbgamgam']

    # print(len(mH1))
    # print(len(mH3))
    # print((b_H3_H1H2_bbgamgam))
    plt.scatter(test.dictCalc['mH1'], test.dictCalc['mH3'], c=test.dictCalc['x_H3_H1_bb_H2_gamgam'])
    plt.show()

    # test.bCalc('H3', 'H1', 'H2', 'bb', 'gamgam').xCalc()
    # x_H3_H1H2_bbgamgam = test.dictCalc['x_H3_H1H2_bbgamgam']
    # mH1 = test.dictCalc['mH1']
    # mH3 = test.dictCalc['mH3']
    # x_H3_H1H2_bbgamgam = test.dictCalc['x_H3_H1H2_bbgamgam']

    # print(test.dictCalc.keys())

    # print(len(mH1))
    # print(len(mH3))
    # print((x_H3_H1H2_bbgamgam))
    # plt.scatter(mH1, mH3, c=x_H3_H1H2_bbgamgam)
    # plt.show()

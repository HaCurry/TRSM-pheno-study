import pandas
import numpy as np
import matplotlib.pyplot as plt

class Observables:

    ''' SM1 == SM2 is not treated '''
    
    def __init__(self, path, *args):
        # save arguments and create dataframe from path
        self.dataframe = pandas.read_table(path)
        self.args = args
        
        # dictCalc contains observables (XS & BRs)
        self.dictCalc = {}

        # A, B, C are the TRSM Higgs bosons H1, H2, H3
        # input by the user where in the process A -> B C
        self.A, self.B, self.C = None, None, None

        # SM1, SM2 are the Standard Model final states
        # of the particles B & C
        self.SM1, self.SM2 = None, None

    def bCalc(self, A, B, C, SM1, SM2):
        b_A_BC = np.array(self.dataframe[f'b_{A}_{B}{C}'])
        b_B_SM1 = np.array(self.dataframe[f'b_{B}_{SM1}'])
        b_B_SM2 = np.array(self.dataframe[f'b_{B}_{SM2}'])
        b_C_SM1 = np.array(self.dataframe[f'b_{C}_{SM1}'])
        b_C_SM2 = np.array(self.dataframe[f'b_{C}_{SM2}'])

        self.dictCalc[f'b_{A}_{B}{C}'] = b_A_BC
        self.dictCalc[f'b_{A}_{B}_{SM1}_{C}_{SM2}'] = b_A_BC * (b_B_SM1 * b_C_SM2)
        self.dictCalc[f'b_{A}_{B}_{SM2}_{C}_{SM1}'] = b_A_BC * (b_B_SM2 * b_C_SM1)
        self.dictCalc[f'b_{A}_{B}{C}_{SM1}{SM2}'] = b_A_BC * (b_B_SM1 * b_C_SM2 
                                                          + b_B_SM2 * b_C_SM1)

        for arg in self.args:
            self.dictCalc[arg] = self.dataframe[arg]

    def xCalc(self, **kwargs):

        if 'prodMode' in kwargs:
            prodMode = kwargs['prodMode']

        else: prodMode = 'gg'

        self.dictCalc[f'x_{self.A}_{prodMode}'] = self.dataframe[f'x_{self.A}_{prodMode}']
        self.dictCalc[f'x_{self.B}_{prodMode}'] = self.dataframe[f'x_{self.B}_{prodMode}']
        self.dictCalc[f'x_{self.C}_{prodMode}'] = self.dataframe[f'x_{self.C}_{prodMode}']

        self.dictCalc[f'x_{self.A}_{self.B}{self.C}'] = (self.dictCalc[f'x_{self.A}_{prodMode}'] 
            * self.dictCalc[f'b_{self.A}_{self.B}{self.C}']) 

        self.dictCalc[f'x_{self.A}_{self.B}_{self.SM1}_{self.C}_{self.SM2}'] = (self.dataframe[f'x_{self.A}_{prodMode}'] 
            * self.dictCalc[f'b_{self.A}_{self.B}_{self.SM1}_{self.C}_{self.SM2}'])

        self.dictCalc[f'x_{self.A}_{self.B}_{self.SM2}_{self.C}_{self.SM1}'] = (self.dataframe[f'x_{self.A}_{prodMode}'] 
            * self.dictCalc[f'b_{self.A}_{self.B}_{self.SM2}_{self.C}_{self.SM1}'])

        self.dictCalc[f'x_{self.A}_{self.B}{self.C}_{self.SM1}{self.SM2}'] = (self.dataframe[f'x_{self.A}_{prodMode}'] 
            * self.dictCalc[f'b_{self.A}_{self.B}{self.C}_{self.SM1}{self.SM2}'])


if __name__ == '__main__':

    test = Observables('plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 'mH1', 'mH3', 'thetahS', 'thetahX', 'thetaSX', 'vs', 'vx')

    # test.bCalc('H3', 'H1', 'H2', 'bb', 'gamgam')
    # mH1 = test.b_NPSM['mH1']
    # mH3 = test.b_NPSM['mH3']
    # b_H3_H1H2_bbgamgam = test.b_NPSM['b_H3_H1H2_bbgamgam']

    # print(len(mH1))
    # print(len(mH3))
    # print((b_H3_H1H2_bbgamgam))
    # plt.scatter(mH1, mH3, c=b_H3_H1H2_bbgamgam)
    # plt.show()


    test.bCalc('H3', 'H1', 'H2', 'bb', 'gamgam').xCalc()
    x_H3_H1H2_bbgamgam = test.dictCalc['x_H3_H1H2_bbgamgam']
    mH1 = test.dictCalc['mH1']
    mH3 = test.dictCalc['mH3']
    x_H3_H1H2_bbgamgam = test.dictCalc['x_H3_H1H2_bbgamgam']

    print(test.dictCalc.keys())

    print(len(mH1))
    print(len(mH3))
    print((x_H3_H1H2_bbgamgam))
    plt.scatter(mH1, mH3, c=x_H3_H1H2_bbgamgam)
    plt.show()

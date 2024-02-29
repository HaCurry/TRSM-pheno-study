#!/usr/bin/python3 python3
import configurer as config
import functions

import os
import subprocess

import numpy as np
import pandas

if __name__ == '__main__':

    def TRSM(mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, SM1, SM2, mode, pathTRSM, pathOutput, **kwargs):

        ####################### kwargs #######################

        if 'BFB' in kwargs:
            BFB = kwargs['BFB']

        else: BFB = 1

        if 'Uni' in kwargs:
            Uni = kwargs['Uni']

        else: Uni = 1

        if 'STU' in kwargs:
            STU = kwargs['STU']

        else: STU = 1

        if 'Higgs' in kwargs:
            Higgs = kwargs['Higgs']

        else: Higgs = 1

        ######################################################

        dictModelParams = {'mH1_lb': mH1, 'mH1_ub': mH1,
                           'mH2_lb': mH2, 'mH2_ub': mH2,
                           'mH3_lb': mH3, 'mH3_ub': mH3,
                           'thetahS_lb': thetahS, 'thetahS_ub': thetahS,
                           'thetahX_lb': thetahX, 'thetahX_ub': thetahX,
                           'thetaSX_lb': thetaSX, 'thetaSX_ub': thetaSX,
                           'vs_lb': vs, 'vs_ub': vs,
                           'vx_lb': vx, 'vx_ub': vx}

        dataId = f'mH1{mH1}_mH2{mH2}_mH3{mH3}'
        pathExecutionConfig = os.path.join(pathOutput, f'config_{dataId}.tsv')
        pathExecutionOutput = os.path.join(pathOutput, f'output_{dataId}.tsv')

        config.checkCreatorNew(pathExecutionConfig, dictModelParams)
        runTRSM = [pathTRSM, '--BFB', str(BFB), '--Uni', str(Uni), '--STU', str(STU), '--Higgs', str(Higgs), pathExecutionOutput, 'check', pathExecutionConfig]

        shell_output = subprocess.run(runTRSM, cwd=pathOutput)

        try:
            H1H2, H1H1, H2H2 = functions.ppXNPSM_massfree(pathExecutionOutput, 'mH1', 'mH2', 'mH3',  SM1, SM2,  normalizationSM=1)
            returnValue = (H1H2[mode])[0]
        except pandas.errors.EmptyDataError:
            returnValue = (0)

        return returnValue

    def wrapInputBayesianOpt(mH1, mH2, mH3, SM1, SM2, mode, pathTRSM, pathOutput, BFB, Uni, STU, Higgs):
        def inputBayesianOpt(thetahS, thetahX, thetaSX, vs, vx):
            return TRSM(mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, SM1, SM2, mode, pathTRSM, pathOutput, BFB=BFB, Uni=Uni, STU=STU, Higgs=Higgs)
        return inputBayesianOpt

    from bayes_opt import BayesianOptimization
    from bayes_opt import UtilityFunction
    mH1 = 90
    mH2 = 125.09
    mH3 = 500
    BFB, Uni, STU, Higgs = 1, 1, 1, 1
    SM1, SM2 = 'bb', 'gamgam'
    mode = 4
    black_box_function = wrapInputBayesianOpt(mH1, mH2, mH3, SM1, SM2, mode,
                                              '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken', 
                                              '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt',
                                              BFB, Uni, STU, Higgs)

    # Bounded region of parameter space
    pbounds = {'thetahS': (-np.pi/2, np.pi/2), 'thetahX': (-np.pi/2, np.pi/2), 'thetaSX': (-np.pi/2, np.pi/2), 
               'vs': (1, 1000), 'vx': (1, 1000)}

    # def black_box_function(x, y):
    #    """Function with unknown internals we wish to maximize.
    #
    #    This is just serving as an example, for all intents and
    #    purposes think of the internals of this function, i.e.: the process
    #    which generates its output values, as unknown.
    #    """
    #     return -x ** 2 - (y - 1) ** 2 + 1

    # pbounds = {'x': (2, 4), 'y': (-3, 3)}

    optimizer = BayesianOptimization(
        f=black_box_function,
        pbounds=pbounds,
        random_state=1,
        verbose=0,
        allow_duplicate_points=True
    )

    init_points = 25 
    n_iter = 2000
    kind = "ucb"
    kappa=10
    xi='default'

    print(f'running n_iter = {n_iter}, init_points = {init_points}, kind = {kind}, kappa = {kappa}, xi = {xi}')
    acquisition_function = UtilityFunction(kind=kind)    
    optimizer.maximize(
        init_points=init_points,
        n_iter=n_iter,
        acquisition_function=acquisition_function
    )

    BayOutput = (optimizer.max)

    BayOutput['params']['mH1'] = mH1
    BayOutput['params']['mH2'] = mH2
    BayOutput['params']['mH3'] = mH3
    BayOutput['params']['BFB'] = BFB
    BayOutput['params']['Uni'] = Uni
    BayOutput['params']['STU'] = STU
    BayOutput['params']['Higgs'] = Higgs
    BayOutput['params']['mode'] = mode

    print(BayOutput)

    BayOutputToJson = {'BayOutput': BayOutput, 'init_points': init_points, 'n_iter': n_iter, 'kind': kind, 'kappa': kappa, 'xi':xi}

    import json
    with open("/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt/BayOptOutput.json", "a") as outfile: 
        json.dump(BayOutputToJson, outfile, indent=4)
    
    # clear the file
    with open(f'/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt/{mH1}_{mH2}_{mH3}.tsv', 'w') as logs:
        pass
    
    # save iterations
    with open(f'/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt/{mH1}_{mH2}_{mH3}.tsv', 'a') as logs:
        logs.write('iteration\ttarget\tthetahS\tthetahX\tthetaSX\tvs\tvx\n')
        for i, res in enumerate(optimizer.res):
            #logs.write(f"Iteration {i}: \n\t{res}\n")
            logs.write(f'{i}\t{res["target"]}\t{res["params"]["thetahS"]}\t{res["params"]["thetahX"]}\t{res["params"]["thetaSX"]}\t{res["params"]["vs"]}\t{res["params"]["vx"]}\n')

    #df = pandas.read_table(f'/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt/{mH1}_{mH2}_{mH3}.tsv')
    #import matplotlib.pyplot as plt
    #plt.plot(np.array(df['iteration']), np.array(df['target']), marker='o')
    #plt.yscale('log')
    #plt.savefig('/eos/user/i/ihaque/bayesianOptPlots/test.pdf')
    
    

#!/usr/bin/python3 python3
import configurer as config
import functions

import os
import subprocess

import numpy as np
import pandas

from scipy.optimize import NonlinearConstraint

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
        
        # input parameters
        dictModelParams = {'mH1_lb': mH1, 'mH1_ub': mH1,
                           'mH2_lb': mH2, 'mH2_ub': mH2,
                           'mH3_lb': mH3, 'mH3_ub': mH3,
                           'thetahS_lb': thetahS, 'thetahS_ub': thetahS,
                           'thetahX_lb': thetahX, 'thetahX_ub': thetahX,
                           'thetaSX_lb': thetaSX, 'thetaSX_ub': thetaSX,
                           'vs_lb': vs, 'vs_ub': vs,
                           'vx_lb': vx, 'vx_ub': vx}

        # some temporary files needed for the executable below
        dataId = f'mH1{mH1}_mH2{mH2}_mH3{mH3}'
        pathExecutionConfig = os.path.join(pathOutput, f'x_config_{dataId}.tsv')
        pathExecutionOutput = os.path.join(pathOutput, f'x_output_{dataId}.tsv')
        
        # creates contents of pathExecutionConfig
        config.checkCreatorNew(pathExecutionConfig, dictModelParams)

        # for subprocesses.run below
        runTRSM = [pathTRSM, '--BFB', str(BFB), '--Uni', str(Uni), '--STU', str(STU), '--Higgs', str(Higgs), pathExecutionOutput, 'check', pathExecutionConfig]
        print('BFB,Uni,STU,Higgs:', BFB, Uni, STU, Higgs)
        # run the executable
        shell_output = subprocess.run(runTRSM, cwd=pathOutput)

        # calculate physical observables from the output from the executable (pathExecutionOutput)
        try:
            H1H2, H1H1, H2H2 = functions.ppXNPSM_massfree(pathExecutionOutput, 'mH1', 'mH2', 'mH3',  SM1, SM2,  normalizationSM=1)
            returnValue = (H1H2[mode])[0]
        
        except pandas.errors.EmptyDataError:
            returnValue = 0
        
        # Sometimes the output is very small values such that it cannot represent them as floats, hence return as 0.
        if np.isnan(returnValue):
            returnValue = 0

        else: pass
        
        print(-returnValue) 
        return -returnValue

    # def constraintTRSM(mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, SM1, SM2, mode, pathTRSM, pathOutput):
    #      
    #     dictModelParams = {'mH1_lb': mH1, 'mH1_ub': mH1,
    #                        'mH2_lb': mH2, 'mH2_ub': mH2,
    #                        'mH3_lb': mH3, 'mH3_ub': mH3,
    #                        'thetahS_lb': thetahS, 'thetahS_ub': thetahS,
    #                        'thetahX_lb': thetahX, 'thetahX_ub': thetahX,
    #                        'thetaSX_lb': thetaSX, 'thetaSX_ub': thetaSX,
    #                        'vs_lb': vs, 'vs_ub': vs,
    #                        'vx_lb': vx, 'vx_ub': vx}

    #     dataId = f'mH1{mH1}_mH2{mH2}_mH3{mH3}'
    #     pathExecutionConfig = os.path.join(pathOutput, f'x_constraint_config_{dataId}.tsv')
    #     pathExecutionOutput = os.path.join(pathOutput, f'x_constraint_output_{dataId}.tsv')

    #     config.checkCreatorNew(pathExecutionConfig, dictModelParams)
    #     runTRSM = [pathTRSM, '--BFB', '1', '--Uni', '1', '--STU', '1', '--Higgs', '1', pathExecutionOutput, 'check', pathExecutionConfig]
    #     
    #     shell_output = subprocess.run(runTRSM, cwd=pathOutput)

    #     try:
    #         # if returnvalue == 1, then model parameters pass the constraints
    #         H1H2, H1H1, H2H2 = functions.ppXNPSM_massfree(pathExecutionOutput, 'mH1', 'mH2', 'mH3',  SM1, SM2,  normalizationSM=1)
    #         returnValue = 1

    #     # if outputfile (pathExecutionOutput) is empty, the parameters do not pass the constraints
    #     except pandas.errors.EmptyDataError:
    #         # if returnValue == -1, then model parameters fail constraints
    #         returnValue = -1
    #     
    #     print(returnValue)
    #     return returnValue
        

    # we do not want to optimize mH1, mH2, mH3 and SM1, SM2, pathTRSM, pathOutput are strings required for TRSM
    def wrapInputBayesianOpt(mH1, mH2, mH3, SM1, SM2, mode, pathTRSM, pathOutput):
        def inputBayesianOpt(thetahS, thetahX, thetaSX, vs, vx):
            return TRSM(mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, SM1, SM2, mode, pathTRSM, pathOutput)
        return inputBayesianOpt

    # def wrapInputBayesianOptConstraint(mH1, mH2, mH3, SM1, SM2, mode, pathTRSM, pathOutput):
    #     def inputBayesianOptConstraint(thetahS, thetahX, thetaSX, vs, vx):
    #         return constraintTRSM(mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, SM1, SM2, mode, pathTRSM, pathOutput)
    #     return inputBayesianOptConstraint

    mH1 = 90
    mH2 = 125.09
    mH3 = 500
    SM1, SM2 = 'bb', 'gamgam'
    mode = 4

    black_box_function = wrapInputBayesianOpt(mH1, mH2, mH3, SM1, SM2, mode,
                                              '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken', 
                                              '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt')
    
    # black_box_constraint = wrapInputBayesianOptConstraint(mH1, mH2, mH3, SM1, SM2, mode,
    #                                           '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken', 
    #                                           '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt')    
    
    # Bounded region of parameter space
    pbounds = {'thetahS': (-np.pi/2, np.pi/2), 'thetahX': (-np.pi/2, np.pi/2), 'thetaSX': (-np.pi/2, np.pi/2), 
               'vs': (1, 1000), 'vx': (1, 1000)}

    import dlib

    #thetahS, thetahX, thetaSX, vs, vx = dlib.find_min_global(black_box_function,
    x, y = dlib.find_min_global(black_box_function,
[-np.pi/2, -np.pi/2, -np.pi/2, 1, 1],
[np.pi/2, np.pi/2, np.pi/2, 1000, 1000],
100)

    print(f'optimal inputs: {x}')
    print(f'optimal output: {y}')


    # IGNORE BELOW, WRITES OUTPUT FROM optimizer.max INTO A .json FILE AND ITERATIONS IN A .tsv FILE

    # from datetime import datetime
    # currentTime = datetime.now() 

    # BayOutput['params']['mH1'] = mH1
    # BayOutput['params']['mH2'] = mH2
    # BayOutput['params']['mH3'] = mH3
    # BayOutput['params']['mode'] = mode

    # BayOutputToJson = {'BayOutput': BayOutput, 'init_points': init_points, 'n_iter': n_iter, 'kind': kind, 'kappa': kappa, 'xi':xi, 'date': str(currentTime)}
    # 
    # print(BayOutputToJson)

    # import json
    # # save settings used in BayesianOptimization and optimizer.maximize and other useful info
    # with open("/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt/x_BayOptOutput.json", "a") as outfile: 
    #     json.dump(BayOutputToJson, outfile, indent=4)
    # 
    # # clear old contents of iteration file
    # # with open(f'/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt/iterations/x_{mH1}_{mH2}_{mH3}.tsv', 'w') as logs:
    # #     pass

    # # save iterations
    # with open(f'/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt/iterations/x_{mH1}_{mH2}_{mH3}_{str(currentTime)}.tsv', 'a') as logs:
    #     logs.write('iteration\ttarget\tmH1\tmH2\tmH3\tthetahS\tthetahX\tthetaSX\tvs\tvx\n')
    #     for i, res in enumerate(optimizer.res):
    #        #logs.write(f"Iteration {i}: \n\t{res}\n")
    #         logs.write(f'{i}\t{res["target"]}\t{BayOutput["params"]["mH1"]}\t{BayOutput["params"]["mH2"]}\t{BayOutput["params"]["mH3"]}\t{res["params"]["thetahS"]}\t{res["params"]["thetahX"]}\t{res["params"]["thetaSX"]}\t{res["params"]["vs"]}\t{res["params"]["vx"]}\n')

























































    

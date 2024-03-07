import configurer as config
import functions

import os
import subprocess
import argparse
import json
import datetime

import numpy as np
import pandas
from scipy.optimize import NonlinearConstraint
import matplotlib.pyplot as plt

from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        prog='ProgramName',
                        description='What the program does',
                        epilog='Text at the bottom of help')

    parser.add_argument('-mS', '--massS', type=float)
    parser.add_argument('-mX', '--massX', type=float)
    
    parser.add_argument('-SM1', '--SM1', type=str, default='bb')
    parser.add_argument('-SM2', '--SM2', type=str, default='gamgam')

    parser.add_argument('-o', '--pathOutput', type=str)
    parser.add_argument('-e', '--pathExecutable', type=str)
    parser.add_argument('-d', '--dataId', default=None)

    parser.add_argument('-init', '--initial', type=int, default=25)
    parser.add_argument('-iter', '--iterations', type=int, default=100)
    parser.add_argument('-kind', '--kind', type=str, default='ucb')

    parser.add_argument('-kappa', '--kappa', type=float, default=2.576)
    parser.add_argument('-xi', '--xi', type=float, default=0)
    
    args = parser.parse_args()

    mS = args.massS
    mX = args.massX

    SM1 = args.SM1
    SM2 = args.SM2

    pathOutput = args.pathOutput
    pathExecutable = args.pathExecutable
    dataId = args.dataId

    init_points = args.initial 
    n_iter = args.iterations
    kind = args.kind

    kappa = args.kappa
    xi = args.xi
    
    def runExecutableTRSM(mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, SM1, SM2, mode, pathTRSM, pathOutput, **kwargs):

        ####################### kwargs #######################

        if 'BFB' in kwargs:
            BFB = kwargs['BFB']

        else: BFB = 0

        if 'Uni' in kwargs:
            Uni = kwargs['Uni']

        else: Uni = 0

        if 'STU' in kwargs:
            STU = kwargs['STU']

        else: STU = 0

        if 'Higgs' in kwargs:
            Higgs = kwargs['Higgs']

        else: Higgs = 0

        ######################################################

        dictModelParams = {'mH1_lb': mH1, 'mH1_ub': mH1,
                           'mH2_lb': mH2, 'mH2_ub': mH2,
                           'mH3_lb': mH3, 'mH3_ub': mH3,
                           'thetahS_lb': thetahS, 'thetahS_ub': thetahS,
                           'thetahX_lb': thetahX, 'thetahX_ub': thetahX,
                           'thetaSX_lb': thetaSX, 'thetaSX_ub': thetaSX,
                           'vs_lb': vs, 'vs_ub': vs,
                           'vx_lb': vx, 'vx_ub': vx}

        dataId = f'{mH1}_{mH2}_{mH3}'
        pathExecutionConfig = os.path.join(pathOutput, f'temp_config_{dataId}.tsv')
        pathExecutionOutput = os.path.join(pathOutput, f'temp_output_{dataId}.tsv')

        config.checkCreatorNew(pathExecutionConfig, dictModelParams)
        runTRSM = [pathTRSM, '--BFB', str(BFB), '--Uni', str(Uni), '--STU', str(STU), '--Higgs', str(Higgs), pathExecutionOutput, 'check', pathExecutionConfig]

        shell_output = subprocess.run(runTRSM, cwd=pathOutput)

        H1H2, H1H1, H2H2 = functions.ppXNPSM_massfree(pathExecutionOutput, 'mH1', 'mH2', 'mH3',  SM1, SM2,  normalizationSM=1)
        returnValue = (H1H2[mode])[0]
        
        if np.isnan(returnValue):
            returnValue = 0

        else: pass
        
        print(f'returnvalue: {returnValue}')
        return returnValue


    def runConstraintExecutableTRSM(mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, SM1, SM2, mode, pathTRSM, pathOutput):
         
        dictModelParams = {'mH1_lb': mH1, 'mH1_ub': mH1,
                           'mH2_lb': mH2, 'mH2_ub': mH2,
                           'mH3_lb': mH3, 'mH3_ub': mH3,
                           'thetahS_lb': thetahS, 'thetahS_ub': thetahS,
                           'thetahX_lb': thetahX, 'thetahX_ub': thetahX,
                           'thetaSX_lb': thetaSX, 'thetaSX_ub': thetaSX,
                           'vs_lb': vs, 'vs_ub': vs,
                           'vx_lb': vx, 'vx_ub': vx}

        dataId = f'{mH1}_{mH2}_{mH3}'
        pathExecutionConfig = os.path.join(pathOutput, f'temp_constraint_config_{dataId}.tsv')
        pathExecutionOutput = os.path.join(pathOutput, f'temp_constraint_output_{dataId}.tsv')

        config.checkCreatorNew(pathExecutionConfig, dictModelParams)
        runTRSM = [pathTRSM, '--BFB', '1', '--Uni', '1', '--STU', '1', '--Higgs', '1', pathExecutionOutput, 'check', pathExecutionConfig]
        
        shell_output = subprocess.run(runTRSM, cwd=pathOutput)

        try:
            # if returnvalue == 1, then model parameters pass the constraints
            H1H2, H1H1, H2H2 = functions.ppXNPSM_massfree(pathExecutionOutput, 'mH1', 'mH2', 'mH3',  SM1, SM2,  normalizationSM=1)
            returnValue = 1

        # if outputfile (pathExecutionOutput) is empty, the parameters do not pass the constraints
        except pandas.errors.EmptyDataError:
            # if returnValue == -1, then model parameters fail constraints
            returnValue = -1
        
        print(f'returnvalue: {returnValue}')
        return returnValue
 


    def wrapInputBayesianOpt(mH1, mH2, mH3, SM1, SM2, mode, pathTRSM, pathOutput):
        def TRSM(thetahS, thetahX, thetaSX, vs, vx):
            return runExecutableTRSM(mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, SM1, SM2, mode, pathTRSM, pathOutput)
        return TRSM

    def wrapInputBayesianOptConstraint(mH1, mH2, mH3, SM1, SM2, mode, pathTRSM, pathOutput):
        def constraintTRSM(thetahS, thetahX, thetaSX, vs, vx):
            return runConstraintExecutableTRSM(mH1, mH2, mH3, thetahS, thetahX, thetaSX, vs, vx, SM1, SM2, mode, pathTRSM, pathOutput)
        return constraintTRSM

    # set mass hierarchy
    if mS < 125.09:
        mH1 = mS
        mH2 = 125.09
        mH3 = mX
        
        # S(bb) H(gamgam)
        mode = 4

    elif 125.09 < mS:
        mH1 = 125.09
        mH2 = mS
        mH3 = mX

        # S(bb) H(gamgam)
        mode = 5
    
    elif mS == 125.09:
        mH1 = 125.09
        mH2 = 125.09
        mH3 = mX

    else:
        raise Exception(f'Something went wrong, is {mS}, {mX} correct?')

    # create directory
    if dataId is None:
        dataId = f'{mH1}_{mH2}_{mH3}'

    else:
        pass
    
    # where all the output will be saved
    pathOutputDataId = os.path.join(pathOutput, dataId)
 
    # this will raise error if directory pathOutput/dataId already exists
    os.makedirs(pathOutputDataId) 
    optimizeFunction = wrapInputBayesianOpt(mH1, mH2, mH3, SM1, SM2, mode,
                                              pathExecutable, 
                                              pathOutputDataId)
    
    constraint = wrapInputBayesianOptConstraint(mH1, mH2, mH3, SM1, SM2, mode,
                                              pathExecutable,
                                              pathOutputDataId)    
    
    optimizeConstraint = NonlinearConstraint(constraint, 0, np.inf)

    # Bounded region of parameter space
    pbounds = {'thetahS': (-np.pi/2, np.pi/2), 'thetahX': (-np.pi/2, np.pi/2), 'thetaSX': (-np.pi/2, np.pi/2), 
               'vs': (1, 1000), 'vx': (1, 1000)}
    
    optimizer = BayesianOptimization(
        f=optimizeFunction,
        constraint=optimizeConstraint,
        pbounds=pbounds,
        random_state=1,
        verbose=0,
        allow_duplicate_points=True,
    )
    
    print(optimizer) 
    print(f'running n_iter = {n_iter}, init_points = {init_points}, kind = {kind}, kappa = {kappa}, xi = {xi}')
    print(kind, kappa, xi, init_points, n_iter)
    #acquisition_function = UtilityFunction(kind=kind, kappa=kappa, xi=xi)    
    optimizer.maximize(
        init_points=init_points,
        n_iter=n_iter,
        #acquisition_function=acquisition_function
    )
    
    # start optimization, BayOutput is a dict with info about the optimization run
    BayOptMetaData = optimizer.max 
   

    # append additional information about the run in BayOutput for saving as a .json file
    BayOptMetaData['params']['mH1'] = mH1
    BayOptMetaData['params']['mH2'] = mH2
    BayOptMetaData['params']['mH3'] = mH3
    BayOptMetaData['params']['mode'] = mode

    BayOptMetaData['optimizationSettings'] = {'init_points': init_points, 'n_iter': n_iter, 'kind': kind, 'kappa': kappa, 'xi':xi}
   
    print(BayOptMetaData)
    
    # save BayOptMetaData as a .json
    pathJSON = os.path.join(pathOutputDataId, f'settings_{dataId}.json') 
    with open(pathJSON, 'w') as outfile: 
        json.dump(BayOptMetaData, outfile, indent=4)
    
    # save the iterations from Bayesian Optimization in a dict
    iterations = {}

    iterations['iteration'] = []
    iterations['target'] = []
    iterations['constraint'] = []

    iterations['mH1'] = []
    iterations['mH2'] = []
    iterations['mH3'] = []
    iterations['thetahS'] = []
    iterations['thetahX'] = []
    iterations['thetaSX'] = []
    iterations['vs'] = []
    iterations['vx'] = []

    for i, res in enumerate(optimizer.res):
        iterations['iteration'].append(i)
        iterations['target'].append(res['target'])
        iterations['constraint'].append(res['constraint'])

        iterations['mH1'].append(BayOptMetaData['params']['mH1'])
        iterations['mH2'].append(BayOptMetaData['params']['mH2'])
        iterations['mH3'].append(BayOptMetaData['params']['mH3'])

        iterations['thetahS'].append(res['params']['thetahS'])
        iterations['thetahX'].append(res['params']['thetahX'])
        iterations['thetaSX'].append(res['params']['thetaSX'])
        iterations['vs'].append(res['params']['vs'])
        iterations['vx'].append(res['params']['vx'])
    
    # save iterations from Bayesian Optimization in a .tsv file
    df = pandas.DataFrame(iterations)
    pathTSV = os.path.join(pathOutputDataId, f'iterations_{dataId}.tsv')
    df.to_csv(pathTSV, index=False)

    # plot iterations
    allowedTarget = []
    allowedIter = []
    disallowedTarget = []
    disallowedIter = []

    for i in range(len(df)):
        if df['constraint'][i] == 1:
            allowedTarget.append(df['target'][i])
            allowedIter.append(df['iteration'][i])

        elif df['constraint'][i] == -1:        
            disallowedTarget.append(df['target'][i])
            disallowedIter.append(df['iteration'][i])

        else:
            raise Exception('Something went wrong...')

    currentDate = datetime.now()

    plt.plot(disallowedIter, disallowedTarget, ls='none', marker='o', color='C1', label='fail')
    plt.plot(allowedIter, allowedTarget, ls='none', marker='o', color='C0', label='pass')
    plt.yscale('log')
    plt.legend(loc='upper right')
    plt.title(f'All iterations {dataId}')
    plt.xlabel('iteration')
    plt.ylabel('XS [pb]')

    plt.savefig(os.path.join(pathOutputDataId, f'plot_all_{dataId}.pdf'))
    plt.savefig(os.path.join(pathOutputDataId, f'plot_all_{dataId}.png'))
    plt.savefig(os.path.join(pathOutput, f'plot_all_{dataId}.png'))
    plt.close()


    plt.plot(disallowedIter, disallowedTarget, ls='none', marker='o', color='C1', label='fail')
    plt.yscale('log')
    plt.legend(loc='upper right')
    plt.title(f'Failed iterations {dataId}')
    plt.xlabel('iteration')
    plt.ylabel('XS [pb]')

    plt.savefig(os.path.join(pathOutputDataId, f'plot_fail_{dataId}.pdf'))
    plt.savefig(os.path.join(pathOutputDataId, f'plot_fail_{dataId}.png'))
    plt.savefig(os.path.join(pathOutput, f'plot_fail_{dataId}.png'))
    plt.close()


    plt.plot(allowedIter, allowedTarget, ls='none', marker='o', color='C0', label='pass')
    plt.yscale('log')
    plt.legend(loc='upper right')
    plt.title(f'Passed iterations {dataId}')
    plt.xlabel('iteration')
    plt.ylabel('XS [pb]')

    plt.savefig(os.path.join(pathOutputDataId, f'plot_pass_{dataId}.pdf'))
    plt.savefig(os.path.join(pathOutputDataId, f'plot_pass_{dataId}.png'))
    plt.savefig(os.path.join(pathOutput, f'plot_pass_{dataId}.png'))
    plt.close()


from helpScannerS import configurer as config

import pandas
import os
import subprocess

if __name__ == '__main__':

    ## paths

    # path repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to ScannerS TRSM executable
    pathTRSM = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken'

    # path where all output from ScannerS will be stored
    pathBPnoconstraints = os.path.join(pathRepo, 'Benchmarkplanes',
                                       'BPs_noconstraints')

    os.makedirs(pathBPnoconstraints, exist_ok=True)

    # path to dataIds. Just a file that lists all the individual
    # dataIds in a .txt file
    pathBPnoconstraintsDataId = os.path.join(pathRepo, 'Benchmarkplanes', 'BPs_noconstraints', 'dataIds.txt')


    modelParamsBP2 = {'mH1_lb': 1,      'mH1_ub': 124,    'mH1Points': 100,
                      'mH2_lb': 125.09, 'mH2_ub': 125.09, 'mH2Points': 1,
                      'mH3_lb': 126,    'mH3_ub': 500,    'mH3Points': 100,
                      'thetahS_lb': 1.352,  'thetahS_ub': 1.352,  'thetahSPoints': 1,
                      'thetahX_lb': 1.175,  'thetahX_ub': 1.175,  'thetahXPoints': 1,
                      'thetaSX_lb': -0.407, 'thetaSX_ub': -0.407, 'thetaSXPoints': 1,
                      'vs_lb': 120, 'vs_ub': 120, 'vsPoints': 1,
                      'vx_lb': 890, 'vx_ub': 890, 'vxPoints': 1,
                      'extra': {'dataId': 'BP2'}}

    modelParamsBP3 = {'mH1_lb': 125.09, 'mH1_ub': 125.09, 'mH1Points': 1,
                      'mH2_lb': 126,    'mH2_ub': 500,    'mH2Points': 100,
                      'mH3_lb': 255,    'mH3_ub': 650,    'mH3Points': 100,
                      'thetahS_lb': -0.129, 'thetahS_ub': -0.129, 'thetahSPoints': 1,
                      'thetahX_lb': 0.226,  'thetahX_ub': 0.226,  'thetahXPoints': 1,
                      'thetaSX_lb': -0.899, 'thetaSX_ub': -0.899, 'thetaSXPoints': 1,
                      'vs_lb': 140, 'vs_ub': 140, 'vsPoints': 1,
                      'vx_lb': 100, 'vx_ub': 100, 'vxPoints': 1,
                      'extra': {'dataId': 'BP3'}}

    # remaining BPs in the TRSM paper, however they are not used, only written here
    # in case of future need

    modelParamsBP1 = {'mH1_lb': 1,      'mH1_ub': 62,     'mH1Points': 100,
                      'mH2_lb': 1,      'mH2_ub': 124,    'mH2Points': 100,
                      'mH3_lb': 125.09, 'mH3_ub': 125.09, 'mH3Points': 1,
                      'thetahS_lb': 1.435,  'thetahS_ub': 1.435,  'thetahSPoints': 1,
                      'thetahX_lb': -0.908, 'thetahX_ub': -0.908, 'thetahXPoints': 1,
                      'thetaSX_lb': -1.456, 'thetaSX_ub': -1.456, 'thetaSXPoints': 1,
                      'vs_lb': 630, 'vs_ub': 630, 'vsPoints': 1,
                      'vx_lb': 700, 'vx_ub': 700, 'vxPoints': 1,
                      'extra': {'dataId': 'BP1'}}

    modelParamsBP4 = {'mH1_lb': 1,      'mH1_ub': 62,     'mH1Points': 100,
                      'mH2_lb': 1,      'mH2_ub': 124,    'mH2Points': 100,
                      'mH3_lb': 125.09, 'mH3_ub': 125.09, 'mH3Points': 1,
                      'thetahS_lb': -1.284, 'thetahS_ub': -1.284, 'thetahSPoints': 1,
                      'thetahX_lb': 1.309,  'thetahX_ub': 1.309,  'thetahXPoints': 1,
                      'thetaSX_lb': -1.519, 'thetaSX_ub': -1.519, 'thetaSXPoints': 1,
                      'vs_lb': 990, 'vs_ub': 990, 'vsPoints': 1,
                      'vx_lb': 310, 'vx_ub': 310, 'vxPoints': 1,
                      'extra': {'dataId': 'BP4'}}

    modelParamsBP5 = {'mH1_lb': 1,      'mH1_ub': 124,    'mH1Points': 100,
                      'mH2_lb': 125.09, 'mH2_ub': 125.09, 'mH2Points': 1,
                      'mH3_lb': 126,    'mH3_ub': 500,    'mH3Points': 100,
                      'thetahS_lb': -1.498, 'thetahS_ub': -1.498, 'thetahSPoints': 1,
                      'thetahX_lb': 0.251,  'thetahX_ub': 0.251,  'thetahXPoints': 1,
                      'thetaSX_lb': 0.271,  'thetaSX_ub': 0.271,  'thetaSXPoints': 1,
                      'vs_lb': 50,  'vs_ub': 50,  'vsPoints': 1,
                      'vx_lb': 720, 'vx_ub': 720, 'vxPoints': 1,
                      'extra': {'dataId': 'BP5'}}

    modelParamsBP6 = {'mH1_lb': 125.09, 'mH1_ub': 125.09, 'mH1Points': 1,
                      'mH2_lb': 126,    'mH2_ub': 500,    'mH2Points': 100,
                      'mH3_lb': 255,    'mH3_ub': 1000,   'mH3Points': 100,
                      'thetahS_lb': 0.207, 'thetahS_ub': 0.207, 'thetahSPoints': 1,
                      'thetahX_lb': 0.146,  'thetahX_ub': 0.146,  'thetahXPoints': 1,
                      'thetaSX_lb': 0.782, 'thetaSX_ub': 0.782, 'thetaSXPoints': 1,
                      'vs_lb': 220, 'vs_ub': 220, 'vsPoints': 1,
                      'vx_lb': 150, 'vx_ub': 150, 'vxPoints': 1,
                      'extra': {'dataId': 'BP6'}}

    ## constraints turned off

    # create the input files for the ScannerS TRSM executable
    listModelParams = [modelParamsBP2, modelParamsBP3]
    config.configureDirs(listModelParams, pathBPnoconstraints,
                         pathBPnoconstraintsDataId, massOrder=True)

    # start running the ScannerS TRSM executable with all constraints turned off
    for X in [2, 3]:
        print(f'*~~~~~~~~~ Starting ScannerS TRSM with BP{X} settings ~~~~~~~~~*')

        # necessary paths for the ScannerS TRSM executable
        pathBPX = os.path.join(pathBPnoconstraints, f'BP{X}')
        outputBPX = os.path.join(pathBPX, f'output_BP{X}_noconstraints.tsv')

        # the config files are the same both in the constraints and 
        # no constraints case
        configBPX = os.path.join(pathBPX, f'config_BP{X}.tsv')

        # all constraints turned on
        # constraints = ['--BFB', '0', '--Uni', '0', '--STU', '0', '--Higgs', '0']
        # subprocess.run([pathTRSM, *constraints, outputBPX, 'check', configBPX],
        #                cwd=pathBPX)

        print(f'*~~~~~~~~~ filtering values which are only constrained for BP{X} ~~~~~~~~~*')
    
        df = pandas.read_table(outputBPX)

        # BFB
        dfBFB = df[df['valid_BFB'] == 0]
        pathBFB = os.path.join(pathBPX, f'output_BP{X}_onlyBFB.tsv')
        dfBFB.to_csv(pathBFB, sep='\t')
        print(f'Filtering rows in output_BP{X}.tsv which fail BFB and saving it in\n\
{pathBFB}\n')

        # Uni
        dfUni = df[df['valid_Uni'] == 0]
        pathUni = os.path.join(pathBPX, f'output_BP{X}_onlyUni.tsv')
        dfUni.to_csv(pathUni, sep='\t')
        print(f'Filtering rows in output_BP{X}.tsv which fail Uni and saving it in\n\
{pathUni}\n')

        # STU
        dfSTU = df[df['valid_STU'] == 0]
        pathSTU = os.path.join(pathBPX, f'output_BP{X}_onlySTU.tsv')
        dfSTU.to_csv(pathSTU, sep='\t')
        print(f'Filtering rows in output_BP{X}.tsv which fail STU and saving it in\n\
{pathSTU}\n')

        # Higgs
        dfHiggs = df[df['valid_Higgs'] == 0]
        pathHiggs = os.path.join(pathBPX, f'output_BP{X}_onlyHiggs.tsv')
        dfHiggs.to_csv(pathHiggs, sep='\t')
        print(f'Filtering rows in output_BP{X}.tsv which fail Higgs and saving it in\n\
{pathHiggs}\n')

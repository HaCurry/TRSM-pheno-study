import pandas
import os
import twoD_SusHiCrossSections as SusHi

if __name__ == '__main__':

    ## paths

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    # path to plot directory
    # E:
    pathPlots = '/eos/user/i/ihaque/SusHiPlots'

    # path to SusHi executable
    # E:
    pathSUSHI = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/SusHi_install/SusHi-1.6.1/bin/sushi'

    # directory containting SusHi input and output (created just to run this script)
    # user will not need to interact with this directory, all cross sections from SusHi
    # will be saved in a .tsv file
    pathTemp = os.path.join(pathRepo,
                            'testing/SusHi_HiggsCrossSections/SusHiOutputsTemp')

    # create directories (plotting and .tsv files) for scale uncertatinty cross sections
    os.makedirs(os.path.join(pathPlots, 'scaleUncert'), exist_ok=True) 
    os.makedirs(os.path.join(pathRepo, '13_6TeV_SusHiCrossSections_ScaleUncert'), exist_ok=True)

    # read in masses which SusHi will generate cross sections. The masses are
    # the masses recommended by the LHCHWG (see the twiki for more info)
    dfYR4_14 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                 'SusHi_HiggsCrossSections', '14TeV_YR4CrossSections.tsv'))

    masses = [mass for mass in dfYR4_14['mass']]

    ## 13.6 TeV scale uncertainty SusHi cross sections


    ## renormalization scale muR/mh = 0.25
    ## factorization scale muF/mh = 0.25

    # The paths are broken up using os.path.join so that you do not have long
    # unreadable strings.
    pathOutputCrossSec_13_6TeV_025mh_025mh = os.path.join(pathRepo,
                                                          'testing/SusHi_HiggsCrossSections',
                                                          '13_6TeV_SusHiCrossSections_ScaleUncert',
                                                          '13_6TeV_SusHiCrossSections_025mh_025mh.tsv')
    pathOutputCrossSecPlots_13_6TeV_025mh_025mh = os.path.join(pathPlots,
                                                               'scaleUncert',
                                                               '13_6TeV_SusHiCrossSections_025mh_025mh.pdf')

    SusHi.SusHiCrossSections(masses, 13600, 'NNLO', pathOutputCrossSec_13_6TeV_025mh_025mh, 
                             pathOutputCrossSecPlots_13_6TeV_025mh_025mh, pathTemp, pathSUSHI,
                             renormScalemuR=0.25, factScalemuF=0.25) 

    ## renormalization scale muR/mh = 0.25
    ## factorization scale muF/mh = 1

    pathOutputCrossSec_13_6TeV_025mh_1mh = os.path.join(pathRepo,
                                                        'testing/SusHi_HiggsCrossSections',
                                                        '13_6TeV_SusHiCrossSections_ScaleUncert',
                                                        '13_6TeV_SusHiCrossSections_025mh_1mh.tsv')
    pathOutputCrossSecPlots_13_6TeV_025mh_1mh = os.path.join(pathPlots,
                                                             'scaleUncert',
                                                             '13_6TeV_SusHiCrossSections_025mh_1mh.pdf')

    SusHi.SusHiCrossSections(masses, 13600, 'NNLO', pathOutputCrossSec_13_6TeV_025mh_1mh,
                             pathOutputCrossSecPlots_13_6TeV_025mh_1mh, pathTemp, pathSUSHI,
                             renormScalemuR=0.25, factScalemuF=1) 

    ## renormalization scale muR/mh = 1 
    ## factorization scale muF/mh = 1 

    pathOutputCrossSec_13_6TeV_1mh_1mh = os.path.join(pathRepo,
                                                      'testing/SusHi_HiggsCrossSections',
                                                      '13_6TeV_SusHiCrossSections_ScaleUncert',
                                                      '13_6TeV_SusHiCrossSections_1mh_1mh.tsv')
    pathOutputCrossSecPlots_13_6TeV_1mh_1mh = os.path.join(pathPlots,
                                                           'scaleUncert',
                                                           '13_6TeV_SusHiCrossSections_1mh_1mh.pdf')

    SusHi.SusHiCrossSections(masses, 13600, 'NNLO', pathOutputCrossSec_13_6TeV_1mh_1mh, 
                             pathOutputCrossSecPlots_13_6TeV_1mh_1mh , pathTemp, pathSUSHI,
                             renormScalemuR=1, factScalemuF=1) 

    ## renormalization scale muR/mh = 1 
    ## factorization scale muF/mh = 0.25

    pathOutputCrossSec_13_6TeV_1mh_025mh = os.path.join(pathRepo,
                                                        'testing/SusHi_HiggsCrossSections',
                                                        '13_6TeV_SusHiCrossSections_ScaleUncert',
                                                        '13_6TeV_SusHiCrossSections_1mh_025mh.tsv')
    pathOutputCrossSecPlots_13_6TeV_1mh_025mh = os.path.join(pathPlots,
                                                             'scaleUncert',
                                                             '13_6TeV_SusHiCrossSections_1mh_025mh.pdf')

    SusHi.SusHiCrossSections(masses, 13600, 'NNLO', pathOutputCrossSec_13_6TeV_1mh_025mh,
                             pathOutputCrossSecPlots_13_6TeV_1mh_025mh, pathTemp, pathSUSHI,
                             renormScalemuR=1, factScalemuF=0.25)

    ## renormalization scale muR/mh = 0.5
    ## factorization scale muF/mh = 0.5

    pathOutputCrossSec_13_6TeV_05mh_05mh = os.path.join(pathRepo,
                                                         'testing/SusHi_HiggsCrossSections',
                                                         '13_6TeV_SusHiCrossSections_ScaleUncert',
                                                         '13_6TeV_SusHiCrossSections_05mh_05mh.tsv')
    pathOutputCrossSecPlots_13_6TeV_05mh_05mh = os.path.join(pathPlots,
                                                             'scaleUncert',
                                                             '13_6TeV_SusHiCrossSections_05mh_05mh.pdf')

    SusHi.SusHiCrossSections(masses, 13600, 'NNLO', pathOutputCrossSec_13_6TeV_05mh_05mh,
                             pathOutputCrossSecPlots_13_6TeV_05mh_05mh, pathTemp, pathSUSHI,
                             renormScalemuR=0.5, factScalemuF=0.5) 

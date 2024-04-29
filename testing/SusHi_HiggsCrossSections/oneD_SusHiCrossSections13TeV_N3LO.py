import os
import pandas
import oneD_SusHiConfigure as SusHi

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

    # create plotting directory if it does not already exist
    os.makedirs(pathPlots, exist_ok=True)

    # directory containting SusHi input and output (created just to run this script)
    # user will not need to interact with this directory, all cross sections from SusHi
    # will be saved in a .tsv file
    pathTemp = os.path.join(pathRepo,
                            'testing/SusHi_HiggsCrossSections/SusHiOutputsTemp')

    # read in masses which SusHi will generate cross sections. The masses are
    # the masses recommended by the LHCHWG (see the twiki for more info)
    dfYR4_14 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                 'SusHi_HiggsCrossSections', '14TeV_YR4CrossSections.tsv'))

    masses = [mass for mass in dfYR4_14['mass']]

    # OBS: everything here is NNLO unless otherwise specified


    ## 13 TeV SusHi cross sections at N3LO

    pathOutputCrossSec_13TeV_N3LO = os.path.join(pathRepo,
                                                 'testing/SusHi_HiggsCrossSections/13TeV_N3LO_SusHiCrossSections.tsv') 
    pathOutputCrossSecPlots_13TeV_N3LO = os.path.join(pathPlots, 'plots1D/13TeV_N3LO_SusHiCrossSections.pdf')

    print('===================================================================')
    print('GENERATING SM ggF HIGGS CROSS SECTIONS WITH SUSHI AT 13 TeV, N3LO')
    print('===================================================================')

    SusHi.SusHiCrossSections(masses, 13000, 'N3LO', pathOutputCrossSec_13TeV_N3LO,
                             pathOutputCrossSecPlots_13TeV_N3LO, pathTemp, pathSUSHI) 

import numpy as np
import pandas
import os

if __name__ == '__main__':

    # path to repo
    # E:
    pathRepo = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno'

    ## create 13.6 (ScannerS * SusHiFactor) SM cross sections

    dfSusHi_13 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                   'SusHi_HiggsCrossSections', 
                                   '13TeV_SusHiCrossSections.tsv'))

    XSSusHi_13 = np.array(dfSusHi_13['SMCrossSec'])

    dfSusHi_13_6 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                     'SusHi_HiggsCrossSections',
                                     '13_6TeV_SusHiCrossSections.tsv'))

    XSSusHi_13_6 = np.array(dfSusHi_13_6['SMCrossSec'])

    XS_13_to_13_6_factor = XSSusHi_13_6/XSSusHi_13

    dfScannerS_13 = pandas.read_table(os.path.join(pathRepo, 'testing',
                                      'SusHi_HiggsCrossSections',
                                      '13TeV_ScannerSCrossSections.tsv'))

    XSScannerS_13_6 = np.array(dfScannerS_13['SMCrossSec']) * XS_13_to_13_6_factor

    dfScannerS_13_6 = pandas.DataFrame({'mass': dfScannerS_13['mass'],
                                       'SMCrossSec': XSScannerS_13_6})

    dfScannerS_13_6.to_csv('13_6TeV_SusHiImprCrossSections.tsv', sep='\t')


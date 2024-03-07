import re

pathExecutionOutput = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/SusHi_install/SusHi-1.6.1/bin/SM-NNLO.out'


lines = []
with open(pathExecutionOutput) as outputFile:
    for line in outputFile:
        #print(line)
        if '# ggh XS in pb' in line:
            print(line)

#print(float(lines[22].split()[1]))

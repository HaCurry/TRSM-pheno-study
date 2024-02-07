#!/bin/bash
#testvar="x40-s3.923"
#mkdir "$testvar"
echo "trying to run scannerS on HTcondor..."
cd /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testMax/$1
/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testMax/$1/$1_output.tsv check /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testMax/$1/$1_config.tsv
echo "$1"

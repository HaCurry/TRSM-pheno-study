#!/bin/bash
#testvar="x40-s3.923"
#mkdir "$testvar"
echo "trying to run scannerS on HTcondor..."
cd /home/iram/scannerS/ScannerS-master/build/regionTestingDirectory/testMaxTryingToFindNaN/$1
/home/iram/scannerS/ScannerS-master/build/TRSMBroken /home/iram/scannerS/ScannerS-master/build/regionTestingDirectory/testMaxTryingToFindNaN/$1/$1_output.tsv check /home/iram/scannerS/ScannerS-master/build/regionTestingDirectory/testMaxTryingToFindNaN/$1/$1_config.tsv
echo "$1"

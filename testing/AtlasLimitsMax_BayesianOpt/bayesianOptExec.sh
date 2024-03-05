#!/bin/bash

while getopts ":X:S:d:" option; do
  case $option in
    X) # starting directory path
      Xmass=$OPTARG;;
    S) # ouput directory path
      Smass=$OPTARG;;
    d)
      dataId=$OPTARG;;
    \?) # Invalid option
      echo "Error: Invalid option"
      exit;;
  esac
done

echo 'checking versions of dependencies'
pip3 freeze | grep -i 'scikit'
pip3 freeze | grep -i 'numpy'
pip3 freeze | grep -i 'scipy'
pip3 freeze | grep -i 'colorama'
echo 'end of python packages installed'

echo 'installing BayesianOptimization'
cd /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt/BayesianOptimization-1.4.3
python3 setup.py install --user
cd ..

echo 'installing matplotlib'
pip3 install matplotlib

echo 'running optimization'
python3 twoD_AtlasLimitsMaxBayOpt.py -mX ${X} -mS ${S} -SM1 bb -SM2 gamgam -o /eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_bayesianOpt -e /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken -d ${dataId} -init 25 -iter 100 -kind ucb

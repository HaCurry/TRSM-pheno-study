#!/bin/bash
pip3 freeze | grep -i 'scikit'
pip3 freeze | grep -i 'numpy'
pip3 freeze | grep -i 'scipy'
pip3 freeze | grep -i 'colorama'
echo 'end of python packages installed'
echo 'Hejsan Svejsan pa digsan'
cd /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_BayesianOpt 
cd BayesianOptimization-1.4.3
python3 setup.py install --user
cd ..
python3 twoD_AtlasLimitsMaxBayOpt.py

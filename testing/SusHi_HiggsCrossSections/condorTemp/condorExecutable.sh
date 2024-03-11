#!/bin/bash

echo 'installing matplotlib'
pip3 install matplotlib

# Enables SusHi to work properly
source /cvmfs/sft.cern.ch/lcg/views/LCG_104c_ATLAS_5/x86_64-el9-gcc13-opt/setup.sh
lhapdf-config --incdir
lhapdf-config --libdir

# Enter directory and run python script which runs SusHi
cd /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections
time python3 twoD_SusHiCrossSections.py

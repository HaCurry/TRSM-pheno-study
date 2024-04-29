#!/bin/bash

# Source lcg (for SusHi to be able to access LHAPDFs)
source /cvmfs/sft.cern.ch/lcg/views/LCG_104c_ATLAS_5/x86_64-el9-gcc13-opt/setup.sh
lhapdf-config --incdir
lhapdf-config --libdir

# Install matplotlib for later plotting
pip3 install matplotlib
pip3 install pandas
#pip3 install matplotlib-inline==0.1.5

# Enter directory and run python script which runs SusHi
cd /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections
time python3 oneD_SusHiCrossSections13TeV.py

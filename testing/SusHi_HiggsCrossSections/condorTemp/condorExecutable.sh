#!/bin/bash

echo 'installing matplotlib'
pip3 install matplotlib

cd /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections
time python3 twoD_SusHiCrossSections.py

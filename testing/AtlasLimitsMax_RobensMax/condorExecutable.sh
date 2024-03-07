#!/bin/bash
cd /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_RobensMax
time /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken --config /afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/AtlasLimitsMax_RobensMax/TRSMBroken.ini scan -n 100000

#!/bin/bash
# condor executable

echo "trying to run scannerS on HTcondor..."

# default values
# path to where all the directories with config files reside
pathOutputDirs=/eos/user/i/ihaque/AtlasLimitsMax/AtlasLimitsMax_configure2
# path to ScannerS executable
pathScannerS=/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/TRSMBroken

# for debugging purposes except -i which specifies the specific dataId
# from https://www.redhat.com/sysadmin/arguments-options-bash-scripts
while getopts ":o:i:s:" option; do
  case $option in
    o) # starting directory path
      pathOutputDirs=$OPTARG;;
    i) # ouput directory path
      dataId=$OPTARG;;
    s) # scannerS executable path
      pathScannerS=$OPTARG;;
    \?) # Invalid option
      echo "Error: Invalid option"
      exit;;
  esac
done

# condor needs to give path to output directory
# from https://unix.stackexchange.com/a/621007/590852
: ${dataId:?Missing -i, please specify dataId}

# cd into pathOutputDirs/dataId
echo "Entering ${pathOutputDirs}/${dataId}"
cd ${pathOutputDirs}/${dataId}

# execute ScannerS TRSM executable
${pathScannerS} ${pathOutputDirs}/${dataId}/output_${dataId}.tsv check ${pathOutputDirs}/${dataId}/config_${dataId}.tsv
echo "Finished job in ${pathOutputDirs}/${dataId}"
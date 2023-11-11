#!/bin/bash

######################
### region testing ###
######################

### constraints

bfbval=apply
unival=apply
stuval=apply
Higgsval=apply

#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini DEFAULT bfb $bfbval
#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini DEFAULT uni $unival
#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini DEFAULT stu $stuval
#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini DEFAULT Higgs $Higgsval

#crudini --set --existing example_input/TRSMBroken_regionTesting.ini DEFAULT bfb $bfbval
#crudini --set --existing example_input/TRSMBroken_regionTesting.ini DEFAULT uni $unival
#crudini --set --existing example_input/TRSMBroken_regionTesting.ini DEFAULT stu $stuval
#crudini --set --existing example_input/TRSMBroken_regionTesting.ini DEFAULT Higgs $Higgsval

#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini DEFAULT bfb $bfbval
#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini DEFAULT uni $unival
#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini DEFAULT stu $stuval
#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini DEFAULT Higgs $Higgsval

crudini --set --existing TRSMBroken_regionTesting.ini DEFAULT bfb $bfbval
crudini --set --existing TRSMBroken_regionTesting.ini DEFAULT uni $unival
crudini --set --existing TRSMBroken_regionTesting.ini DEFAULT stu $stuval
crudini --set --existing TRSMBroken_regionTesting.ini DEFAULT Higgs $Higgsval

### model parameters

argv=("$@")

mHa_val_lb=${argv[0]}
mHa_val_ub=${argv[1]}

mHb_val_lb=${argv[2]}
mHb_val_ub=${argv[3]}

mHc_val_lb=${argv[4]}
mHc_val_ub=${argv[5]}

ths_val_lb=${argv[6]}
ths_val_ub=${argv[7]}

thx_val_lb=${argv[8]}
thx_val_ub=${argv[9]}

tsx_val_lb=${argv[10]}
tsx_val_ub=${argv[11]}

vs_val_lb=${argv[12]}
vs_val_ub=${argv[13]}

vx_val_lb=${argv[14]}
vx_val_ub=${argv[15]}

points=${argv[16]}


#for (( j=0; j<argc; j++ )); do
#    echo "${argv[j]}"
#done

#mHa_val_lb=$1
#mHa_val_ub=$2

#mHb_val_lb=$3
#mHb_val_ub=$4

#mHc_val_lb=$5
#mHc_val_ub=$6

#ths_val_lb=$7
#ths_val_ub=$8

#thx_val_lb=$9
#thx_val_ub=$10

#tsx_val_lb=$11
#tsx_val_ub=$12

#vs_val_lb=$13
#vs_val_ub=$14

#vx_val_lb=$15
#vx_val_ub=$16

#points=$17




#pihalf=1.57079632679



######################################################## FREE PARAMETERS ########################################################

### X -> SH ths free
#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini scan mHa $mHa_val_lb\ $mHa_val_ub
#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini scan mHb $mHb_val_lb\ $mHb_val_ub
#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini scan mHc $mHc_val_lb\ $mHc_val_ub

#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini scan t1 $ths_val_lb\ $ths_val_ub
#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini scan t2 $thx_val_lb\ $thx_val_ub
#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini scan t3 $tsx_val_lb\ $tsx_val_ub

#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini scan vs $vs_val_lb\ $vs_val_ub
#crudini --set --existing /home/iram/scannerS/ScannerS-master/build/example_input/TRSMBroken_regionTesting.ini scan vx $vx_val_lb\ $vx_val_ub

#crudini --set --existing example_input/TRSMBroken_regionTesting.ini scan mHa $mHa_val_lb\ $mHa_val_ub
#crudini --set --existing example_input/TRSMBroken_regionTesting.ini scan mHb $mHb_val_lb\ $mHb_val_ub
#crudini --set --existing example_input/TRSMBroken_regionTesting.ini scan mHc $mHc_val_lb\ $mHc_val_ub

#crudini --set --existing example_input/TRSMBroken_regionTesting.ini scan t1 $ths_val_lb\ $ths_val_ub
#crudini --set --existing example_input/TRSMBroken_regionTesting.ini scan t2 $thx_val_lb\ $thx_val_ub
#crudini --set --existing example_input/TRSMBroken_regionTesting.ini scan t3 $tsx_val_lb\ $tsx_val_ub

#crudini --set --existing example_input/TRSMBroken_regionTesting.ini scan vs $vs_val_lb\ $vs_val_ub
#crudini --set --existing example_input/TRSMBroken_regionTesting.ini scan vx $vx_val_lb\ $vx_val_ub

#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini scan mHa $mHa_val_lb\ $mHa_val_ub
#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini scan mHb $mHb_val_lb\ $mHb_val_ub
#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini scan mHc $mHc_val_lb\ $mHc_val_ub

#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini scan t1 $ths_val_lb\ $ths_val_ub
#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini scan t2 $thx_val_lb\ $thx_val_ub
#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini scan t3 $tsx_val_lb\ $tsx_val_ub

#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini scan vs $vs_val_lb\ $vs_val_ub
#crudini --set --existing ../example_input/TRSMBroken_regionTesting.ini scan vx $vx_val_lb\ $vx_val_ub

crudini --set --existing TRSMBroken_regionTesting.ini scan mHa $mHa_val_lb\ $mHa_val_ub
crudini --set --existing TRSMBroken_regionTesting.ini scan mHb $mHb_val_lb\ $mHb_val_ub
crudini --set --existing TRSMBroken_regionTesting.ini scan mHc $mHc_val_lb\ $mHc_val_ub

crudini --set --existing TRSMBroken_regionTesting.ini scan t1 $ths_val_lb\ $ths_val_ub
crudini --set --existing TRSMBroken_regionTesting.ini scan t2 $thx_val_lb\ $thx_val_ub
crudini --set --existing TRSMBroken_regionTesting.ini scan t3 $tsx_val_lb\ $tsx_val_ub

crudini --set --existing TRSMBroken_regionTesting.ini scan vs $vs_val_lb\ $vs_val_ub
crudini --set --existing TRSMBroken_regionTesting.ini scan vx $vx_val_lb\ $vx_val_ub


## if this script is run from the directory regionTestingDirectory
#../TRSMBroken regionTesting.tsv --config ../example_input/TRSMBroken_regionTesting.ini scan -n $points
## if this script is run in same directory
#./TRSMBroken regionTestingDirectory/regionTesting.tsv --config example_input/TRSMBroken_regionTesting.ini scan -n $points
## if this script is run in same directory with .ini file in same directory
../TRSMBroken regionTesting.tsv --config TRSMBroken_regionTesting.ini scan -n $points


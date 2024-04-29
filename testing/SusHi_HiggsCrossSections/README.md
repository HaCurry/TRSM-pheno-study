# OBS!

No need to run any scripts in this directory. The plotting scripts (`..._plot.py`)
may be modified and run again if desired.

OBS. If scripts is needed to run with condor (specifically the scripts) 
`twoD_SusHiCrossSections13TeV.py`
`twoD_SusHiCrossSections13TeV_N3LO.py`
`twoD_SusHiCrossSections13_6TeV.py`
`twoD_SusHiScaleUncertCrossSections.py`
then make sure to not submit them at the same time. This is due to the
scripts will be trying to execute the _same_ SusHi executable at the
same time which will most likely lead to problems.

In other words, submit the above scripts (i.e the condor submit files in `SusHiCondor13TeV`,
`SusHiCondor13TeV_N3LO`, `SusHiCondor13_6TeV`, `SusHiCondorScaleUncert`) and sequentially,
i.e after each job has finished. 

Or just run them locally, that works fine as well (but not in parallel)!

# TABLE OF CONTENTS IN THIS DIRECTORY

## calculating scripts

The `.tsv` files in this directory contains all the cross sections
used in the thesis. However, the scale uncertainty cross sections in the
directory `13_6TeV_SusHiCrossSections_ScaleUncert` are not used and can
be ignored.

`oneD_ScannerSCrossSections13TeV.py`: creates the 13 TeV LHCHWG SM ggF Higgs cross 
sections (`13TeV_ScannerSCrossSections.tsv`) using the ScannerS TRSM executable.

`twoD_SusHiCrossSections.py`: contains some functions for generating the SusHi SM ggF
Higgs cross sections at 13 TeV, 13.6 TeV and NNLO, N3LO. This script is mainly used
as module for the scripts below.

`twoD_SusHiCrossSections13TeV.py`: imports functions from `twoD_SusHiCrossSections.py`
and generates the 13 TeV NNLO SM ggF Higgs cross sections (`13TeV_SusHiCrossSections.tsv`).
Can be run with condor, see the directory `SusHiCondor13TeV`

`twoD_SusHiCrossSections13_6TeV.py`: imports functions from `twoD_SusHiCrossSections.py`
and generates the 13.6 TeV NNLO SM ggF Higgs cross sections (`13_6TeV_SusHiCrossSections.tsv`).
Can be run with condor, see the directory `SusHiCondor13_6TeV`

`twoD_SusHiCrossSections13TeV_N3LO.py`: imports functions from `twoD_SusHiCrossSections.py`
and generates the 13 TeV N3LO SM ggF Higgs cross sections (`13TeV_N3LO_SusHiCrossSections.tsv`).
Can be run with condor, see the directory `SusHiCondor13TeV_N3LO`

`oneD_SusHiImprCrossSections13_6TeV.py`: creates the SusHi improved cross sections
(13.6 TeV) as seen in the thesis (`13_6TeV_SusHiImprCrossSections.tsv`).

Remaining scripts in this directory are of no importance and is not used in the thesis.

## plotting scripts

`oneD_SusHiScannerSCrossSections13TeV_13_6TeV_plot.py` plots some figures using the `.tsv`
files in this directory. Some of the figures in this script appears in the thesis.

Remaining scripts in this directory are of no importance and is not used in the thesis.
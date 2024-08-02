# OBS!

No need to run any scripts in this directory, however, the plotting scripts (`..._plot.py`) may be modified and run again if desired.

OBS. If scripts is needed to run with condor (specifically the scripts), `twoD_SusHiCrossSections13TeV.py`, `twoD_SusHiCrossSections13_6TeV.py` then make sure to *not*
submit them at the same time. This is due to the scripts will be trying to execute the _same_ SusHi executable at the same time which will most likely lead to problems.

In other words, submit the above scripts (i.e the condor submit files in `SusHiCondor13TeV`, `SusHiCondor13TeV_N3LO`, `SusHiCondor13_6TeV`) sequentially, i.e after each
job has finished.

Or just run them locally, that works fine as well (but not in parallel)!

Observe, the `.tsv` files `13TeV_ScannerSCrossSections` and `14TeV_YR4CrossSections.tsv`  corresponds to the 13 TeV LHCHWG and 14 TeV LHCHWG SM ggF Higgs cross sections
respectively. In the thesis they are refered to as LHCHWG cross sections, here they are (confusingly) named differently. The `.tsv` file `13TeV_ScannerSCrossSections` is
generated using ScannerS but they could as well have been taken from the LHCHWG website.


# TABLE OF CONTENTS IN THIS DIRECTORY

## calculating scripts

`oneD_ScannerSCrossSections13TeV.py`: creates the 13 TeV LHCHWG SM ggF Higgs cross  sections (`13TeV_ScannerSCrossSections.tsv`) using the ScannerS TRSM executable.

`oneD_SusHiConfigure.py`: contains some functions for generating the SusHi SM ggF Higgs cross sections at 13 TeV, 13.6 TeV and NNLO, N3LO. This script is mainly used as
module for the scripts below.

`oneD_SusHiCrossSections13TeV.py`: imports functions from `oneD_SusHiConfigure.py` and generates the 13 TeV NNLO SM ggF Higgs cross sections
(`13TeV_SusHiCrossSections.tsv`). Can be run with condor, see the directory `SusHiCondor13TeV`

`oneD_SusHiCrossSections13_6TeV.py`: imports functions from `oneD_SusHiConfigure.py` and generates the 13.6 TeV NNLO SM ggF Higgs cross sections
(`13_6TeV_SusHiCrossSections.tsv`). Can be run with condor, see the directory `SusHiCondor13_6TeV`

`oneD_SusHiImprCrossSections13_6TeV.py`: creates the SusHi improved cross sections (13.6 TeV) as seen in the thesis (`13_6TeV_SusHiImprCrossSections.tsv`).

Remaining scripts in this directory are of no importance and is not used in the thesis.

## plotting scripts

`oneD_SusHiScannerSCrossSections13TeV_13_6TeV_plot.py` plots some figures using the `.tsv` files in this directory. Some of the figures in this script appears in the
thesis.

`twoD_SusHiImpr13_6TeV_NPSM_plot.py`: plots the $gg \to h_{3} \to h_{1}(b\bar{b}/\gamma\gamma) h_{2}(\gamma\gamma/b\bar{b})$ using the SusHi improved cross sections
(`13_6TeV_SusHiImprCrossSections.tsv`) at 13.6 TeV as seen in the thesis.

`twoD_YR413_6TeV_NPSM_plot.py`: plots the gg -> H3 -> H1(bb/gamgam) H2(gamgam/bb) using the YR4 cross sections (`14TeV_YR4CrossSections.tsv`) at 14 TeV as seen in the
thesis (in the thesis they are referred to as the LHCHWG 14 TeV cross sections).

Remaining scripts in this directory are of no importance and is not used in the thesis.

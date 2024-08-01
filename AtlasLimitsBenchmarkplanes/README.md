# TABLE OF CONTENTS IN THIS DIRECTORY

This directory plots the figures of the ATLAS limits vs the benchmark plane predicted cross sections by the TRSM (BP2 and BP3).

## calculating scripts

`twoD_AtlasLimBPs_configure.py`: (OBS this script does not need to be run, all the output is compiled in `AtlasLimitsBenchmarkplanes.tsv`) calculates
$b\bar{b}\gamma\gamma$ cross sections using TRSM with BP2 and BP3 settings for the mass points in `Atlas2023Limits.json` and stores them in `pathOutputParent`. Compiles
all the cross sections and the limits in one single file in `AtlasLimitsBenchmarkplanes.tsv`. Make sure to provide the path to the TRSM executable in `pathTRSM`.

## plotting scripts

`twoD_AtlasLimBPs_plot.py`: plots the ratio of the observed limits and the TRSM $b\bar{b}\gamma\gamma$ cross sections found in `AtlasLimitsBenchmarkplanes.tsv`. Figures
can be found in [plots](plots).

# TABLE OF CONTENTS IN THIS DIRECTORY
Creates a grid of $10\times 10 \times 10 \times 10 \times 10 = 100000$ sets of model parameters for each mass point in the ATLAS limits `Atlas2023Limits.json`. This is
then fed into the TRSMBroken executable which excludes parameter sets which fail HiggsBounds, HiggsSignals and the theoretical constraints and calculates the various
observables from the surviving model parameters. The fraction of surviving models are then plotted. From the surviving sets the maximum $b\bar{b}\gamma\gamma$ cross
section is calculated and compared with the ATLAS observed limits and for the ATLAS observed limits which are violated by the maximum $b\bar{b}\gamma\gamma$ cross
sections, the distribution of $b\bar{b}\gamma\gamma$ cross section are plotted.

## calculating scripts
`twoD_AtlasLimGS_configure.py`: produces the directory structure in the path `pathOutputParent` where a directory is created for each mass point with the name e.g.
`X170_S30` from the ATLAS limit mass points. The HTCondor scripts are found in `pathCondorSubmitAndExecute`, by running the HTCondor scripts a job will be created
for each directory in `pathOutputParent` where the TRSM executable will exclude model parameters (out of the 100000) if they fail HiggsBounds, HiggsSignals and the
theoretical constraints and calculates various observables from the surviving sets of model parameters. The path to the TRSM executable needs to be provided in `pathTRSM`
where the constraints can be modified by changing the values of `BFB`, `Uni`, `STU`, `Higgs`.

`twoD_AtlasLimGS_compile.py`: after the HTCondor jobs are finished, `twoD_AtlasLimGS_compile.py` finds the maximum `b\bar{b}\gamma\gamma` cross section for each mass
point from the surviving sets of model parameters and the number of exclusions by the ATLAS observed limit and number of surviving models from the `ScannerS` constraints
and more.

## plotting scripts

`twoD_AtlasLimGS_survivedConstr_plot.py`: plots the fraction of surviving models from `ScannerS` constraints. Figures can be found in [plots](plots)

`twoD_AtlasLimGS_plot.py`: plots the maximum $b\bar{b}\gamma\gamma$ cross section from the surviving models. Figures can be found in [plots](plots)

`twoD_AtlasLimGS_dist_plot.py`: plots the distribution of $b\bar{b}\gamma\gamma$ cross section of the mass points where the maximum $b\bar{b}\gamma\gamma$ cross section
violates the ATLAS observed limits (see the figures from `twoD_AtlasLimGS_plot.py`).

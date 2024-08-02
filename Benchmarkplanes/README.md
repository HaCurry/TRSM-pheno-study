# TABLE OF CONTENTS IN THIS DIRECTORY

This directory plots the $b\bar{b}\gamma\gamma$ cross sections using BP2 and BP3

# calculating scripts

`twoD_BP_configure.py`: can be either run locally or through HTCondor. If run on HTCondor please edit the path `executable` in the submit script `condorSubmit.sub`
and the path `pathRepo` in `pathRepo`. Additionally the path to the TRSM executable `pathTRSM` and the path to the repo `pathRepo` needs to provided in
`twoD_BP_configure.py`.

# plotting scripts

`twoD_BP_NPSM_plot.py`: plots the $b\bar{b}\gamma\gamma$ cross section ($\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma))$, $\sigma(gg\to h_{3} \to h_{1}
(\gamma\gamma) h_{2}(b\bar{b}))$) using BP2 and BP3. Figures can be found in [plots](plots).

`twoD_BP_NPSM_ratio_plot.py`: plots the ratio of the two modes $\sigma(gg\to h_{3} \to h_{1}(b\bar{b}) h_{2}(\gamma\gamma))/\sigma(gg\to h_{3} \to h_{1}(\gamma\gamma)
h_{2}(b\bar{b}))$ in BP2 and BP3. Figures can be found in [plots](plots).

`twoD_BP_NP_plot.py`: plots the branching ratio $\text{BR}(h_{3} \to h_{1} h_{2})$ and the cross section $\sigma(gg \to h_{3} \to h_{1} h_{2})$ using BP2 and BP3. Figures
can be found in [plots](plots).

`twoD_BP_NWA_plot.py`: plots the relative widths of the TRSM Higgs bosons $h_{1}$, $h_{2}$, $h_{3}$ using BP2 and BP3. Figures can be found in [plots](plots).

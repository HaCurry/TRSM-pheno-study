import json
import argparse
import glob
import pandas
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl



def XNP_rt(BPdirectory, axes1, axes2, axes3, physics):
    
    df = pandas.read_table(BPdirectory, index_col = 0)
    # PC
    # df = pandas.read_table ( r"\\wsl.localhost\Ubuntu\home\iram\scannerS\ScannerS-master\build\output_file.tsv" , index_col =0)
    
    mH1_H1H2 = [i for i in df[axes1]]
    mH2_H1H2 = [i for i in df[axes2]]
    mH3_H1H2 = [i for i in df[axes3]]
    
    b_H3_H1H2 = [i for i in df["b_H3_H1H2"]]
    b_H3_H1H1 = [i for i in df["b_H3_H1H1"]]
    b_H3_H2H2 = [i for i in df["b_H3_H2H2"]]
    
    if (physics == "XSH") or (physics == "XSS") or (physics == "XHH"):
        H1H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, b_H3_H1H2])
        H1H1 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, b_H3_H1H1])
        H2H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, b_H3_H2H2])
        
        return H1H2, H1H1, H2H2
    
    x_H3_gg_H1H2 = [i for i in df["x_H3_gg"]]
    x_H3_gg_H1H1 = x_H3_gg_H1H2.copy()
    x_H3_gg_H2H2 = x_H3_gg_H1H2.copy()    
    
    if (physics == "ppXSH") or (physics == "ppXSS") or (physics == "ppXHH"):
        ggF_xs_SM_Higgs = 31.02 * 10**(-3)
        
        # rescaled cross-section
        pp_X_H1H2 = [(b_H3_H1H2[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
        H1H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H1H2])
        
        pp_X_H1H1 = [(b_H3_H1H1[i] * x_H3_gg_H1H1[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H1))]
        H1H1 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H1H1])
        
        pp_X_H2H2 = [(b_H3_H2H2[i] * x_H3_gg_H2H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H2H2))]
        H2H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H2H2])
        
        return H1H2, H1H1, H2H2
        
    else:
        raise Exception("No physics chosen in XNP_rt")




def ppXNPSM_massfree(BPdirectory, axes1, axes2, axes3, SM1, SM2):
    df = pandas.read_table(BPdirectory)#, index_col = 0)
    
    mH1_H1H2 = [i for i in df[axes1]] #"mH1"
    mH2_H1H2 = [i for i in df[axes2]] #"mH2"
    mH3_H1H2 = [i for i in df[axes3]] #"mH3"
    
    mH1_H1H1 = mH1_H1H2.copy()
    mH2_H1H1 = mH2_H1H2.copy()
    mH3_H1H1 = mH3_H1H2.copy()
    
    mH1_H2H2 = mH1_H1H2.copy()
    mH2_H2H2 = mH2_H1H2.copy()
    mH3_H2H2 = mH3_H1H2.copy()
    
    mH1_x_H3_gg = mH1_H1H2.copy()
    mH2_x_H3_gg = mH2_H1H2.copy()
    mH3_x_H3_gg = mH3_H1H2.copy()
    
    b_H3_H1H2 = [i for i in df["b_H3_H1H2"]]
    b_H3_H1H1 = [i for i in df["b_H3_H1H1"]]
    b_H3_H2H2 = [i for i in df["b_H3_H2H2"]]
    x_H3_gg_H1H2 = [i for i in df["x_H3_gg"]]
    x_H3_gg_H1H1 = x_H3_gg_H1H2.copy()
    x_H3_gg_H2H2 = x_H3_gg_H1H2.copy()
    
    b_H1_bb     = [i for i in df["b_H1_" + SM1]]        #"b_H1_bb"
    b_H1_gamgam = [i for i in df["b_H1_" + SM2]]        #"b_H1_gamgam"
    b_H2_bb     = [i for i in df["b_H2_" + SM1]]        #"b_H2_bb"
    b_H2_gamgam = [i for i in df["b_H2_" + SM2]]        #"b_H2_gamgam"
    
    epsilon = 10**(-6)
    
    check = ( len(mH1_H1H2 ) + len(mH2_H1H2) + len(mH3_H1H2) \
        + len(mH1_H1H1) + len(mH2_H1H1) + len(mH3_H1H1) \
        + len(mH1_H2H2) + len(mH2_H2H2) + len(mH3_H2H2) \
        + len(mH1_x_H3_gg) + len(mH2_x_H3_gg) + len(mH3_x_H3_gg) \
        + len(b_H3_H1H2) + len(b_H3_H1H1) + len(b_H3_H2H2) + len(x_H3_gg_H1H2) + len(x_H3_gg_H1H1) + len(x_H3_gg_H2H2) \
        + len(b_H1_bb) + len(b_H1_gamgam) + len(b_H2_bb) + len(b_H2_gamgam) ) / ( 22 *len(df["Unnamed: 0"]) )
    
    if  abs( check - 1 )  > + epsilon:
        raise Exception('length of lists not equal in ppXNPSM_massfree')
    
    b_H1_bb_H2_gamgam = [b_H1_bb[i] * b_H2_gamgam[i] for i in range(len(b_H1_bb))]
    b_H1_gamgam_H2_bb = [b_H2_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
    
    b_H1H2_bbgamgam = [b_H1_bb_H2_gamgam[i] + b_H1_gamgam_H2_bb[i] for i in range(len(b_H1_bb))]
    b_H1H1_bbgamgam = [b_H1_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
    b_H2H2_bbgamgam = [b_H2_bb[i] * b_H2_gamgam[i] for i in range(len(b_H2_bb))]
    
    
#    ggF_bbgamgam_xs_SM_Higgs = (31.02 * 10**(-3)) * 0.0026  
    # ggF_bbgamgam_xs_SM_Higgs = (31.02 * 10**(-3)) * (10**(-2)*0.028)  
    ggF_bbgamgam_xs_SM_Higgs = 1 
    
    # rescaled cross-section
    pp_X_H1H2_bbgamgam = [(b_H1H2_bbgamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H1H2_bbgamgam))]
    # pp_X_H1H2_bbgamgam = [x_H3_gg_H1H2[i] *  b_H3_H1H2[i] for i in range(len(b_H1H2_bbgamgam))]
    
    pp_X_H1H1_bbgamgam = [(b_H1H1_bbgamgam[i] * x_H3_gg_H1H1[i] * b_H3_H1H1[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H1H1_bbgamgam))]
    # pp_X_H1H1_bbgamgam = [ x_H3_gg_H1H1[i] * b_H3_H1H1[i] for i in range(len(b_H1H1_bbgamgam))]
    
    pp_X_H2H2_bbgamgam = [(b_H2H2_bbgamgam[i] * x_H3_gg_H2H2[i] * b_H3_H2H2[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H2H2_bbgamgam))]
    # pp_X_H2H2_bbgamgam = [x_H3_gg_H2H2[i] * b_H3_H2H2[i] for i in range(len(b_H2H2_bbgamgam))]
    
    
    pp_X_H1_bb_H2_gamgam = [b_H1_bb_H2_gamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
    pp_X_H1_gamgam_H2_bb = [b_H1_gamgam_H2_bb[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
    
    
    H1H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H1H2_bbgamgam, pp_X_H1_bb_H2_gamgam, pp_X_H1_gamgam_H2_bb])
    H1H1 = np.array([mH1_H1H1, mH2_H1H1, mH3_H1H1, pp_X_H1H1_bbgamgam])
    H2H2 = np.array([mH1_H2H2, mH2_H2H2, mH3_H2H2, pp_X_H2H2_bbgamgam])
    
    return H1H2, H1H1, H2H2



#BP2_H1H2, BP2_H1H1, BP2_H2H2 = XNP_rt(r"/home/iram/scannerS/ScannerS-master/build/BP2output/BP2_output_file.tsv", "mH1", "mH2", "mH3", "XSH")

BP2_H1H2, BP2_H1H1, BP2_H2H2 = ppXNPSM_massfree(r"/home/iram/scannerS/ScannerS-master/build/BP2output/BP2_output_file.tsv", "mH1", "mH2", "mH3", "bb", "gamgam")

BP3_H1H2, BP2_H1H1, BP2_H2H2 = ppXNPSM_massfree(r"/home/iram/scannerS/ScannerS-master/build/BP3output/BP3_output_file.tsv", "mH1", "mH2", "mH3", "bb", "gamgam")



## BP2 ##
TRSM_BP2_ms = BP2_H1H2[0]
TRSM_BP2_mx = BP2_H1H2[2]
TRSM_BP2_z = BP2_H1H2[4]

nInterp = 500
TRSM_BP2_ms_i, TRSM_BP2_mx_i = np.linspace(TRSM_BP2_ms.min(), TRSM_BP2_ms.max(), nInterp), np.linspace(TRSM_BP2_mx.min(), TRSM_BP2_mx.max(), nInterp)
TRSM_BP2_ms_i, TRSM_BP2_mx_i = np.meshgrid(TRSM_BP2_ms_i, TRSM_BP2_mx_i)

TRSM_BP2_z_i = scipy.interpolate.griddata((TRSM_BP2_ms, TRSM_BP2_mx), TRSM_BP2_z, (TRSM_BP2_ms_i, TRSM_BP2_mx_i), method='linear')

plt.imshow(TRSM_BP2_z_i, vmin=TRSM_BP2_z.min(), vmax=TRSM_BP2_z.max(), origin='lower',
                extent=[TRSM_BP2_ms.min(), TRSM_BP2_ms.max(), TRSM_BP2_mx.min(), TRSM_BP2_mx.max()], aspect='auto')

plt.colorbar(label =r'$\sigma( pp \rightarrow X)\times$ BR$ (X \rightarrow SH  \rightarrow bb \gamma \gamma)$ [pb]')

plt.title(r"BP2")

plt.show()
plt.close()






## BP3 ##
TRSM_BP3_ms = BP3_H1H2[1]
TRSM_BP3_mx = BP3_H1H2[2]
TRSM_BP3_z = BP3_H1H2[4]

nInterp = 500
TRSM_BP3_ms_i, TRSM_BP3_mx_i = np.linspace(TRSM_BP3_ms.min(), TRSM_BP3_ms.max(), nInterp), np.linspace(TRSM_BP3_mx.min(), TRSM_BP3_mx.max(), nInterp)
TRSM_BP3_ms_i, TRSM_BP3_mx_i = np.meshgrid(TRSM_BP3_ms_i, TRSM_BP3_mx_i)

TRSM_BP3_z_i = scipy.interpolate.griddata((TRSM_BP3_ms, TRSM_BP3_mx), TRSM_BP3_z, (TRSM_BP3_ms_i, TRSM_BP3_mx_i), method='linear')

plt.imshow(TRSM_BP3_z_i, vmin=TRSM_BP3_z.min(), vmax=TRSM_BP3_z.max(), origin='lower',
                extent=[TRSM_BP3_ms.min(), TRSM_BP3_ms.max(), TRSM_BP3_mx.min(), TRSM_BP3_mx.max()], aspect='auto')

plt.colorbar(label =r'$\sigma( pp \rightarrow X)\times$ BR$ (X \rightarrow SH  \rightarrow bb \gamma \gamma)$ [pb]')

plt.title(r"BP3")

plt.show()
plt.close()






## EXCLUSION LIMITS ##
limits = pandas.read_json('Atlas2023Limits.json')

mx, ms, limit_obs, limit_exp = [], [], [], []

for element in limits:
    mx.append((limits[element])[0])
    ms.append((limits[element])[1])
#    limit_exp.append((limits[element])[2] * 10 **(-3))
#    limit_obs.append((limits[element])[3] * 10 **(-3))
    limit_exp.append((limits[element])[2] * 10 **(-3))
    limit_obs.append((limits[element])[3] * 10 **(-3))

mx = np.array(mx)
ms = np.array(ms)
limit_exp = np.array(limit_exp)
limit_obs = np.array(limit_obs)


## BP2 min max
BP2_x_min, BP2_x_max = TRSM_BP2_ms.min(), TRSM_BP2_ms.max()
BP2_y_min, BP2_y_max = TRSM_BP2_mx.min(), TRSM_BP2_mx.max()


## BP3 min max
BP3_x_min, BP3_x_max = TRSM_BP3_ms.min(), TRSM_BP3_ms.max()
BP3_y_min, BP3_y_max = TRSM_BP3_mx.min(), TRSM_BP3_mx.max()


## BP2 Meshgrids
BP2_xi, BP2_yi = np.linspace(BP2_x_min, BP2_x_max, nInterp), np.linspace(BP2_y_min, BP2_y_max, nInterp)
BP2_grid_x, BP2_grid_y = np.meshgrid(BP2_xi, BP2_yi)


## BP3 Meshgrids
BP3_xi, BP3_yi = np.linspace(BP3_x_min, BP3_x_max, nInterp), np.linspace(BP3_y_min, BP3_y_max, nInterp)
BP3_grid_x, BP3_grid_y = np.meshgrid(BP3_xi, BP3_yi)


## BP2Interpolate the limits on the grid
BP2_grid_limit = scipy.interpolate.griddata((ms, mx), limit_obs, (BP2_grid_x, BP2_grid_y), method='cubic')


## BP3Interpolate the limits on the grid
BP3_grid_limit = scipy.interpolate.griddata((ms, mx), limit_obs, (BP3_grid_x, BP3_grid_y), method='cubic')


## BP2 EXCLUSION LIMITS PLOTTING ##
plt.imshow(BP2_grid_limit, vmin=limit_obs.min(), vmax=limit_obs.max(), origin='lower',
#                extent=[ms.min(), ms.max(), mx.min(), mx.max()], aspect='auto')
                extent=[BP2_x_min, BP2_x_max, BP2_y_min, BP2_y_max], aspect='auto')
plt.xlim(BP2_x_min, BP2_x_max)
plt.ylim(BP2_y_min, BP2_y_max)

plt.title(r'BP2 Observed limits')

plt.colorbar(label =r'$\sigma( pp \rightarrow X)\times$ BR$ (X \rightarrow SH  \rightarrow bb \gamma \gamma)$ [pb]')

plt.show()
plt.close()


## BP3 EXCLUSION LIMITS PLOTTING ##
plt.imshow(BP3_grid_limit, vmin=limit_obs.min(), vmax=limit_obs.max(), origin='lower',
                extent=[ms.min(), ms.max(), mx.min(), mx.max()], aspect='auto')
plt.xlim(BP3_x_min, BP3_x_max)
plt.ylim(BP3_y_min, BP3_y_max)

plt.title(r'BP3 Observed limits')

plt.colorbar(label =r'$\sigma( pp \rightarrow X)\times$ BR$ (X \rightarrow SH  \rightarrow bb \gamma \gamma)$ [pb]')

plt.show()
plt.close()


## BP2 EXCLUSION REGIONS ##
#BP2_with_exclusion = np.where(TRSM_BP2_z_i > BP2_grid_limit, TRSM_BP2_z_i, np.nan)

#plt.imshow(BP2_with_exclusion, vmin=TRSM_BP2_z.min(), vmax=TRSM_BP2_z.max(), origin='lower',
#                extent=[TRSM_BP2_ms.min(), TRSM_BP2_ms.max(), TRSM_BP2_mx.min(), TRSM_BP2_mx.max()], aspect='auto')
#plt.colorbar(label =r'$\sigma( pp \rightarrow X)\times$ BR$ (X \rightarrow SH  \rightarrow bb \gamma \gamma)$ [pb]')

BP2_with_exclusion = np.where(TRSM_BP2_z_i < BP2_grid_limit, TRSM_BP2_z_i, np.nan)

plt.imshow(BP2_with_exclusion, vmin=TRSM_BP2_z.min(), vmax=TRSM_BP2_z.max(), origin='lower',
                extent=[BP2_x_min , BP2_x_max, BP2_y_min, BP2_y_max], aspect='auto')
plt.colorbar(label =r'$\sigma( pp \rightarrow X)\times$ BR$ (X \rightarrow SH  \rightarrow bb \gamma \gamma)$ [pb]')

plt.title(r"BP2")
plt.show()
plt.close()


## BP3 EXCLUSION REGIONS ##
BP3_with_exclusion = np.where(TRSM_BP3_z_i < BP3_grid_limit, TRSM_BP3_z_i, np.nan)

plt.imshow(BP3_with_exclusion, vmin=TRSM_BP3_z.min(), vmax=TRSM_BP3_z.max(), origin='lower',
                extent=[BP3_x_min , BP3_x_max, BP3_y_min, BP3_y_max], aspect='auto')
plt.colorbar(label =r'$\sigma( pp \rightarrow X)\times$ BR$ (X \rightarrow SH  \rightarrow bb \gamma \gamma)$ [pb]')

plt.title(r"BP3")
plt.show()
plt.close()



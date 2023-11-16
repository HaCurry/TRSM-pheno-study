# -*- coding: utf-8 -*-
import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.interpolate
from scipy.interpolate import CubicSpline
mpl.rcParams.update(mpl.rcParamsDefault)
from numpy import ma
from subprocess import call
import subprocess




def pointfinder(epsilon, pointS, pointX, listS, listX, br):
    S = pointS
    X = pointX
    index = 0
    print(len(listS), len(listX), len(br))
    for i in range(len(br)):
        testS = (listS)[i]
        testX = (listX)[i]
        if abs(S - testS) < epsilon and abs(X - testX) < epsilon:
            epsilon = max(abs(S - testS), abs(X - testX))
            index = i
    print(index, (listS)[index], (listX)[index], (br)[index])
    return (listS)[index], (listX)[index], (br)[index]




def pointGen(BP, region, size, generator):
    
    def random(ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition):
        ms = np.random.uniform(ms_lowerbound, ms_upperbound, 1)
        mx = np.random.uniform(mx_lowerbound, mx_upperbound, 1)
        if condition(ms, mx):
            point = [ms, mx]
            return point
        else:
            point = random(ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition)
            return point
    
    def BP2conditionRegion1(ms, mx):
        if (5.2 * ms + 125.09 > mx):
            return True
        else: 
            return False
    
    def BP2conditionRegion2(ms, mx):
        if (5.2 * ms + 125.09 > mx) and (mx > ms + 125.09):
            return True
        else: 
            return False
    
    def BP2conditionRegion3(ms, mx):
        if (ms + 125.09 > mx) and (2 * ms < mx):
            return True
        else: 
            return False

    def BP3conditionRegion1(ms, mx):
        if (mx > 2 * ms) and (3.27 * ms + 78 > mx) and (-0.34 * ms + 641 > mx) and (mx > 2 * ms):
            return True
        else:
            return False

    def BP3conditionRegion2(ms, mx):
        if (2 * ms > mx) and ((-0.72) * ms + 745 > mx) and (mx > ms + 125.09 ):
            return True
        else:
            return False

    def BP3conditionRegion3(ms, mx):
        if (ms + 125.09 > mx) and ((-1.29) * ms + 949 > mx) and (mx > ms):
            return True
        else:
            return False

    pointlist = []
    
    if BP == 'BP2':
    
        if region == 1:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 1, 124, 250, 500, BP2conditionRegion1
            
        elif region == 2:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 1, 124, 126, 250, BP2conditionRegion2
            
        elif region == 3:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 1, 124, 126, 250, BP2conditionRegion3

        else:
            raise Exception('No region chosen')
    
    elif BP == 'BP3':
        
        if region == 1:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 126, 290, 255, 650, BP3conditionRegion1
        
        elif region == 2:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 126, 380, 255, 600, BP3conditionRegion2
            
        elif region == 3:
            ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition = 126, 500, 255, 550, BP3conditionRegion3
        
        else:
            raise Exception('No region chosen')
    
    else:
        raise Exception('No BP chosen')
    
    if generator == 'random':
        
        for i in range(size):
            point = random(ms_lowerbound, ms_upperbound, mx_lowerbound, mx_upperbound, condition)
            pointlist.append(point)
        return np.array(pointlist)
    
    elif generator == 'grid':
        
        mslist = np.linspace(ms_lowerbound, ms_upperbound, size)
        mxlist = np.linspace(mx_lowerbound, mx_upperbound, size)
        
        for i in range(size):
            for j in range(size):
                if condition(mslist[i], mxlist[j]):
                    pointlist.append([mslist[i], mxlist[j]])
                else:
                    continue
        return np.array(pointlist)
    
    else:
        raise Exception('No generator chosen')



def plotmarkerAuto2(markers, visible, decimals, fsize, x, y, n):
    for i in range(len(markers)):
        dudS, dudX, br = pointfinder(5, (markers[i])[0], (markers[i])[1], x, y, n)
        pointS, pointX = (markers[i])[0], (markers[i])[1]
        plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        if visible == True:
            plt.plot(pointS, pointX, marker = 'o', mfc = 'none', color = 'r')




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
        
    # Note, only ppXSHNP is supported, the rest are under development
    elif (physics == "ppXSHNP") or (physics == "ppXSHNP") or (physics == "ppXSHNP"):
        
        SM1, SM2 = "bb", "gamgam" # This is here temporarily so that in the future the user can choose SM1, SM2
        
        b_H1_bb     = [i for i in df["b_H1_" + SM1]]        #"b_H1_bb"
        b_H1_gamgam = [i for i in df["b_H1_" + SM2]]        #"b_H1_gamgam"
        b_H2_bb     = [i for i in df["b_H2_" + SM1]]        #"b_H2_bb"
        b_H2_gamgam = [i for i in df["b_H2_" + SM2]]        #"b_H2_gamgam"
        
        b_H1_bb_H2_gamgam = [b_H1_bb[i] * b_H2_gamgam[i] for i in range(len(b_H1_bb))]
        b_H1_gamgam_H2_bb = [b_H2_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
        
        b_H1H2_bbgamgam = [b_H1_bb_H2_gamgam[i] + b_H1_gamgam_H2_bb[i] for i in range(len(b_H1_bb))]
        # b_H1H2_bbgamgam = [b_H1_bb[i] * b_H2_gamgam[i] + b_H2_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
        b_H1H1_bbgamgam = [b_H1_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
        b_H2H2_bbgamgam = [b_H2_bb[i] * b_H2_gamgam[i] for i in range(len(b_H2_bb))]
        
#        For future customization of the user
#        ggF_bbgamgam_xs_SM_Higgs = normalization
        # ggF_bbgamgam_xs_SM_Higgs = (31.02 * 10**(-3)) * 0.0026  
        # ggF_bbgamgam_xs_SM_Higgs = (31.02 * 10**(-3)) * (10**(-2)*0.028)  
        ggF_bbgamgam_xs_SM_Higgs = 1 
        
        # rescaled cross-section
        pp_X_H1H2_bbgamgam = [(b_H1H2_bbgamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H1H2_bbgamgam))]
        
        pp_X_H1H1_bbgamgam = [(b_H1H1_bbgamgam[i] * x_H3_gg_H1H1[i] * b_H3_H1H1[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H1H1_bbgamgam))]
        
        pp_X_H2H2_bbgamgam = [(b_H2H2_bbgamgam[i] * x_H3_gg_H2H2[i] * b_H3_H2H2[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H2H2_bbgamgam))]
        
        
        pp_X_H1_bb_H2_gamgam = [b_H1_bb_H2_gamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
        pp_X_H1_gamgam_H2_bb = [b_H1_gamgam_H2_bb[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
        
            
        H1H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H1H2_bbgamgam, pp_X_H1_bb_H2_gamgam, pp_X_H1_gamgam_H2_bb])
        H1H1 = np.array([mH1_H1H1, mH2_H1H1, mH3_H1H1, pp_X_H1H1_bbgamgam])
        H2H2 = np.array([mH1_H2H2, mH2_H2H2, mH3_H2H2, pp_X_H2H2_bbgamgam])
        
        return H1H2, H1H1, H2H2
        
    else:
        raise Exception("No physics chosen in XNP_rt")




def massplots(BP, physics, userParametersDict, directory, filename):

    if BP == "BP2":
        H1H2, H1H1, H2H2 = XNP_rt(r"/home/iram/scannerS/ScannerS-master/build/BP2output/BP2_output_file.tsv", "mH1", "mH2", "mH3", physics)

    elif BP == "BP3":    
        H1H2, H1H1, H2H2 = XNP_rt(r"/home/iram/scannerS/ScannerS-master/build/BP3output/BP3_output_file.tsv", "mH1", "mH2", "mH3", physics)
    
    else:
        raise Exception("No BP chosen in massplots")


    if physics == "XSH":
        
        if BP == "BP2":
            x, y, n = H1H2[0], H1H2[2], H1H2[3]
            title = filename + "BP2: $BR(X\\to SH)$"
        
        elif BP == "BP3":
            x, y, n = H1H2[1], H1H2[2], H1H2[3]
            title = filename + "BP3: $BR(X\\to SH)$"

    elif physics == "ppXSH" or "ppXSHNP":

        if BP == "BP2":
            x, y, n = H1H2[0], H1H2[2], H1H2[3]
            title = filename + "BP2: $\sigma(pp \\to X\\to SH)$"
        
        elif BP == "BP3":
            x, y, n = H1H2[1], H1H2[2], H1H2[3]
            title = filename + "BP3: $\sigma(pp \\to X\\to SH)$"

    elif physics == "XHH":
        if BP == "BP2":
            x, y, n = H2H2[0], H2H2[2], H2H2[3]
            plt.title(filename + "BP2: $BR(pp \\to X\\to HH)$")
        
        elif BP == "BP3":
            x, y, n = H1H1[1], H1H1[2], H1H1[3]
            title = filename + "BP3: $BR(pp \\to X\\to HH)$"

    elif physics == "ppXHH":
        if BP == "BP2":
            x, y, n = H2H2[0], H2H2[2], H2H2[3]
            title = filename + "BP2: $\sigma(pp \\to X\\to HH)$"
        
        elif BP == "BP3":
            x, y, n = H1H1[1], H1H1[2], H1H1[3]
            title = filename + "BP3: $\sigma(pp \\to X\\to HH)$"

    elif physics == "XSS":
   
        if BP == "BP2":
            x, y, n = H1H1[0], H1H1[2], H1H1[3]
            title = filename + "BP2: $BR(X\\to SS)$"

        elif BP == "BP3":
            x, y, n = H2H2[1], H2H2[2], H2H2[3]
            title = filename + "BP3: $BR(X\\to SS)$"

    elif physics == "ppXSS":

        if BP == "BP2":
            x, y, n =  H1H1[0], H1H1[2], H1H1[3]
            title = filename + "BP2: $\sigma(X\\to SS)$"

        elif BP == "BP3":
            x, y, n = H2H2[1], H2H2[2], H2H2[3]
            title = filename + "BP3: $\sigma(X\\to SS)$"



    elif physics == "ppXNPSM":
        raise Exception("ppXNPSM is in work in progress not finished")
    
    else:
        raise Exception("No physics chosen for massplots")
        
    
    plt.title(title)
    x, y, z = np.asarray(x), np.asarray(y), np.asarray(n)
        
    if BP == "BP2":
        plt.xlim(0,124)        
        plt.ylim(124,500)
        
        boundaryx = np.linspace(0, 600)
        plt.plot(boundaryx, np.array([2* 125.09 for i in boundaryx]), label = r'$m_{X} = 2 \cdot m_{H}$')
        # plt.text(3, 235, r'$M_{X} = 2\cdot M_{H}$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

        plt.plot(boundaryx, boundaryx + 125.09, label = r'$M_{X} = M_{S} + M_{H}$')
        # plt.text(26, 134, r'$M_{X} = M_{S} + M_{H}$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))#, rotation=18)

        plt.plot(boundaryx, 2*boundaryx, label = r'$m_{X} = 2 \cdot m_{S}$')
        # plt.text(75, 134, r'$M_{X} = 2\cdot M_{S}$', size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))#, rotation=32)
        
    elif BP == "BP3":
        plt.xlim(126, 500)
        plt.ylim(255, 650)
        
        boundaryx = np.linspace(120, 500)
        plt.plot(boundaryx, 2*boundaryx, color = 'C0', label = r'$m_{X} = 2m_{S}$')
        # plt.text(298, 575, r'$M_{X} = 2\cdot M_{S}$', size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

        plt.plot(boundaryx, boundaryx + 125.09, color = 'C1', label = r'$m_{X} = m_{S} + m_H$')
        # plt.text(337, 445, r'$M_{X} = M_{S} + M_{H}$', size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))

        plt.plot(boundaryx, boundaryx, color = 'C2', label = r'$m_{X} = m_{S}$')
        # plt.text(353, 336, r'$M_{X} = M_{S}$', size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))
    
    # code taken from stackexchange
    nInterp = 500
    xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    xi, yi = np.meshgrid(xi, yi)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    
    colorbarlabel = {"XSH": "$BR(X \\to SH)$", "ppXSH": "$\sigma(pp \\to X \\to SH)$", "XHH": "$BR(X \\to HH)$", "ppXHH" : "$\sigma(pp \\to X \\to HH)$", "XSS": "$BR(X \\to SS)$", "ppXSS" : "$\sigma(pp \\to X \\to SS)$"}
    
    plt.colorbar(label = BP + ": " + colorbarlabel[physics])
    
    plt.xlabel(r"$M_{S}$ [GeV]")
    plt.ylabel(r"$M_{X}$ [GeV]")    

    visibleMarkers, decimals, fontsize = True, 4, 8
    if isinstance(userParametersDict, dict) == True:
        plotmarkerAuto2([ [userParametersDict["ms"], userParametersDict["mx"]] ], visibleMarkers, decimals, fontsize, x, y, n)
    elif isinstance(userParametersDict, list) == True:
        points = []
        for dictElement in userParametersDict:
            # ms, mx = dictElement["ms"], dictElement["mx"]
            # points.append([ms, mx])
            points.append([int(dictElement["ms"]), int(dictElement["mx"])])
        plotmarkerAuto2(points, visibleMarkers, decimals, fontsize, x, y, n)
    
    location = directory + "/" + filename 
    plt.savefig(location + " " + physics + "massplot")




def dataPuller(BP, physics, userParametersDict, axis):
    
    if BP == "BP2":
        programParametersDict = { 
        "mHa_lb": 80, "mHa_ub": 80, "mHb_lb": 125.09, "mHb_ub": 125.09, "mHc_lb": 375, "mHc_ub": 375, 
        "ths_lb": 1.352, "ths_ub": 1.352, "thx_lb": 1.175, "thx_ub": 1.175, "tsx_lb": -0.407, "tsx_ub": -0.407, 
        "vs_lb": 120, "vs_ub": 120, "vx_lb": 890, "vx_ub": 890, 
        "points": 100
        }
        
        programParametersDict["mHa_lb"] = userParametersDict["ms"]
        programParametersDict["mHa_ub"] = userParametersDict["ms"]
        
        programParametersDict["mHc_lb"] = userParametersDict["mx"]
        programParametersDict["mHc_ub"] = userParametersDict["mx"]
        
        userParametersKeys = userParametersDict.keys()
        
    elif BP == "BP3":
        programParametersDict = { 
        "mHa_lb": 125.09, "mHa_ub": 125.09, "mHb_lb": 200, "mHb_ub": 200, "mHc_lb": 400, "mHc_ub": 400, 
        "ths_lb": -0.129, "ths_ub": -0.129, "thx_lb": 0.226, "thx_ub": 0.226, "tsx_lb": -0.899, "tsx_ub": -0.899, 
        "vs_lb": 140, "vs_ub": 140, "vx_lb": 100, "vx_ub": 100, 
        "points": 100
        }
        
        programParametersDict["mHb_lb"] = userParametersDict["ms"]
        programParametersDict["mHb_ub"] = userParametersDict["ms"]

        programParametersDict["mHc_lb"] = userParametersDict["mx"]
        programParametersDict["mHc_ub"] = userParametersDict["mx"]

        userParametersKeys = userParametersDict.keys()

    else:
        raise Exception("No benchmarkplane chosen")

    
    for key in userParametersKeys:
        if key == "ms" or key == "mx":
            continue
        else:
            programParametersDict[key] = userParametersDict[key]
#    if len(arguments) != 17:
#        print(len(arguments))
#        raise Exception("Few arguments")
    
    toShell = ["/bin/bash", "regionTesting.sh"]

    programParametersKeys = programParametersDict.keys()

    for key in programParametersKeys:
        toShell.append(str(programParametersDict[key]))
    
    #code from stackexchange: https://stackoverflow.com/a/75843787/17456342

#    try:
    subprocess.run(toShell, timeout = 120)
#    except subprocess.TimeoutExpired:
#        print('timed out!')
    
    df = pandas.read_table(r"regionTesting.tsv")
    
    mH1_H1H2 = np.array([i for i in df[axis]])
    mH2_H1H2 = np.array([i for i in df["mH2"]])
    mH3_H1H2 = np.array([i for i in df["mH3"]])

#    mH1_H1H1 = mH1_H1H2.copy()
#    mH2_H1H1 = mH2_H1H2.copy()
#    mH3_H1H1 = mH3_H1H2.copy()

#    mH1_H2H2 = mH1_H1H2.copy()
#    mH2_H2H2 = mH2_H1H2.copy()
#    mH3_H2H2 = mH3_H1H2.copy()

    b_H3_H1H2 = np.array([i for i in df["b_H3_H1H2"]])
    b_H3_H1H1 = np.array([i for i in df["b_H3_H1H1"]])
    b_H3_H2H2 = np.array([i for i in df["b_H3_H2H2"]])

    idx = np.argsort(mH1_H1H2)
    mH1_H1H2  = mH1_H1H2[idx]
    
    
    if physics == "XSH":
        b_H3_H1H2 = b_H3_H1H2[idx]
        return mH1_H1H2, b_H3_H1H2
            
    elif physics == "XHH":
        if BP == "BP2":    
            b_H3_H2H2 = b_H3_H2H2[idx]
            return mH1_H1H2, b_H3_H2H2
        elif BP == "BP3":
            b_H3_H1H1 = b_H3_H1H1[idx]
            return mH1_H1H2, b_H3_H1H1
        
    elif physics == "XSS":
        if BP == "BP2":
            b_H3_H1H1 = b_H3_H1H1[idx]
            return mH1_H1H2, b_H3_H1H1
        elif BP == "BP3":
            b_H3_H2H2 = b_H3_H2H2[idx]
            return mH1_H1H2, b_H3_H2H2

    
    x_H3_gg_H1H2 = np.array([i for i in df["x_H3_gg"]])
    x_H3_gg_H1H2 = x_H3_gg_H1H2[idx]
#    x_H3_gg_H1H1 = x_H3_gg_H1H2.copy()
#    x_H3_gg_H2H2 = x_H3_gg_H1H2.copy()

    # rescaled SM dihiggs cross-section (ggF):
    # https://cds.cern.ch/record/2764447/files/ATL-PHYS-SLIDE-2021-092.pdf
    ggF_xs_SM_Higgs = 31.02 * 10**(-3)
    
    if physics == "ppXSH":
        b_H3_H1H2 = b_H3_H1H2[idx]
        pp_X_H1H2 = np.array([(b_H3_H1H2[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H2))])
#        pp_X_H1H2 = np.array([b_H3_H1H2[i] for i in range(len(b_H3_H1H2))])
        return mH1_H1H2, pp_X_H1H2
    
    elif physics == "ppXHH":
        if BP == "BP2":
            b_H3_H2H2 = b_H3_H2H2[idx]
            pp_X_H2H2 = np.array([(b_H3_H2H2[i] * x_H3_gg_H2H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H2H2))])
            return mH1_H1H2, pp_X_H2H2
        elif BP == "BP3":
            b_H3_H1H1 = b_H3_H1H1[idx]
#            pp_X_H1H1 = np.array([(b_H3_H1H1[i] * x_H3_gg_H1H1[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H1))])
            pp_X_H1H1 = np.array([(b_H3_H1H1[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H1))])
            return mH1_H1H2, pp_X_H1H1

    elif physics == "ppXSS":
        if BP == "BP2":
            b_H3_H1H1 = b_H3_H1H1[idx]
#            pp_X_H1H1 = np.array([(b_H3_H1H1[i] * x_H3_gg_H1H1[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H1))])
            pp_X_H1H1 = np.array([(b_H3_H1H1[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H1))])
            return mH1_H1H2, pp_X_H1H1
        elif BP == "BP3":
            b_H3_H2H2 = b_H3_H2H2[idx]
#            pp_X_H2H2 = np.array([(b_H3_H2H2[i] * x_H3_gg_H2H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H2H2))])
            pp_X_H2H2 = np.array([(b_H3_H2H2[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H2H2))])
            return mH1_H1H2, pp_X_H2H2
            
    else:
        raise Exception("No physics chosen")




def regionTestingFunc(BP, physics, userParametersDict, free, directory, filename, individualPlots):
    
    duds = []
    individual = []
    
    if free == "vev":
        
        for dictElement in userParametersDict:
            
            try:
                # Ensures dictElement is always a dictionary
                if isinstance(userParametersDict, dict) == True:
                    dictElement = userParametersDict
                
                dictElement["vs_lb"] = 1
                dictElement["vs_ub"] = 1000
                vev_vs, val_vs = dataPuller(BP, physics, dictElement, "vs")
                del dictElement["vs_lb"]
                del dictElement["vs_ub"]
                
                dictElement["vx_lb"] = 1
                dictElement["vx_ub"] = 1000
                vev_vx, val_vx = dataPuller(BP, physics, dictElement, "vx")
                del dictElement["vx_lb"]
                del dictElement["vx_ub"]
                
                if individualPlots == True:
                    individual.append( {"vev_vs": vev_vs, "val_vs": val_vs, "vev_vx": vev_vx, "val_vx": val_vx, "ms": dictElement["ms"], "mx": dictElement["mx"]} )
                    
                    # For plotting constant y = dictElement["yaxis"] in individual plots
                    if "yaxis" in dictElement:
                        (individual[-1])["yaxis"] = dictElement["yaxis"]
                    
                plt.plot(vev_vs, val_vs)#, label = "ms = {}, mx = {}".format(dictElement["ms"], dictElement["mx"]))
                plt.plot(vev_vx, val_vx, color = plt.gca().lines[-1].get_color(), label = "ms = {}, mx = {}".format(dictElement["ms"], dictElement["mx"]))
            
                # If userParametersDict is a dictionary (a single element), the loop should break after this
                if isinstance(userParametersDict, dict) == True:
                    break
            except subprocess.TimeoutExpired:
                duds.append( [dictElement["ms"], dictElement["mx"]] )

        plt.xlim(1, 1000)
        if physics == "XSH" or physics == "XHH" or physics == "XSS":
            ylim_lb, ylim_ub = 0, 1                 # will be used in individual plots
            plt.ylim(ylim_lb, ylim_ub)
        if physics == "ppXSH" or physics == "ppXHH" or physics == "ppXSS":
            ylim_lb, ylim_ub = plt.gca().get_ylim()
#            plt.ylim(0,50)
        # code taken from stackexchange: https://stackoverflow.com/a/43439132/17456342
        plt.title(filename)
        location = directory + "/" + filename
        plt.savefig(location)
#        plt.show()
        plt.close()

        massplots(BP, physics, userParametersDict, directory, filename)
#        plt.show()
        plt.close()
        
    elif free == "angle":

        for dictElement in userParametersDict:
            
            try:
                # Ensures dictElement is always a dictionary
                if isinstance(userParametersDict, dict) == True:
                    dictElement = userParametersDict
                
                dictElement["ths_lb"] = -np.pi/2
                dictElement["ths_ub"] = np.pi/2
                angle_hS, val_hS = dataPuller(BP, physics, dictElement, "thetahS")
                del dictElement["ths_lb"]
                del dictElement["ths_ub"]
                
                dictElement["thx_lb"] = -np.pi/2
                dictElement["thx_ub"] = np.pi/2
                angle_hX, val_hX = dataPuller(BP, physics, dictElement, "thetahX")
                del dictElement["thx_lb"]
                del dictElement["thx_ub"]
                
                dictElement["tsx_lb"] = -np.pi/2
                dictElement["tsx_ub"] = np.pi/2
                angle_SX, val_SX = dataPuller(BP, physics, dictElement, "thetaSX")
                del dictElement["tsx_lb"]
                del dictElement["tsx_ub"]
                
                if individualPlots == True:
                    individual.append( {"angle_hS": angle_hS, "val_hS": val_hS, "angle_hX": angle_hX, "val_hX": val_hX, "angle_SX": angle_SX, "val_SX": val_SX , "ms": dictElement["ms"], "mx": dictElement["mx"]} )
                    
                    # For plotting constant y = dictElement["yaxis"] in individual plots
                    if "yaxis" in dictElement:
                        (individual[-1])["yaxis"] = dictElement["yaxis"]
                
                plt.plot(angle_hS, val_hS)#, label = "ms = {}, mx = {}".format(dictElement["ms"], dictElement["mx"]))
                plt.plot(angle_hX, val_hX, color = plt.gca().lines[-1].get_color())#, label = "ms = {}, mx = {}".format(dictElement["ms"], dictElement["mx"]))
                plt.plot(angle_SX, val_SX, color = plt.gca().lines[-1].get_color(), label = "ms = {}, mx = {}".format(dictElement["ms"], dictElement["mx"]))
                plt.xlim(-np.pi/2, np.pi/2)
                
                # If userParametersDict is a dictionary (a single element), the loop should break after this
                if isinstance(userParametersDict, dict) == True:
                    break
                    
            except subprocess.TimeoutExpired:
                duds.append( [dictElement["ms"], dictElement["mx"]] )
        
        plt.xlim(-np.pi/2, np.pi/2)
        if physics == "XSH" or physics == "XHH" or physics == "XSS":
            ylim_lb, ylim_ub = 0, 1                 # will be used in individual plots
            plt.ylim(ylim_lb, ylim_ub)
        if physics == "ppXSH" or physics == "ppXHH" or physics == "ppXSS":
            ylim_lb, ylim_ub = plt.gca().get_ylim() # will be used in individual plots
#            plt.ylim(0,50)
        plt.title(filename)
        location = directory + "/" + filename
        plt.savefig(location)
#        plt.show()
        plt.close()

        massplots(BP, physics, userParametersDict, directory, filename)
#        plt.show()
        plt.close()
        
    else:
        raise Exception("No proper axes given for plotting")
        
    
    if individualPlots == True:
        
        if free == "vev":
        
            location = directory + "/" + "vevIndividual"
            toShell = ["mkdir", location]
            subprocess.run(toShell)
        
            for dictElement in individual:
                plt.plot(dictElement["vev_vs"], dictElement["val_vs"],label = "vs")
                plt.plot(dictElement["vev_vx"], dictElement["val_vx"],label = "vx", color = plt.gca().lines[-1].get_color())
                
                # Plots a constant dashed line at y = dictElement["yaxis"] (can be used for checking if scannerS is above observed limits)
                if "yaxis" in dictElement:
                    plt.axhline(y=dictElement["yaxis"], color='black', linestyle="dashed")
                
                plt.xlim(1, 1000)
                plt.ylim(ylim_lb, ylim_ub)
                plt.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0)
                plt.title(filename + ", " + "ms = {}, mx = {}".format(dictElement["ms"], dictElement["mx"]))
                
                # Plots a constant dashed line at y = dictElement["yaxis"] (can be used for checking if scannerS is above observed limits)
                # and removes it for the next individual plot
                if "yaxis" in dictElement:
                    yaxis = plt.axhline(y=dictElement["yaxis"], color='black', linestyle='dashed')
                    plt.savefig(location + "/" + filename + "_{}-{}".format(dictElement["ms"], dictElement["mx"]) + ".png", bbox_inches="tight")
                    #code from stackexchange (specifically the comment by user P2000): https://stackoverflow.com/a/42955955/17456342
                    yaxis.remove()
                else:
                    plt.savefig(location + "/" + filename + "_{}-{}".format(dictElement["ms"], dictElement["mx"]) + ".png", bbox_inches="tight")

                # code from stackexchange: https://stackoverflow.com/a/64043072/17456342
                for line in plt.gca().lines: # put this before you call the 'mean' plot function.
                    line.set_label(s='')
            
            plt.close()
        
        elif free == "angle":
        
            location = directory + "/" + "angleIndividual"
            toShell = ["mkdir", location]
            subprocess.run(toShell)
        
            for dictElement in individual:
                plt.plot(dictElement["angle_hS"], dictElement["val_hS"],label = "hs")
                plt.plot(dictElement["angle_hX"], dictElement["val_hX"],label = "hX", color = plt.gca().lines[-1].get_color())
                plt.plot(dictElement["angle_SX"], dictElement["val_SX"],label = "SX", color = plt.gca().lines[-1].get_color())
                
                plt.xlim(-np.pi/2, np.pi/2)
                plt.ylim(ylim_lb, ylim_ub)
                plt.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0)
                plt.title(filename + ", " + "ms = {}, mx = {}".format(dictElement["ms"], dictElement["mx"]))
                
                # Plots a constant dashed line at y = dictElement["yaxis"] (can be used for checking if scannerS is above observed limits)
                # and removes it for the next individual plot
                if "yaxis" in dictElement:
                    yaxis = plt.axhline(y=dictElement["yaxis"], color='black', linestyle='dashed')
                    plt.savefig(location + "/" + filename + "_{}-{}".format(dictElement["ms"], dictElement["mx"]) + ".png", bbox_inches="tight")
                    #code from stackexchange (specifically the comment by user P2000): https://stackoverflow.com/a/42955955/17456342
                    yaxis.remove()
                else:            
                    plt.savefig(location + "/" + filename + "_{}-{}".format(dictElement["ms"], dictElement["mx"]) + ".png", bbox_inches="tight")
                
                # code from stackexchange: https://stackoverflow.com/a/64043072/17456342
                for line in plt.gca().lines: # put this before you call the 'mean' plot function.
                    line.set_label(s='')
            
            plt.close()
            
        else:
            raise Exception("No physics chosen in individual plots")
    
    if len(duds) != 0:
    
        print("+----------------------------------------------------------+")
        print("The following masspoints were aborted for taking too long:")
        print("+----------------------------------------------------------+")
        print(duds)
        print("+----------------------------------------------------------+")
        print("saving to " + directory + "as" + filename + "_Aborted.txt")
        
        with open(directory + "/" + filename +"_Aborted.txt", "w") as f:
            f.write(str(duds))
            
        print("+----------------------------------------------------------+")
        
    elif len(duds) == 0:
        print("+----------------------------------------------------------+")
        print("There are no aborted masspoints")

    else:
        raise Exception("aborted mass points failed")









#### BP2 REGION 2

#pointlist = TRSM_rt.pointGen("BP2", 2, 5, "grid")

#dictPointlist = []

#for element in pointlist:
#    dictPointlist.append({ "ms": element[0], "mx": element[1] })

#TRSM_rt.regionTestingFunc("BP2", "XSH", dictPointlist, "vev", "plotting/XSH_region2_5x5", "BP2_XSHvev_region2", individualPlots = True)
#TRSM_rt.regionTestingFunc("BP2", "XSH", dictPointlist, "angle", "plotting/XSH_region2_5x5", "BP2_XSHangle_region2", individualPlots = True)



#### BP2 REGION 3

#pointlist = TRSM_rt.pointGen("BP2", 3, 5, "grid")

#dictPointlist = []

#for element in pointlist:
#    dictPointlist.append({ "ms": element[0], "mx": element[1] })

#TRSM_rt.regionTestingFunc("BP2", "XSS", dictPointlist, "vev", "plotting/XSS_region3_5x5", "BP2_XSSvev_region3", individualPlots = True)
#TRSM_rt.regionTestingFunc("BP2", "XSS", dictPointlist, "angle", "plotting/XSS_region3_5x5", "BP2_XSSangle_region3", individualPlots = True)


#TRSM_rt.regionTestingFunc("BP2", "XSH", [{"ms": 80, "mx": 350}, {"ms": 100, "mx": 300}], "angle", "temp", "check_angle", individualPlots = True)
#TRSM_rt.regionTestingFunc("BP2", "XSH", [{"ms": 80, "mx": 350}, {"ms": 100, "mx": 300}], "vev", "temp", "check_vev", individualPlots = True)



#### BP3 REGION 1

#pointlist = TRSM_rt.pointGen("BP3", 1, 5, "grid")

#dictPointlist = []

#for element in pointlist:
#    dictPointlist.append({ "ms": element[0], "mx": element[1] })

#TRSM_rt.regionTestingFunc("BP3", "XSH", dictPointlist, "vev",   "plotting/BP3_BR_XNP/BP3_XSH_region1_5x5", "BP3_XSHvev_region1",   individualPlots = True)
#TRSM_rt.regionTestingFunc("BP3", "XSH", dictPointlist, "angle", "plotting/BP3_BR_XNP/BP3_XSH_region1_5x5", "BP2_XSHangle_region1", individualPlots = True)



### BP3 REGION 2

pointlist = pointGen("BP3", 2, 8, "grid")

dictPointlist = []

for element in pointlist:
    dictPointlist.append({ "ms": element[0], "mx": element[1] })

regionTestingFunc("BP3", "XSH", dictPointlist, "vev",   "plotting/BP3_BR_XNP/BP3_XSH_region2_8x8", "BP3_XSHvev_region2",   individualPlots = True)
regionTestingFunc("BP3", "XSH", dictPointlist, "angle", "plotting/BP3_BR_XNP/BP3_XSH_region2_8x8", "BP2_XSHangle_region2", individualPlots = True)


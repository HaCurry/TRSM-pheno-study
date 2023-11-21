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
    """Returns the coordinates (listS)[index], (listX)[index] and the value at 
    the coordinates (br)[index] nearest to the given coordinates (pointS, pointX).
    
    Let epsilon be larger than the average distance between the points in the
    coordinate lists listS, listX.
    """

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
    """ Generates mass points for a benchmarkplane BP in a given region with a
    given size and generator.
    
    If generator is set to random, size is the numer of points generated.
    
    If generator is set to grid, size is the side length of the grid before the
    applied constrains from the region i.e all points outside regions will be 
    thrown away.
    """
    
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
    """Plots markers in a figure given a list of tuples of coordinates with the 
    value of the coordinates given by pointfinder.
    
    If visible is set to True, a red o-shaped marker is plotted in the figure.
    
    Decimals determines the number of decimals in pointfinder.
    
    fsize determines the fontsize for the value given by pointfinder.
    
    x, y, n is used by pointfinder to generate the nearest value given the marker
    points. 
    """


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
        
    # Note, only ppXSHSM is supported, the rest are under development
    elif (physics == "ppXSHSM") or (physics == "ppXSSSM") or (physics == "ppXHHSM"):
        
        SM1, SM2 = "bb", "gamgam"
        b_H1_bb     = [i for i in df["b_H1_" + SM1]]        #"b_H1_bb"
        b_H1_gamgam = [i for i in df["b_H1_" + SM2]]        #"b_H1_gamgam"
        b_H2_bb     = [i for i in df["b_H2_" + SM1]]        #"b_H2_bb"
        b_H2_gamgam = [i for i in df["b_H2_" + SM2]]        #"b_H2_gamgam"
        
        b_H1H2_bbgamgam = [b_H1_bb[i] * b_H2_gamgam[i] + b_H2_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
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
        
        b_H1_bb_H2_gamgam = [b_H1_bb[i] * b_H2_gamgam[i] for i in range(len(b_H1_bb))]
        pp_X_H1_bb_H2_gamgam = [b_H1_bb_H2_gamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
        
        b_H1_gamgam_H2_bb = [b_H1_gamgam[i] * b_H2_bb[i] for i in range(len(b_H1_gamgam))]
        pp_X_H1_gamgam_H2_bb = [b_H1_gamgam_H2_bb[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
        
            
        H1H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H1H2_bbgamgam, pp_X_H1_bb_H2_gamgam, pp_X_H1_gamgam_H2_bb])
        H1H1 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H1H1_bbgamgam])
        H2H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H2H2_bbgamgam])
        
        return H1H2, H1H1, H2H2
        
    else:
        raise Exception("No physics chosen in XNP_rt")




def massplots(BP, physics, userParametersDict, directory, filename, SM1, SM2):
    
    if BP == "BP2":
        H1H2, H1H1, H2H2 = XNP_rt(r"/home/iram/scannerS/ScannerS-master/build/BP2output/BP2_output_file.tsv", "mH1", "mH2", "mH3", physics)

    elif BP == "BP3":    
        H1H2, H1H1, H2H2 = XNP_rt(r"/home/iram/scannerS/ScannerS-master/build/BP3output/BP3_output_file.tsv", "mH1", "mH2", "mH3", physics)
    
    else:
        raise Exception("No BP chosen in massplots")

    # line of code suggested by ChatGPT
    x, y, z = '', '', ''  # Initialize the variables

    if physics == "XSH":
        
        if BP == "BP2":
            x, y, n = H1H2[0], H1H2[2], H1H2[3]
        elif BP == "BP3":
            x, y, n = H1H2[1], H1H2[2], H1H2[3]
        else:
            raise Exception("Error HERE!")
        
        title = filename + BP + ": $BR(X\\to SH)$"
        
        plt.title(title)
        x, y, z = np.asarray(x), np.asarray(y), np.asarray(n)

    elif (physics == "ppXSH") or (physics == "ppXSHSM"):

        if physics == "ppXSH":
        
            if BP == "BP2":
                x, y, n = H1H2[0], H1H2[2], H1H2[3]
            elif BP == "BP3":
                x, y, n = H1H2[1], H1H2[2], H1H2[3]
            else:
                raise Exception("Error HERE!")
            
            title = filename + BP + ": $\sigma(pp \\to X\\to SH)$"
            
            plt.title(title)
            x, y, z = np.asarray(x), np.asarray(y), np.asarray(n)
            
        else: # physics == "ppXSHSM":
            
            if BP == "BP2":
                x, y, n = H1H2[0], H1H2[2], H1H2[4]
            
            elif BP == "BP3":
                x, y, n = H1H2[1], H1H2[2], H1H2[4]
            
            SM1, SM2 = "bb", "gamgam"
            
            title = filename + BP + ": $\sigma(pp \\to X\\to SH" + SM1 + SM2 + ")$"
            
            plt.title(title)
            x, y, z = np.asarray(x), np.asarray(y), np.asarray(n)

    elif physics == "XHH":
        
        if BP == "BP2":
            x, y, n = H2H2[0], H2H2[2], H2H2[3]
            print(x[0],y[0],n[0])
        
        elif BP == "BP3":
            x, y, n = H1H1[1], H1H1[2], H1H1[3]
            print(x[0],y[0],n[0])
        else:
            raise Exception("Error HERE!")
        
        title = filename + BP +": $BR(pp \\to X\\to HH)$"

        plt.title(title)
        x, y, z = np.asarray(x), np.asarray(y), np.asarray(n)

    elif physics == "ppXHH":
        
        if BP == "BP2":
            x, y, n = H2H2[0], H2H2[2], H2H2[3]
        
        elif BP == "BP3":
            x, y, n = H1H1[1], H1H1[2], H1H1[3]
        else:
            raise Exception("Error HERE!")
            
        title = filename + BP + ": $\sigma(pp \\to X\\to HH)$"

        plt.title(title)
        x, y, z = np.asarray(x), np.asarray(y), np.asarray(n)

    elif physics == "XSS":
   
        if BP == "BP2":
            x, y, n = H1H1[0], H1H1[2], H1H1[3]

        elif BP == "BP3":
            x, y, n = H2H2[1], H2H2[2], H2H2[3]
        else:
            raise Exception("Error HERE!")
        
        title = filename + BP + ": $BR(X\\to SS)$"

        plt.title(title)
        x, y, z = np.asarray(x), np.asarray(y), np.asarray(n)

    elif physics == "ppXSS":

        if BP == "BP2":
            x, y, n =  H1H1[0], H1H1[2], H1H1[3]

        elif BP == "BP3":
            x, y, n = H2H2[1], H2H2[2], H2H2[3]
        else:
            raise Exception("Error HERE!")
        
        title = filename + BP + ": $\sigma(X\\to SS)$"

        plt.title(title)
        x, y, z = np.asarray(x), np.asarray(y), np.asarray(n)

    elif physics == "ppXNPSM":
        raise Exception("ppXNPSM is in work in progress not finished")
    
    else:
        raise Exception("No physics chosen for massplots")
        
    
#    plt.title(title)
#    x, y, z = np.asarray(x), np.asarray(y), np.asarray(n)
        
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

    else:
        raise Exception("Error HERE!")

    # code taken from stackexchange
    nInterp = 500
    xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    xi, yi = np.meshgrid(xi, yi)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    SMlabel = {"uu": "u\\bar{u}", "cc": "c\\bar{c}", "tt": "t\\bar{t}", "dd": "d\\bar{d}", "ss": "s\\bar{s}", "bb": "b\\bar{b}", "mumu": "\mu^{+}\mu^{-}", "tautau": "\\tau^{+}\\tau^{-}", "gg": "gg", "gamgam": "\gamma\gamma", "ZZ": "ZZ", "WW": "W^{+}W^{-}"}

    if SM1 != None and SM2 != None:
        colorbarlabel = {"XSH": "$BR(X \\to SH)$", "ppXSH": "$\sigma(pp \\to X \\to SH)$", "XHH": "$BR(X \\to HH)$", "ppXHH" : "$\sigma(pp \\to X \\to HH)$", "XSS": "$BR(X \\to SS)$", "ppXSS" : "$\sigma(pp \\to X \\to SS)$", "ppXSHSM": "$\sigma(pp \\to X \\to SH \\to " + SMlabel[SM1] + SMlabel[SM2] + " )$"}                                         

    else:
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
    else:
        raise Exception("Error HERE!")
    
    location = directory + "/" + filename 
    plt.savefig(location + " " + physics + "massplot")



def dataPuller(BP, physics, userParametersDict, axis, SM1, SM2):
# Returns arrays for parameter plots
    
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

    subprocess.run(toShell, timeout = 180)
    
    df = pandas.read_table(r"regionTesting.tsv")
    
    mH1_H1H2 = np.array([i for i in df[axis]])
    mH2_H1H2 = np.array([i for i in df["mH2"]])
    mH3_H1H2 = np.array([i for i in df["mH3"]])

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
    ggF_xs_SM_Higgs_SM1SM2 = 1
    
    if (physics == "ppXSH") or (physics == "ppXSHSM"):
        
        b_H3_H1H2 = b_H3_H1H2[idx]

        if physics == "ppXSH":
            pp_X_H1H2 = np.array([(b_H3_H1H2[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H1H2))])
    #        pp_X_H1H2 = np.array([b_H3_H1H2[i] for i in range(len(b_H3_H1H2))])
            return mH1_H1H2, pp_X_H1H2
        
        else: # physics == "ppXSHSM"
#            SM1, SM2 = "bb", "gamgam"
            b_H1_bb     = np.array([i for i in df["b_H1_" + SM1]])        #"b_H1_bb"
            b_H1_gamgam = np.array([i for i in df["b_H1_" + SM2]])        #"b_H1_gamgam"
            b_H2_bb     = np.array([i for i in df["b_H2_" + SM1]])        #"b_H2_bb"
            b_H2_gamgam = np.array([i for i in df["b_H2_" + SM2]])        #"b_H2_gamgam"
            
            b_H1_bb_H2_gamgam = np.array([b_H1_bb[i] * b_H2_gamgam[i] for i in range(len(b_H1_bb))])
            b_H1_bb_H2_gamgam = b_H1_bb_H2_gamgam[idx]
            
            pp_X_H1_bb_H2_gamgam = np.array([b_H1_bb_H2_gamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i] for i in range(len(b_H3_H1H2))])
            
            return mH1_H1H2, pp_X_H1_bb_H2_gamgam
    
    elif physics == "ppXHH":
        if BP == "BP2":
            b_H3_H2H2 = b_H3_H2H2[idx]
            pp_X_H2H2 = np.array([(b_H3_H2H2[i] * x_H3_gg_H1H2[i]) / ggF_xs_SM_Higgs for i in range(len(b_H3_H2H2))])
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




#def regionTestingFunc(BP, physics, userParametersDict, free, directory, filename, logyscale = False, individualPlots = True, sameFrame = True):
def regionTestingFunc(directory, filename, userParametersDict, **kwargs):
    
    if "free" in kwargs:
        free = kwargs["free"]
    
    else:
        raise Exception("No free chosen")

    if "BP" in kwargs:
        BP = kwargs["BP"]

    else:
        raise Exception("No BP chosen")
    
    if "physics" in kwargs:
        physics = kwargs["physics"]
        
        if (physics == "ppXSHSM") or (physics == "ppXSSSM") or (physics == "ppXHHSM"):

            if ("SM1" in kwargs) and ("SM2" in kwargs):
                SM1, SM2 = kwargs["SM1"], kwargs["SM2"]

            else:
                raise Exception("No SM finalstates chosen")

        else:
            SM1, SM2 = None, None

    if "logyscale" in kwargs:
        logyscale = kwargs["logyscale"]

    else:
        logyscale = False
        
    if "individualPlots" in kwargs:
        individualPlots = kwargs["individualPlots"]

    else:
        individualPlots = True
    
    if "sameFrame" in kwargs:
        sameFrame = kwargs["sameFrame"]

    else:
        sameFrame = True
        
    if "numberedTitle" in kwargs:
        numberedTitle = kwargs["numberedTitle"]
    else:
        numberedTitle = False
    
    
    duds = []
    individual = []
    
    bounds_vev = [{"vs_lb": 1, "vs_ub": 1000, "axis": "vs"}, {"vx_lb": 1, "vx_ub": 1000, "axis": "vx"}]
    bounds_angle = [{"ths_lb": -np.pi/2, "ths_ub": np.pi/2, "axis": "thetahS"}, {"thx_lb": -np.pi/2, "thx_ub": np.pi/2, "axis": "thetahX"}, {"tsx_lb": -np.pi/2, "tsx_ub": np.pi/2, "axis": "thetaSX"}]

    if free == "vev":
        bounds_list = bounds_vev
        label = [r'$v_{S} \ (solid), v_{X} \ (dotted)$']
        xlim_lb, xlim_ub = 1, 1000

    elif free == "angle":
        bounds_list = bounds_angle
        label = [r'$\theta_{hS} \ (solid), \theta_{hX} \ (dotted), \theta_{SX} \ (dashdot)$']
        xlim_lb, xlim_ub = -np.pi/2, np.pi/2

    else:
        raise Exception("No free chosen in regionTestingFunc!")

    color_list = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
    color_index = 0

    for i in range(len(userParametersDict)) :

        try:

            plotting_list = []

            for j in range(len(bounds_list)):
                # add free parameters to userParametersDict
                for key in (bounds_list[j]).keys():
                    
                    if key != "axis":
                        print(key)
                        (userParametersDict[i])[key] = (bounds_list[j])[key]
                    
                    elif key == "axis":
                        axis = (bounds_list[j])["axis"]
                    
                    else:
                        raise Exception("error with \"axis\" in adding keys")
                    
                # free parameter list and value list
                x, y = dataPuller(BP, physics, (userParametersDict[i]), axis, SM1, SM2)
                
                # save free parameter list and value list in plotting_list
                # for key in (bounds_list[j]).keys():
                plotting_list.append([x,y])
                
                # delete free parameters to userParametersDict
                for key in (bounds_list[j]).keys():

                    if key != "axis":
                        del (userParametersDict[i])[key]
                        
                    elif key == "axis":
                        continue
                        
                    else:
                        raise Exception("error with \"axis\" in deleting keys")

            linestyle_list = ['solid', 'dotted', 'dashdot']
            linestyle_index = 0

            for plot in plotting_list:

                # color value makes sure all curves have the same colour
#                try:
                plt.plot(plot[0], plot[1], 
                color = color_list[color_index % 10], 
#                label = "ms = {}, mx = {}".format((userParametersDict[i])["ms"], (userParametersDict[i])["mx"]) 
                linestyle = linestyle_list[linestyle_index])
                
                linestyle_index = linestyle_index + 1

                # if it is the first element, we plot as normal
#                except IndexError:
#                    plt.plot(plot[0], plot[1])
            
            
            # if individualPlots is True, make sure to save plotting_list
            if individualPlots == True:
                individual.append( {"plotting_list": plotting_list, "ms": (userParametersDict[i])["ms"], "mx": (userParametersDict[i])["mx"]} )
                
                # if user gives "yaxis" in userParametersDict then save to individual plots
                if "yaxis" in (userParametersDict[i]):
                    (individual[-1])["yaxis"] = (userParametersDict[i])["yaxis"]
                    
            color_index = color_index + 1

        except subprocess.TimeoutExpired:
            duds.append( [(userParametersDict[i])["ms"], (userParametersDict[i])["mx"]] )

    plt.xlim(xlim_lb, xlim_ub)

    plt.legend(label, loc = 'upper right')

    if logyscale == True:
        plt.yscale('log')

    if (physics == "XSH") or (physics == "XHH") or (physics == "XSS"):
        ylim_lb, ylim_ub = 0, 1    # will be used in individual plots
        plt.ylim(ylim_lb, ylim_ub)


    elif (physics == "ppXSH") or (physics == "ppXHH") or (physics == "ppXSS") or (physics == "ppXSHSM") or (physics == "ppXHHSM") or (physics == "ppXSSSM"):
        
        if individualPlots == True:
            ylim_lb, ylim_ub = plt.gca().get_ylim()    # will be used in individual plots

            for dictElementIndividual in individual:    

                # if plt ylimit upper bound is larger than yaxis set bound to to that otherwise use default settings
                # This is so that the y limits of the  individual plots encompass all the figures 
                if ("yaxis" in dictElementIndividual) and (dictElementIndividual["yaxis"] > ylim_ub):
                    ylim_ub = 2 * dictElementIndividual["yaxis"] # set the upperbound to double ylim_ub, otherwise the yaxis line is not visible in individual plots
                    print("==================== First step! ====================")

                else:
                    continue
            
            # if user wants same ylimts of the individual plots and the total plots
            if sameFrame == True:
                plt.ylim(ylim_lb, ylim_ub)


        else:
            ylim_lb, ylim_ub = plt.gca().get_ylim()

    else:
        raise Exception("No physics chosen")

    plt.title(filename)
    location = directory + "/" + filename
    plt.savefig(location)
    plt.close()

    massplots(BP, physics, userParametersDict, directory, filename, SM1, SM2)
    plt.close()

    if individualPlots == True:
        
        if free == "vev":
            location = directory + "/" + "vevIndividual"
            xlim_lb, xlim_ub = 1, 1000
            label = [r'$v_{S} \ (solid), v_{X} \ (dotted)$']

        elif free == "angle":        
            location = directory + "/" + "angleIndividual"
            xlim_lb, xlim_ub = -np.pi/2, np.pi/2
            label = [r'$\theta_{hS} \ (solid), \theta_{hX} \ (dotted), \theta_{SX} \ (dashdot)$']
        
        toShell = ["mkdir", location]
        subprocess.run(toShell)
        
        color_list = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
        color_index = 0
        
        if numberedTitle == True:
            numberedTitle_index = 0
        
        linestyle_list = ['solid', 'dotted', 'dashdot']
        
        for dictElement in individual:
            
            print(dictElement["ms"], dictElement["mx"])
            
            linestyle_index = 0

            for plot in dictElement["plotting_list"]:
                
                print(plot[0])
                print(plot[1])    
                    
                plt.plot(plot[0], plot[1], 
                color = color_list[color_index % 10],
                linestyle = linestyle_list[linestyle_index])
                
                linestyle_index = linestyle_index + 1

            color_index = color_index + 1

            plt.xlim(xlim_lb, xlim_ub)
            plt.ylim(ylim_lb, ylim_ub)

            if logyscale == True:
                plt.yscale('log')

            plt.legend(label, loc = 'upper right', handletextpad=-2.0, handlelength=0)
            plt.title(filename + ", " + "ms = {}, mx = {}".format(dictElement["ms"], dictElement["mx"]))

            # Plots a constant dashed line at y = dictElement["yaxis"] (can be used for checking if scannerS is above observed limits)
            # and removes it for the next individual plot
            if "yaxis" in dictElement:
                yaxis = plt.axhline(y = dictElement["yaxis"], color='black', linestyle='dashed')
                print("==================== Second step! ====================")
                print(ylim_ub)
                
                if numberedTitle == True:
                    plt.savefig(location + "/" + filename + str(numberedTitle_index) + ".png", bbox_inches="tight")
                    numberedTitle_index = numberedTitle_index + 1
                    
                else:                        
                    plt.savefig(location + "/" + filename + "_{}-{}".format(dictElement["ms"], dictElement["mx"]) + ".png", bbox_inches="tight")
                
#                plt.savefig(location + "/" + filename + "_{}-{}".format(dictElement["ms"], dictElement["mx"]) + ".png", bbox_inches="tight")
                #code from stackexchange (post and comment by user P2000): https://stackoverflow.com/a/42955955/17456342
                yaxis.remove()
                print("==================== Third step! ====================")

                
            # code from stackexchange: https://stackoverflow.com/a/64043072/17456342
            for line in plt.gca().lines: # put this before you call the 'mean' plot function.
                line.set_label(s='')

        plt.close()

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


## Problems/issues/obs to look out for and potentially fix:
#1.     ppXSHbbgamgam is not rescaled while ppXSH is

#1.1    The scale factor is fixed in ppXSH, this should potentially for the user 
#       to be able to customize  

#2.     Only ppXSHbbgamgam is supported but not the general ppXNPbbgamgam where NP is SS, HH.

#3.1    fix the following line in XNP_rt (we only want one of the modes): 
#       b_H1H2_bbgamgam = [b_H1_bb[i] * b_H2_gamgam[i] + b_H2_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]







#### BP2 REGION 2

#pointlist = pointGen("BP2", 2, 5, "grid")

#dictPointlist = []

#for element in pointlist:
#    dictPointlist.append({ "ms": element[0], "mx": element[1] })

###"temp4", "BP2_Atlas2023_obs_limit_angle", BP2_dictPointlistAtlas[0:2], BP = "BP2", physics = "ppXSHSM", SM1 = "bb", SM2 = "gamgam", free =  "angle", logyscale = True)

#regionTestingFunc("temp5", "BP2_XSHvev_region2", dictPointlist[0:2],  BP = "BP2", physics = "XSH", free = "vev", individualPlots = True,)
#regionTestingFunc("temp5", "BP2_XSHangle_region2", dictPointlist[0:2], BP = "BP2", physics = "XSH", free = "angle", individualPlots = True)



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



#### BP3 REGION 2

#pointlist = pointGen("BP3", 2, 8, "grid")

#dictPointlist = []

#for element in pointlist:
#    dictPointlist.append({ "ms": element[0], "mx": element[1] })

#regionTestingFunc("BP3", "XSH", dictPointlist, "vev",   "plotting/BP3_BR_XNP/BP3_XSH_region2_8x8", "BP3_XSHvev_region2",   individualPlots = True)
#regionTestingFunc("BP3", "XSH", dictPointlist, "angle", "plotting/BP3_BR_XNP/BP3_XSH_region2_8x8", "BP2_XSHangle_region2", individualPlots = True)

### YOU WERE JUST DOING THIS ONE
#### BP3 REGION 3

#pointlist = pointGen("BP3", 3, 8, "grid")

#dictPointlist = []

#for element in pointlist:
#    dictPointlist.append({ "ms": element[0], "mx": element[1] })
#                                                                            #BP3_XHH_region3_8x8
#print(dictPointlist)
##regionTestingFunc("BP3", "XHH", dictPointlist, "vev",   "plotting/BP3_BR_XNP/BP3_XHH_region3_8x8", "BP3_XHHvev_region3",   individualPlots = True)
#regionTestingFunc("BP3", "XHH", dictPointlist, "angle", "plotting/BP3_BR_XNP/BP3_XHH_region3_8x8", "BP3_XHHangle_region3", individualPlots = True)



## BP2 ATLAS LIMITS

## OBSERVED LIMITS DATA PULLER##
limits = pandas.read_json('Atlas2023Limits.json')

mx, ms, limit_obs, limit_exp = [], [], [], []

for element in limits:
    mx.append((limits[element])[0])
    ms.append((limits[element])[1])
#    limit_exp.append((limits[element])[2] * 10 **(-3))
#    limit_obs.append((limits[element])[3] * 10 **(-3))
    limit_exp.append((limits[element])[2] * 10 **(-3))
    limit_obs.append((limits[element])[3] * 10 **(-3))
    # limit_exp.append((limits[element])[2] )
    # limit_obs.append((limits[element])[3] )

mx = np.array(mx)
ms = np.array(ms)
limit_exp = np.array(limit_exp)
limit_obs = np.array(limit_obs)

def constrained_observed_lim(ms, mx, limit_obs, ms_lb = 1, ms_ub = 124, mx_lb = 126, mx_ub = 500, LessThanOrEqualTo = True):
    ms_BP2constrained = []
    mx_BP2constrained = []
    limit_obs_BP2constrained = []
    if LessThanOrEqualTo == True:
        for i in range(len(limit_obs)):
            # if (BP2_x_min < ms[i]) and  (ms[i] < BP2_x_max) and (BP2_y_min < mx[i]) and (mx[i] < BP2_y_max):
            # MAKE SURE TO PLOT THIS SO YOU HAVE YOUR DESIRED POINTS BECAUSE THE EQUALITY MIGHT INCLUDE SOME
            # UNDESIRED POINTS IF THE FLOAT VALUE IS VERY CLOSE TO HE BOUNDS. OTHERWISE SET LessThanOrEqualTo = False
            if (ms_lb <= ms[i]) and  (ms[i] <= ms_ub) and (mx_lb <= mx[i]) and (mx[i] <= mx_ub):
                ms_BP2constrained.append(ms[i])
                mx_BP2constrained.append(mx[i])
                limit_obs_BP2constrained.append(limit_obs[i])
            else:
                continue
        
        return ms_BP2constrained, mx_BP2constrained, limit_obs_BP2constrained
    
    else:
        for i in range(len(limit_obs)):
            # if (BP2_x_min < ms[i]) and  (ms[i] < BP2_x_max) and (BP2_y_min < mx[i]) and (mx[i] < BP2_y_max):
            # MAKE SURE TO PLOT THIS SO YOU HAVE YOUR DESIRED POINTS BECAUSE THE EQUALITY MIGHT INCLUDE SOME
            # UNDESIRED POINTS IF THE FLOAT VALUE IS VERY CLOSE TO HE BOUNDS. OTHERWISE SET LessThanOrEqualTo = False
            if (ms_lb < ms[i]) and  (ms[i] < ms_ub) and (mx_lb < mx[i]) and (mx[i] < mx_ub):
                ms_BP2constrained.append(ms[i])
                mx_BP2constrained.append(mx[i])
                limit_obs_BP2constrained.append(limit_obs[i])
            else:
                continue
        
        return ms_BP2constrained, mx_BP2constrained, limit_obs_BP2constrained
    
ms_BP2constrained, mx_BP2constrained, limit_obs_BP2constrained = constrained_observed_lim(ms, mx, limit_obs, LessThanOrEqualTo = True)

BP2_dictPointlistAtlas = []
for i in range(len(limit_obs_BP2constrained)):
    BP2_dictPointlistAtlas.append({ "ms": ms_BP2constrained[i], "mx": mx_BP2constrained[i], "yaxis": limit_obs_BP2constrained[i] })
    
#regionTestingFunc("BP2", "ppXSHSM", BP2_dictPointlistAtlas[2], "angle", "plottingLimits/Atlas2023/BP2_Atlas", "BP2_Atlas2023_obs_limit", logyscale = True, individualPlots = True)

#(directory, filename, userParametersDict, **kwargs)

#regionTestingFunc("plottingLimits/Atlas2023/BP2_Atlas", "BP2_Atlas2023_obs_limit_vev_points_1_to_25", BP2_dictPointlistAtlas[0:25], BP = "BP2", physics = "ppXSHSM", SM1 = "bb", SM2 = "gamgam", free =  "vev", logyscale = True, numberedTitle = True)
regionTestingFunc("plottingLimits/Atlas2023/BP2_Atlas", "BP2_Atlas2023_obs_limit_vev_points_25_to_rest", BP2_dictPointlistAtlas[25:], BP = "BP2", physics = "ppXSHSM", SM1 = "bb", SM2 = "gamgam", free =  "vev", logyscale = True, numberedTitle = True)
#regionTestingFunc("plottingLimits/Atlas2023/BP2_Atlas", "BP2_Atlas2023_obs_limit_angle_points_1_to_25", BP2_dictPointlistAtlas[0:25], BP = "BP2", physics = "ppXSHSM", SM1 = "bb", SM2 = "gamgam", free =  "angle", logyscale = True, numberedTitle = True)








#listPacker(BPdirectory, axes1, axes2, axes3, SM1, SM2, xs_NP = True, xs_SM = True, sort = False):
#    
#    df = pandas.read_table(BPdirectory, index_col = 0)
#    
#    mH1_H1H2 = [i for i in df[axes1]]
#    mH2_H1H2 = [i for i in df[axes2]]
#    mH3_H1H2 = [i for i in df[axes3]]
#    
#    b_H3_H1H2 = [i for i in df["b_H3_H1H2"]]
#    b_H3_H1H1 = [i for i in df["b_H3_H1H1"]]
#    b_H3_H2H2 = [i for i in df["b_H3_H2H2"]]
#    
#    masses, br = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2]), np.array([b_H3_H1H2, b_H3_H1H1, b_H3_H2H2])
#    
#    if (xs_NP == False) and (xs_SM == False): 
#        return masses, br
#        
#    elif (xs_NP == True) and (xs_SM == False): 
#        Xsection_NP = np.array([i for i in df["x_H3_gg"]])
#        return masses, br, Xsection_NP
#    
#    elif (xs_NP == True) and (xs_SM == True):
#        SM1, SM2
#        b_H1_bb     = [i for i in df["b_H1_" + SM1]]        #"b_H1_bb"
#        b_H1_gamgam = [i for i in df["b_H1_" + SM2]]        #"b_H1_gamgam"
#        b_H2_bb     = [i for i in df["b_H2_" + SM1]]        #"b_H2_bb"
#        b_H2_gamgam = [i for i in df["b_H2_" + SM2]]        #"b_H2_gamgam" 
#        
#        b_H1_bb_H2_gamgam = np.array([b_H1_bb[i] * b_H2_gamgam[i] for i in range(len(b_H1_bb))])
#        b_H1_gamgam_H2_bb = np.array([b_H1_gamgam[i] * b_H2_bb[i] for i in range(len(b_H1_gamgam))])
#        b_H1H2_bbgamgam = np.array([b_H1_bb_H2_gamgam[i] + b_H1_gamgam_H2_bb[i] for i in range(len(b_H1_bb_H2_gamgam))])
#        
#        Xsection_SM = np.array([b_H1_bb_H2_gamgam, b_H1_gamgam_H2_bb, b_H1H2_bbgamgam])
#        
#        return masses, br, Xsection_NP, Xsection_SM






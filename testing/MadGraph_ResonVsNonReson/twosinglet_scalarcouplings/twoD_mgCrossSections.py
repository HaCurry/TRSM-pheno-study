import pandas
import subprocess
import re

# packages for generateCard
import math, cmath
import string, os, sys, fileinput, pprint, math
import numpy as np
import operator
from scipy.interpolate import interp1d
import collections
#from prettytable import PrettyTable
from math import log10, floor
import matplotlib
matplotlib.use('PDF')
import matplotlib.gridspec as gridspec
from matplotlib.ticker import Locator
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import rc
from matplotlib import container
#from matplotlib.mlab import griddata
import matplotlib.font_manager as fm
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as mpatches

def generateCard(pathParam_card, mH1_input, mH2_input, mH3_input, thetahS_input, thetahX_input, thetaSX_input, vs_input, vx_input):

    '''
    Creates run_card at location pathParam_card for madgraph with values of the
    TRSM parameters according to user given input. This function is based on
    code that can found in the twosinglet repo
    https://gitlab.com/apapaefs/twosinglet
    in the directory
    /twosinglet_scalarcouplings/twosinglet_generatecard.py

    returns None
    '''
    
    # round number to chosen number of significant digits
    def round_sig(x, sig=2):
        if x == 0.:
            return 0.
        if math.isnan(x) is True:
            print('Warning, NaN!')
            return 0.
        return round(x, sig-int(floor(log10(abs(x))))-1)

    # choose the next colour -- for plotting
    ccount = 0
    def next_color():
        global ccount
        colors = ['green', 'orange', 'red', 'blue', 'black', 'cyan', 'magenta', 'brown', 'violet'] # 9 colours
        color_chosen = colors[ccount]
        if ccount < 8:
            ccount = ccount + 1
        else:
            ccount = 0    
        return color_chosen

    # do not increment colour in this case:
    def same_color():
        global ccount
        colors = ['green', 'orange', 'red', 'blue', 'black', 'cyan', 'magenta', 'brown', 'violet'] # 9 colours
        color_chosen = colors[ccount-1]
        return color_chosen

    def reset_color():
        global ccount
        ccount = 0

    # scatter plot with changing markers
    def mscatter(x,y,ax=None, m=None, **kw):
        import matplotlib.markers as mmarkers
        if not ax: ax=plt.gca()
        sc = ax.scatter(x,y,**kw)
        if (m is not None) and (len(m)==len(x)):
            paths = []
            for marker in m:
                if isinstance(marker, mmarkers.MarkerStyle):
                    marker_obj = marker
                else:
                    marker_obj = mmarkers.MarkerStyle(marker)
                path = marker_obj.get_path().transformed(
                            marker_obj.get_transform())
                paths.append(path)
            sc.set_paths(paths)
        return sc


    # function to get template
    def getTemplate(basename):
        with open('%s.template' % basename, 'r') as f:
            templateText = f.read()
        return string.Template( templateText )

    # write a filename
    def writeFile(filename, text):
        with open(filename,'w') as f:
            f.write(text)

    # round number to sig significant figures
    def round_sig(x, sig=2):
        if x == 0.:
            return 0.
        if math.isnan(x) is True:
            print('Warning, NaN!')
            return 0.
        return round(x, sig-int(math.floor(math.log10(abs(x))))-1)
        
    # the R mixing matrix given the cosines of the angles
    def Rmatrix(a12, a13, a23):
        # define output matrix
        R = [[0. for x in range(3)] for y in range(3)]
        #calculate the cos functions
        c1 = math.cos(a12)
        c2 = math.cos(a13)
        c3 = math.cos(a23)
        # get the sin functions
        s1 = math.sin(a12)
        s2 = math.sin(a13)
        s3 = math.sin(a23)

        # calculate the elements
        R[0][0] = c1 * c2
        R[0][1] = - s1 * c2
        R[0][2] = - s2
        R[1][0] = s1 * c3 - c1 * s2 * s3
        R[1][1] = c1 * c3 + s1 * s2 * s3
        R[1][2] = - c2 * s3
        R[2][0] = c1 * s2 * c3 + s1 * s3
        R[2][1] = c1 * s3 - s1 * s2 * c3
        R[2][2] = c2 * c3
        return R
    
    def lambda_ijkm(i, j, k, m, M1, M2, M3, v, vs, vx, *R):
        R11, R12, R13, R21, R22, R23, R31, R32, R33 = R[0][0], R[0][1], R[0][2], R[1][0], R[1][1], R[1][2], R[2][0], R[2][1], R[2][2]

        # sort the i, j, k, m
        ind = (i, j, k, m)
        ind_sort = sorted(ind)
        # get the coupling filename
        couplfile = str(ind_sort[0]) + str(ind_sort[1]) + str(ind_sort[2]) + str(ind_sort[3]) + '.dat'    
        # read in the file and evaluate
        if os.path.exists(couplfile) is True:
            couplstream = open(couplfile, 'r')
        else:
            print(('Error:', couplfile, 'does not exist!'))
        for line in couplstream:
            coupl = eval(line)
        return coupl

    def lambda_ijk(i, j, k, M1, M2, M3, v, vs, vx, *R):
        R11, R12, R13, R21, R22, R23, R31, R32, R33 = R[0][0], R[0][1], R[0][2], R[1][0], R[1][1], R[1][2], R[2][0], R[2][1], R[2][2]

        # sort the i, j, k, m
        ind = (i, j, k)
        ind_sort = sorted(ind)
        # get the coupling filename
        couplfile = 'Cubic_' + str(ind_sort[0]) + str(ind_sort[1]) + str(ind_sort[2]) + '.dat'    
        # read in the file and evaluate
        if os.path.exists(couplfile) is True:
            couplstream = open(couplfile, 'r')
        else:
            print(('Error:', couplfile, 'does not exist!'))
        for line in couplstream:
            coupl = eval(line)
        return coupl

    # calculate the width h2 -> h1 h1, given the mass, the coupling l112 (in GeV) and the sin(mixing angle)
    def Gam_h2_to_h1h1(m1, m2, l112):
      if m2 < 2*m1:
        return 0.
      width_h2h1h1 = l112**2 * math.sqrt( 1 - 4 * m1**2 / m2**2 ) / 8 / math.pi / m2
      return width_h2h1h1

    # calculate the width h3 -> h2 h1, given the mass, the coupling l123 (in GeV) and the sin(mixing angle)
    def Gam_h3_to_h2h1(m1, m2, m3, l123):
      if m3 < m1+m2:
        return 0.
      P = (1./2./m3) * math.sqrt( (m3**2 - (m1+m2)**2) * (m3**2 - (m1-m2)**2) )
      width_h3h2h1 = l123**2 * P / 8 / math.pi / m3**2
      return width_h3h2h1

    # function to read in the branching ratios into a dictionary in the format:
    # mass [GeV] | H -> bbbar | H -> tautau | H -> mumu | H -> cc | H -> ss | H -> tt | H -> gg | H -> gammagamma | H -> Zgamma | H -> WW | H -> ZZ | total width [GeV]
    # see https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR2014#SM_Higgs_Branching_Ratios_and_Pa
    def read_higgsBR(brfile):
        higgsbrs = {}
        brstream = open(brfile, 'r')
        brarray = []
        for line in brstream:
            brarray = [ float(line.split()[1]), float(line.split()[2]), float(line.split()[3]), float(line.split()[4]), float(line.split()[5]), float(line.split()[6]), float(line.split()[7]), float(line.split()[8]), float(line.split()[9]), float(line.split()[10]), float(line.split()[11]), float(line.split()[12])]
            higgsbrs[float(line.split()[0])] = brarray
        # sort by increasing value of HYmass
        sorted_x = sorted(list(higgsbrs.items()), key=operator.itemgetter(0))
        sorted_higgsbrs = collections.OrderedDict(sorted_x)
        return sorted_higgsbrs

    # create interpolators for the various BRs and total width and return a dictionary
    def interpolate_HiggsBR(brdict):
      # the kind of interpolation
      interpkind = 'cubic'

      # define an array of interpolators
      interp_higgsbrs = []

      # find out how many BRs+width we have:
      values_view = list(brdict.values())
      value_iterator = iter(values_view)
      first_value = next(value_iterator)
      NBRs = len(first_value)
  
      # push back all the values of the masses, brs and width into arrays
      mass_array = []
      br_array =[[] for yy in range(NBRs)]

      # get the mass and the corresponding BR arrays
      for key in list(brdict.keys()):
          mass_array.append(key)
          for ii in range(NBRs):
            br_array[ii].append(brdict[key][ii])

      # now create the interpolators and put them in the array:
      for ii in range(NBRs):
            interpolator = interp1d(mass_array, br_array[ii], kind=interpkind, bounds_error=False)
            interp_higgsbrs.append(interpolator)

      return interp_higgsbrs


    # function to read in the XS into a dictionary in the format:
    # mS or mH (GeV) | Cross Section (pb) |	+Theory | -Theory |	TH Gaussian | -+(PDF+alphaS)
    # see https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHXSWG#BSM_Higgs
    def read_higgsXS_N3LO(xsfile):
        higgsxss = {}
        xsstream = open(xsfile, 'r')
        xsarray = []
        for line in xsstream:
            xsarray = [ float(line.split()[1]), float(line.split()[2]), float(line.split()[3]), float(line.split()[4]), float(line.split()[5])]
            higgsxss[float(line.split()[0])] = xsarray
        # sort by increasing value of HYmass
        sorted_x = sorted(list(higgsxss.items()), key=operator.itemgetter(0))
        sorted_higgsxss = collections.OrderedDict(sorted_x)
        return sorted_higgsxss

    # create interpolators for the XS and return a dictionary
    def interpolate_HiggsXS(xsdict):
      # the kind of interpolation
      interpkind = 'next'

      # define an array of interpolators
      interp_higgsxss = []

      # find out how many BRs+width we have:
      values_view = list(xsdict.values())
      value_iterator = iter(values_view)
      first_value = next(value_iterator)
      NXSs = len(first_value)
  
      # push back all the values of the masses, brs and width into arrays
      mass_array = []
      xs_array =[]

      # get the mass and the corresponding BR arrays
      for key in list(xsdict.keys()):
          mass_array.append(key)
          xs_array.append(xsdict[key][0])

      # now create the interpolators and put them in the array:
      interp_higgsxss = interp1d(mass_array, xs_array, kind=interpkind, bounds_error=False)

      return interp_higgsxss


    # function that takes in the sintheta, lambda112, mh1 and an mh2 array and returns the array of BRs for the Heavy Higgs
    def calc_h2_BRs(interpolators_SM, mh1, mh2, R21, l112):
        heavyBRs = []
        # get the corresponding SM width from the interpolator (this should be the last element):
        if mh2 < 1000.: # 
                Gamma_SM = interpolators_SM[-1](mh2)
        else:
                Gamma_SM = interpolators_SM[-1](1000.)
       # get the rescaling factor of the SM BRs:
        rescale_fac = RES_BR_h2_to_xx(R21, Gamma_SM, mh1, mh2, l112)
        # loop over the SM BRs and rescale with the factor:
        for hh in range(len(interpolators_SM)-1):
            heavyBRs.append(interpolators_SM[hh](mh2) * rescale_fac)
        # add the h1h1 decay:
        BR_hh = BR_h2_to_h1h1(R21, mh1, mh2, l112, Gamma_SM)
        heavyBRs.append(BR_hh)
        width = width_h2(R21, mh1, mh2, l112, Gamma_SM)
        heavyBRs.append(width)
        # transpose the array to get it into the right form for plotting
        heavyBRs = np.transpose(heavyBRs)
        return heavyBRs

    # function that takes in the sintheta, lambda112, mh1 and an mh2 array and returns the array of BRs for the Heavy Higgs
    def calc_h3_BRs(interpolators_SM, mh1, mh2, mh3, R31, l113, l123, l223):
        heavyBRs = []
        # get the corresponding SM width from the interpolator (this should be the last element):
        if mh3 < 1000.: # 
            Gamma_SM = interpolators_SM[-1](mh3)
        else:
            Gamma_SM = interpolators_SM[-1](1000.)
        #print(('BSM width at m3=', mh3, Gamma_SM))
        # get the rescaling factor of the SM BRs:
        rescale_fac = RES_BR_h3_to_xx(R31, Gamma_SM, mh1, mh2, mh3, l113, l123, l223)
        # loop over the SM BRs and rescale with the factor:
        for hh in range(len(interpolators_SM)-1):
            heavyBRs.append(interpolators_SM[hh](mh3) * rescale_fac)
        # add the h1h1 decay:
        BR_h1h1 = BR_h3_to_h1h1(R31, mh1, mh2, mh3, l113, l123, l223, Gamma_SM)
        heavyBRs.append(BR_h1h1)
        BR_h2h1 = BR_h3_to_h2h1(R31, mh1, mh2, mh3, l113, l123, l223, Gamma_SM)
        heavyBRs.append(BR_h2h1)
        BR_h2h2 = BR_h3_to_h2h2(R31, mh1, mh2, mh3, l113, l123, l223, Gamma_SM)
        heavyBRs.append(BR_h2h2)
        width = width_h3(R31, mh1, mh2, mh3, l113, l123, l223, Gamma_SM)
        heavyBRs.append(width)
        # transpose the array to get it into the right form for plotting
        heavyBRs = np.transpose(heavyBRs)
        return heavyBRs

    # function that takes in the sintheta, lambda112, mh1 and an mh2 array and returns the array of BRs for the Heavy Higgs
    def calc_h1_BRs(interpolators_SM, mh1, R11):
        BRs = []
        # get the corresponding SM width from the interpolator (this should be the last element):
        if mh1 < 1000.: # 
            Gamma_SM = interpolators_SM[-1](mh1)
        else:
            Gamma_SM = interpolators_SM[-1](1000.)
        # loop over the SM BRs and rescale with the factor:
        for hh in range(len(interpolators_SM)-1):
            BRs.append(interpolators_SM[hh](mh1)*R11**2)
        width = R11**2 * Gamma_SM
        BRs.append(width)
        # transpose the array to get it into the right form for plotting
        BRs = np.transpose(BRs)
        return BRs


    # branching ratio RESCALING for h2 -> xx given Gamma_SM, sintheta, m1, m2, l112:
    def RES_BR_h2_to_xx(R21, Gam_SM, m1, m2, l112):
        Gam_h2h1h1 = Gam_h2_to_h1h1(m1, m2, l112)
        RES_h2xx = R21**2 * Gam_SM/ ( Gam_SM * R21**2  + Gam_h2h1h1)
        return RES_h2xx

    # branching ratio RESCALING for h3 -> xx given Gamma_SM, sintheta, m1, m2, l112:
    def RES_BR_h3_to_xx(R31, Gam_SM, m1, m2, m3, l113, l123, l223):
        Gam_h2h1h1 = Gam_h2_to_h1h1(m1, m3, l113)
        Gam_h3h2h1 = Gam_h3_to_h2h1(m1, m2, m3, l123)
        Gam_h3h2h2 = Gam_h2_to_h1h1(m2, m3, l223)

        RES_h3xx = R31**2 * Gam_SM/ ( Gam_SM * R31**2  + Gam_h2h1h1 + Gam_h3h2h1 + Gam_h3h2h2)
        return RES_h3xx

    # the BR h2 -> h1 h1, given the m2, sintheta, l112, Gam_SM (total SM BR)
    def BR_h2_to_h1h1(R21, m1, m2, l112, Gam_SM):
        BRh2h1h1 = Gam_h2_to_h1h1(m1, m2, l112) /  ( Gam_SM * R21**2  + Gam_h2_to_h1h1(m1, m2, l112))
        return BRh2h1h1

    # the BR h3 -> h1 h1, given the m2, sintheta, l112, Gam_SM (total SM BR)
    def BR_h3_to_h1h1(R31, m1, m2, m3, l113, l123, l223, Gam_SM):
        BRh2h1h1 = Gam_h2_to_h1h1(m1, m3, l113) / ( Gam_SM * R31**2  + Gam_h2_to_h1h1(m1, m3, l113) + Gam_h3_to_h2h1(m1, m2, m3, l123) + Gam_h2_to_h1h1(m2, m3, l223))
        return BRh2h1h1

    # the BR h2 -> h1 h1, given the m2, sintheta, l112, Gam_SM (total SM BR)
    def BR_h3_to_h2h1(R31, m1, m2, m3, l113, l123, l223, Gam_SM):
        BRh2h1h1 = Gam_h3_to_h2h1(m1, m2, m3, l123) /  ( Gam_SM * R31**2  + Gam_h2_to_h1h1(m1, m3, l113) + Gam_h3_to_h2h1(m1, m2, m3, l123) + Gam_h2_to_h1h1(m2, m3, l223))
        return BRh2h1h1

    # the BR h2 -> h1 h1, given the m2, sintheta, l112, Gam_SM (total SM BR)
    def BR_h3_to_h2h2(R31, m1, m2, m3, l113, l123, l223, Gam_SM):
        BRh2h1h1 = Gam_h2_to_h1h1(m2, m3, l223) /  ( Gam_SM * R31**2  + Gam_h2_to_h1h1(m1, m3, l113) + Gam_h3_to_h2h1(m1, m2, m3, l123) + Gam_h2_to_h1h1(m2, m3, l223))
        return BRh2h1h1

    def width_h2(R21, m1, m2, l112, Gam_SM):
        total_width = Gam_SM * R21**2  + Gam_h2_to_h1h1(m1, m2, l112)
        return total_width

    def width_h3(R31, m1, m2, m3, l113, l123, l223, Gam_SM):
        total_width = Gam_SM * R31**2  + Gam_h2_to_h1h1(m1, m3, l113) + Gam_h3_to_h2h1(m1, m2, m3, l123) + Gam_h2_to_h1h1(m2, m3, l223)
        return total_width

    # print the heavy Higgs info:
    #def print_Higgs_info(HeavyHiggsBRs, BR_text_array_heavy, textinfo):
    #    print textinfo
    #    tbl = PrettyTable(["process", "BR"])
    #    for idx in range(len(HeavyHiggsBRs)):
    #      tbl.add_row([BR_text_array_heavy[idx].replace('$', ''), round_sig(HeavyHiggsBRs[idx],6)])
    #    print tbl
    #    BRsum_heavy = np.sum(HeavyHiggsBRs[:-1])
    #    print 'consistency check: sum(BRs)=', round_sig(BRsum_heavy,5)
    #    print '\n'


    #########################################
    # SOME ANALYSIS BEGINS HERE             #
    # DEFINING SOME INTERPOLATORS/VARIABLES #
    #########################################
    
    BR_text_array_h1 = [ '$b\\bar{b}$', '$\\tau \\tau$', '$\\mu \\mu$', '$c\\bar{c}$', '$s\\bar{s}$', '$t\\bar{t}$', '$gg$', '$\\gamma\\gamma$', '$Z \\gamma$', '$WW$', '$ZZ$', '$\\Gamma$' ]
    BR_text_array_h2 = [ '$b\\bar{b}$', '$\\tau \\tau$', '$\\mu \\mu$', '$c\\bar{c}$', '$s\\bar{s}$', '$t\\bar{t}$', '$gg$', '$\\gamma\\gamma$', '$Z \\gamma$', '$WW$', '$ZZ$', '$h_1 h1$', '$\\Gamma$' ]
    BR_text_array_h3 = [ '$b\\bar{b}$', '$\\tau \\tau$', '$\\mu \\mu$', '$c\\bar{c}$', '$s\\bar{s}$', '$t\\bar{t}$', '$gg$', '$\\gamma\\gamma$', '$Z \\gamma$', '$WW$', '$ZZ$', '$h_1 h1$', '$h_1 h_2$', '$h_2 h_2$', '$\\Gamma$' ]

    # the file containing the branching ratios for the SM Higgs boson:
    BR_file = "higgsBR_YR4.txt"
    # read the file:
    #print(('reading in', BR_file))
    HiggsBRs = read_higgsBR(BR_file)
    # test: print the dictionary
    # print_HiggsBR(HiggsBRs)
    # first get the interpolated BRs and SM width 
    BR_interpolators_SM = interpolate_HiggsBR(HiggsBRs)  # this returns the actual interpolators

    # the 13 TeV ggF cross sections at N^3LO
    XS13_file = "higgsXS_YR4_13TeV_N3LO.txt"
    #print(('reading in', XS13_file))
    HiggsXS_13_N3LO = read_higgsXS_N3LO(XS13_file)
    # get the interpolated XS
    XS_interpolator_SM_13TeV_N3LO = interpolate_HiggsXS(HiggsXS_13_N3LO)

    # write out madgraph parameter card:
    # get template:                
    param_card_template = getTemplate("param_card.dat")

    def get_point_info(v, vs, vx, M1, M2, M3, a12, a13, a23, PRINT):
    
        #calculate the cos
        c1 = math.cos(a12)
        c2 = math.cos(a13)
        c3 = math.cos(a23)

        #calculate the sin
        s1 = math.sin(a12)
        s2 = math.sin(a13)
        s3 = math.sin(a23)

        # first get the R-matrix 
        R = Rmatrix(a12, a13, a23)
        if PRINT:
            # print all parameters:
            print(('v, vs, vx, M1, M2, M3, a12, a13, a23=', v, vs, vx, M1, M2, M3, a12, a13, a23))
            print('\n')
            print(('R11=', R[0][0]))
            print(('R12=', R[0][1]))
            print(('R13=', R[0][2])) 
            print(('R21=', R[1][0])) 
            print(('R22=', R[1][1]))
            print(('R23=', R[1][2]))
            print(('R31=', R[2][0]))
            print(('R32=', R[2][1])) 
            print(('R33=', R[2][2]))
            print('\n')

        # define a dictionary with all the lambdas:
        lambda_dict = {}
        paramsubs = {
             'A12': a12,
             'A13': a13,
             'A23': a23,
             'S1' : s1,
             'S2' : s2,
             'S3' : s3,
             'C1' : c1,
             'C2' : c2,
             'C3' : c3,
             'M1' : M1,
             'M2' : M2,
             'M3' : M3,
             'V'  : v,
             'VS' : vs,
             'VX' : vx,
             'R11' : R[0][0],
             'R21' : R[1][0],
             'R31' : R[2][0]
    #        'R21' : R[1][0],
    #        'R31' : R[2][0]
             }
        # check all couplings:
        # triple:
        ijk = (1, 2, 3)
        if PRINT:
            print('triple couplings:')
            print('i j k\t\t\t lambda(i,j,k)')
        for i in ijk:
            for j in (jc for jc in ijk if jc <= i):
                for k in (kc for kc in ijk if kc <= j):
                    lambda_dict[tuple(sorted((i,j,k)))] = lambda_ijk(i, j, k, M1, M2, M3, v, vs, vx, *R)
                    lambda_text = 'K' + str(sorted((i,j,k))[0]) + str(sorted((i,j,k))[1]) + str(sorted((i,j,k))[2])
                    paramsubs[lambda_text] = lambda_dict[tuple(sorted((i,j,k)))]
                    if PRINT: print((sorted((i,j,k)), '\t\t', paramsubs[lambda_text]))

        if PRINT:
            print('\nquartic couplings:')
            print('i j k m\t\t\t lambda(i,j,k, m)')
        for i in ijk:
            for j in (jc for jc in ijk if jc <= i):
                for k in (kc for kc in ijk if kc <= j):
                    for m in (mc for mc in ijk if mc <= j):
                        lambda_dict[tuple(sorted((i,j,k,m)))] = lambda_ijkm(i, j, k, m, M1, M2, M3, v, vs, vx, *R)
                        lambda_text = 'K' + str(sorted((i,j,k,m))[0]) + str(sorted((i,j,k,m))[1]) + str(sorted((i,j,k,m))[2]) + str(sorted((i,j,k,m))[3])
                        paramsubs[lambda_text] = lambda_dict[tuple(sorted((i,j,k,m)))]
                        if PRINT: print((sorted((i,j,k,m)), '\t\t', paramsubs[lambda_text]))

        # calculate "by hand" the cross section for h2 -> h1 h1 and h3 -> h1 h1:
        # first get the widths to the light Higgs:
        width_h2h1h1= Gam_h2_to_h1h1(M1, M2, lambda_dict[tuple((1,1,2))])
        width_h3h1h1= Gam_h2_to_h1h1(M1, M3, lambda_dict[tuple((1,1,3))])
        width_h3h2h1= Gam_h3_to_h2h1(M1, M2, M3, lambda_dict[tuple((1,2,3))])
        width_h3h2h2= Gam_h2_to_h1h1(M2, M3, lambda_dict[tuple((2,2,3))])
        if PRINT:
            print('\nWidths:')
            print(('Gamma(h2 > h1 h1)=', width_h2h1h1, 'GeV'))
            print(('Gamma(h3 > h1 h1)=', width_h3h1h1, 'GeV'))
            print(('Gamma(h3 > h2 h1)=', width_h3h2h1, 'GeV'))
            print(('Gamma(h3 > h2 h2)=', width_h3h2h2, 'GeV'))


        # get the BRs for scalars:
        h1_BRs = calc_h1_BRs(BR_interpolators_SM, M1, R[0][0])
        h2_BRs = calc_h2_BRs(BR_interpolators_SM, M1, M2, R[1][0], lambda_dict[tuple((1,1,2))])
        h3_BRs = calc_h3_BRs(BR_interpolators_SM, M1, M2, M3, R[2][0], lambda_dict[tuple((1,1,3))], lambda_dict[tuple((1,2,3))], lambda_dict[tuple((2,2,3))])
        if PRINT:
            print('\n')
            # print them
            #print_Higgs_info(h1_BRs, BR_text_array_h1, 'h1 BRs & width')
            print('\n')
            #print_Higgs_info(h2_BRs, BR_text_array_h2, 'h2 BRs & width')
            print('\n')
            #print_Higgs_info(h3_BRs, BR_text_array_h3, 'h3 BRs & width')

        # add total widths to sparameter substitions dictionary (the last element)
        paramsubs['width1'] = h1_BRs[-1]
        paramsubs['width2'] = h2_BRs[-1]
        paramsubs['width3'] = h3_BRs[-1]

        # cross sections for single production of h1,2,3 at N3LO at 13 TeV:
        xs13_n3lo_h1 = round_sig(R[0][0]**2 * XS_interpolator_SM_13TeV_N3LO(M1),5)
        xs13_n3lo_h2 = round_sig(R[1][0]**2 * XS_interpolator_SM_13TeV_N3LO(M2),5)
        xs13_n3lo_h3 = round_sig(R[2][0]**2 * XS_interpolator_SM_13TeV_N3LO(M3),5)
        if PRINT: 
            print('single hX xs@13 TeV at N3LO (narrow width):')
            print(('sigma(h1)=', xs13_n3lo_h1, 'pb'))
            print(('sigma(h2)=', xs13_n3lo_h2, 'pb'))
            print(('sigma(h3)=', xs13_n3lo_h3, 'pb'))
        
            # cross sections for h2 -> h1 h1 and h3 -> h1 h1: (11th component of the hX_BRs arrays)
            print('\nhX -> h1 h1 xs@13 TeV at N3LO (narrow width):')
            print(('sigma(h2)*BR(h2->h1h1)=', xs13_n3lo_h2 * h2_BRs[11], 'pb'))
            print(('sigma(h3)*BR(h3->h1h1)=', xs13_n3lo_h3 * h3_BRs[11], 'pb'))
        return v, vs, vx, M1, M2, M3, a12, a13, a23, R, lambda_dict, xs13_n3lo_h1, xs13_n3lo_h2, xs13_n3lo_h3, h1_BRs, h2_BRs, h3_BRs, paramsubs

    # write out the parameter card:
    def write_param_card(paramfile, paramsubs):
        print('Writing param_card.dat with parameters:', paramsubs)
        # writeFile('param_card.dat', param_card_template.substitute(paramsubs) )
        writeFile(paramfile, param_card_template.substitute(paramsubs) )


    def convert_to_HBHS(name, v, vs, vx, M1, M2, M3, a12, a13, a23, R, lambda_dict, xs13_n3lo_h1, xs13_n3lo_h2, xs13_n3lo_h3, h1_BRs, h2_BRs, h3_BRs, paramsubs):
        point_info = [name, M1, M2, M3, h1_BRs[-1], h2_BRs[-1], h3_BRs[-1], R[0][0], R[1][0], R[2][0], h1_BRs, h2_BRs, h3_BRs, xs13_n3lo_h2, xs13_n3lo_h3]
        return point_info


    ###################
    # WRITE CARD HERE:#
    ###################

    WRITECARD = True

    if WRITECARD is True:
        v = 246.
        vs = vs_input
        vx = vx_input
        M1 = mH1_input
        M2 = mH2_input
        M3 = mH3_input
        a12 = thetahS_input
        a13 = thetahX_input
        a23 = thetaSX_input

        # BP3 (point H in 2101.00037) from 1908.08554
        # v = 246.
        # vs = 140.
        # vx = 100.
        # M1 = 125.09
        # M2 = 263
        # M3 = 455
        # a12=-0.129
        # a13= 0.226
        # a23=-0.899


        # for Tania 18/5/2023
        #vs=220
        #vx=150
        #M1 = 125.09
        #M2 = 130.4
        #M3 = 367.6
        #a12=0.207
        #a13=0.146
        #a23=0.782

        # get the point info 
        v, vs, vx, M1, M2, M3, a12, a13, a23, R, lambda_dict, xs13_n3lo_h1, xs13_n3lo_h2, xs13_n3lo_h3, h1_BRs, h2_BRs, h3_BRs, paramsubs = get_point_info(v, vs, vx, M1, M2, M3, a12, a13, a23, False)

        # print Lambdas here
        #print('lambda_dict=', lambda_dict)
        #print('lambdas for hhh=[', lambda_dict[(1,1,1)],',', lambda_dict[(1,1,2)],',', lambda_dict[(1,1,3)],',', lambda_dict[(1,2,3)],',', lambda_dict[(1,2,2)],',', lambda_dict[(1,1,1,1)],',', lambda_dict[(1,1,1,2)],',', lambda_dict[(1,1,1,3)], ',', lambda_dict[(1,1,3)], ']')

        # write out the param_card.dat with the given paramsubs obtained for the point
        # write_param_card('param_card.dat', paramsubs)
        write_param_card(pathParam_card, paramsubs)


def generateScript(pathOutput, pathMadgraphOutput, pathRun_card, pathLoop_sm_twoscalar,
                   nevents, process):
    '''
    Creates a madgraph script in the location pathOutput for a process
    e.g. 
    process = 'p p > eta0 h / iota0 [noborn=QCD]' or
    process = 'p p > eta0 h  [noborn=QCD]'.

    pathMadgraphOutput is the path madgraph will generate its output when
    the script generated by this function is run.

    User must specify the path to the loop_sm_two_scalar directory in the TRSM
    model https://gitlab.com/apapaefs/twosinglet

    returns the path to the script
    '''

    script = f'''#************************************************************
#*                     MadGraph5_aMC@NLO                    *
#*                                                          *
#*                *                       *                 *
#*                  *        * *        *                   *
#*                    * * * * 5 * * * *                     *
#*                  *        * *        *                   *
#*                *                       *                 *
#*                                                          *
#*                                                          *
#*         VERSION 3.5.3                 2023-12-23         *
#*                                                          *
#*    The MadGraph5_aMC@NLO Development Team - Find us at   *
#*    https://server06.fynu.ucl.ac.be/projects/madgraph     *
#*                                                          *
#************************************************************
#*                                                          *
#*               Command File for MadGraph5_aMC@NLO         *
#*                                                          *
#*     run as ./bin/mg5_aMC  filename                       *
#*                                                          *
#************************************************************
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
define l+ = e+ mu+
define l- = e- mu-
define vl = ve vm vt
define vl~ = ve~ vm~ vt~
set stdout_level DEBUG
convert model {pathLoop_sm_twoscalar}/loop_sm_twoscalar
import model {pathLoop_sm_twoscalar}/loop_sm_twoscalar
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
generate {process}
output {pathMadgraphOutput}
launch
0
set iseed 123
set nevents {str(nevents)}
set width 99925 auto
set width 99926 auto
set width 25 auto
{pathRun_card}
0
    '''
# set output_dependencies internal
# set use_syst False
# set pdlabel none
# remember to remove 'set use_syst False'

    pathMadgraph_script = os.path.join(pathOutput, 'scriptMadgraph')

    with open(pathMadgraph_script, "w") as scriptFile:
        scriptFile.write(script)

    return pathMadgraph_script


def mainExecution(pathOutput, pathTempParam_card, pathLoop_sm_twoscalar, nevents, process, runName):
    '''
    This is the function executed in the loop in main.

    pathOutput: confusingly defined as the directory where the madgraph 
    output is stored.
    pathTempParam_card: path to the param_card
    pathLoop_sm_twoscalar: path to the TRSM model
    nevents: number of madgraph events for the process
    process: the physical process in madgraph syntax e.g.
    p p > eta0 h / iota0 [noborn=QCD]
    runName: the name of the output from Madgraph. The output can be found
    in pathOutput as 'outputMadgraph_[directory name of pathOutput]_[runName]'
    '''

    # madgraph output path
    outputMadgraphName = f'outputMadgraph_{os.path.basename(pathOutput)}_{runName}'
    pathMadgraphOutput = os.path.join(pathOutput, outputMadgraphName)

    # generate madgraph script
    pathMadgraphScript = generateScript(pathOutput, pathMadgraphOutput, pathTempParam_card, pathLoop_sm_twoscalar, 
                                        nevents, process)

    # check if param_card generated any widths
    # which are nan and return appropriate cross
    # sections in that case (see if, elif below)
    paramCard = ''
    with open(os.path.join(pathMadgraphOutput, pathTempParam_card)) as file:
        for row in file:
            paramCard = paramCard + row
            
    patternH = re.compile('DECAY 25 nan \# wh')
    patternEta = re.compile('DECAY 99925 nan \# weta')
    patternIota = re.compile('DECAY 99926 nan \# wiota')

    lineCrossSecH = patternH.findall(paramCard)
    lineCrossSecEta = patternEta.findall(paramCard)
    lineCrossSecIota = patternIota.findall(paramCard)

    # crossSecUncert is set to -1 to alert the user
    # that the width of h is nan and Madgraph will
    # raise an error if the param_card with these
    # settings are run
    if len(lineCrossSecH) != 0:
        crossSec = -1
        crossSecUncert = -1
        return crossSec, crossSecUncert

    # crossSecUncert is set to -2 to alert the user
    # that the width of eta is nan and Madgraph will
    # raise an error if the param_card with these
    # settings are run
    elif len(lineCrossSecEta) != 0:
        crossSec = -1
        crossSecUncert = -1
        return crossSec, crossSecUncert
        
    # crossSecUncert is set to -3 to alert the user
    # that the width of iota is nan and Madgraph will
    # raise an error if the param_card with these
    # settings are run
    elif len(lineCrossSecIota) != 0:
        crossSec = -1
        crossSecUncert = -1
        return crossSec, crossSecUncert

    else:
        pass

    # if no nan widths were found, run Madgraph
    
    # run madgraph
    runMadgraph = [pathMadgraph, pathMadgraphScript]

    # run the executable
    shell_output = subprocess.run(runMadgraph, cwd=pathOutput,
                                  capture_output=True, text=True)

    print('printing Madgraph stdout and stderr...')
    print(shell_output.stdout)
    print(shell_output.stderr)
    
    # regex pattern
    pattern = re.compile('Current estimate of cross-section.*')

    # find substring with cross sections
    lineCrossSec = pattern.findall(shell_output.stdout)

    crossSecString = lineCrossSec[0].split()

    crossSec = float(crossSecString[4])
    crossSecUncert = float(crossSecString[6])

    return crossSec, crossSecUncert


if __name__ == '__main__':

    # all output from this script (madgraph and .csv files)
    # will be identified with runName
    runName = sys.argv[1]
    
    # read in path to madgraph executable
    pathMadgraph = sys.argv[2]

    # read in path to file with model parameters
    pathConfig = sys.argv[3]
    df = pandas.read_table(pathConfig)

    # path to output directory
    pathOutput = sys.argv[4]

    # path to TRSM model
    pathLoop_sm_twoscalar = sys.argv[5]

    # number of Madgraph events
    nevents = sys.argv[6]
    # nevents = 100

    # create dictionary where madgraph output will be stored
    dictCrossSec = {}
    dictCrossSec['mH1'], dictCrossSec['mH2'], dictCrossSec['mH3'] = [], [], []
    dictCrossSec['thetahS'], dictCrossSec['thetahX'], dictCrossSec['thetaSX'] = [], [], []
    dictCrossSec['vs'], dictCrossSec['vx'] = [], []
    dictCrossSec['pp_iota0_eta0h'], dictCrossSec['pp_iota0_eta0h_uncert'] = [], [] 
    dictCrossSec['pp_eta0h'], dictCrossSec['pp_eta0h_uncert'] = [], []
    dictCrossSec['ratio'] = []

    for i in range(len(df)):
        # read model parameters from df
        mH1_input = df['mH1'][i]
        mH2_input = df['mH2'][i]
        mH3_input = df['mH3'][i]
        thetahS_input = df['thetahS'][i]
        thetahX_input = df['thetahX'][i]
        thetaSX_input = df['thetaSX'][i] 
        vs_input = df['vs'][i]
        vx_input = df['vx'][i]

        # store in dictionary
        dictCrossSec['mH1'].append(mH1_input)
        dictCrossSec['mH2'].append(mH2_input)
        dictCrossSec['mH3'].append(mH3_input)
        dictCrossSec['thetahS'].append(thetahS_input)
        dictCrossSec['thetahX'].append(thetahX_input)
        dictCrossSec['thetaSX'].append(thetaSX_input)
        dictCrossSec['vs'].append(vs_input)
        dictCrossSec['vx'].append(vx_input)

        # path to param_card
        pathTempParam_card = os.path.join(pathOutput, f'tempParam_card_{str(i)}.dat')

        # generate param_card
        generateCard(pathTempParam_card,
                     mH1_input, mH2_input, mH3_input,
                     thetahS_input, thetahX_input, thetaSX_input, 
                     vs_input, vx_input)

        # generate p p > eta0 h / iota0 [noborn=QCD]
        crossSec_no_iota0, crossSecUncert_no_iota0 = mainExecution(pathOutput, pathTempParam_card, pathLoop_sm_twoscalar, 
                                                 nevents, 'p p > iota0 > eta0 h [noborn=QCD]', f'pp_iota0_eta0h_{i}')
        
        dictCrossSec['pp_iota0_eta0h'].append(crossSec_no_iota0)
        dictCrossSec['pp_iota0_eta0h_uncert'].append(crossSecUncert_no_iota0)

        # generate p p > eta0 h [noborn=QCD]
        crossSec, crossSecUncert = mainExecution(pathOutput, pathTempParam_card, pathLoop_sm_twoscalar,
                                                             nevents, 'p p > eta0 h [noborn=QCD]', f'pp_eta0h_{i}')

        dictCrossSec['pp_eta0h'].append(crossSec)
        dictCrossSec['pp_eta0h_uncert'].append(crossSecUncert)

        # cross sections set to -1 when the generate card
        # generates nan widths, see mainExecution
        if crossSec_no_iota0 == -1 and crossSec == -1:
            ratio = 0

        # calculate ratio
        else:
            ratio = crossSec/crossSec_no_iota0

        dictCrossSec['ratio'].append(ratio)

    # create dataframe out of dictCrossSec
    # and create a csv file out of the dataframe
    dfCSV = pandas.DataFrame(dictCrossSec)

    # quick fix to get the dataId, not a good solution...
    dataId = (pathOutput.split('/'))[-2]

    pathCSV = os.path.join(pathOutput, f'output_{dataId}_{runName}.tsv')
    dfCSV.to_csv(pathCSV, sep='\t')

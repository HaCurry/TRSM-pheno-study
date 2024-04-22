# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:16:40 2023

@author: Iram Haque
"""

import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects
import scipy.interpolate
from scipy.interpolate import CubicSpline
matplotlib.rcParams.update(matplotlib.rcParamsDefault)


def observables(pathObservables, SM1, SM2, *args, **kwargs):
    '''
    Calculates observables such as cross sections, branching ratios of the process
    gg -> H3 -> Ha Hb > SM1 SM2 and returns a dictionary with such observables. 
    
    Note, observables refers to anything from the ScannerS TRSM output and 
    anything calculated from the output.

    pathObservables: string
        path to ScannerS TRSM executable output.

    SM1: string
        Standard model final state.
    
    SM2: string
        Standard model final state.

    args*: string
        additional observables found in the ScannerS TRSM executable output
        that the user wants stored in the dictionary such as 'thetahS',
        'thetahX', 'thetaSX', 'vs', 'vx', 'mH1', 'mH2', 'mH3' or anything
        else found in the ScannerS TRSM output.

    **kwargs:

    prodMode: string, default: 'gg'
        the production mode for  H3. Other possible production modes includes
        'vbf'.

    normSM: float, default: (31.05 * 10**(-3)) * 0.002637 
        normalizes the cross section gg -> Ha Hb -> SM1 SM2
        by normSM. Default value is the standard model HH cross section
        multiplied by the bb gamgam branching ratio taken. Values can be
        found in:
        https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH
        and
        https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR?sortcol=0;table=1;up=0#sorted_table

    kineticExclude: bool, default: False
        excludes observables which do not obey mH3 > mH1 + mH2 with the
        tolerance kineticExcludeEps.

    kineticExcludeEps: float, default: 10**(-10)
        if kineticExclude = True then the constraint mH3 > mH1 + mH2
        is applied with the tolerance mH3 - (mH1 + mH2) > kineticExcludeEps.
        In principle the user will never have to interact with this value.

    pathRun3Data: string, default: None
        path to gg -> HSM cross sections (or other mode) in .tsv format.
        All observables to calculate the cross section of 
        gg -> H3 -> Ha Hb -> SM1 SM2 will be taken from the ScannerS TRSM
        output (pathObservables) except the first step gg -> H3 where
        the cross section of gg -> HSM is taken from pathRun3Data and using
        \sigma(gg -> H3) = \kappa^{2} * \sigma(gg -> HSM) (see TRSM paper) 
        and using the NWA the new cross section gg -> H3 -> Ha Hb -> SM1 SM2
        is calculated.

    keyMassRun3: string, default: 'mass'
        the column header of the masses in pathRun3Data. 

    keyCrossSecRun3: string, default: 'crossSec'
        the column header of the cross sections in pathRun3Data

    saveAll: bool, default: False
        saves some additional observables used when calculating the cross section
        gg -> H3 -> Ha Hb -> SM1 SM2.

    returns:
        observables: dict
        dictionary with all observables. The possible observables and their keys
        (a and b are integers with possible values 1, 2, 3 and SMi, SMj are SM final states
        e.g. 'bb', 'gamgam', 'tautau', see ScannerS TRSM output for possible SM final states)
        
        'b_Ha_SMi_Hb_SMj' branching ratio Ha(SMi) Hb(SMj) 
        'b_HaHb_SMiSMj' branching ratio Ha Hb -> SMi SMj
        'x_Ha_Hb_SMi_Hc_SMj' cross section gg -> Ha -> Hb(SMi) Hc(SMj) 
        'x_Ha_HaHb_SMiSMj' cross section gg -> Ha -> Hb Hc -> SMi SMj

        if saveAll = True, then the following additional observables are available
        'b_H3_HaHb' branching ratio H3 -> Ha Hb (a and b can only be set to 1 or 2 here),
        'x_Ha' cross section gg -> Ha (unless prodMode set by user)
        'b_Ha_SMi' branching ratio Ha -> SMi

        and any other observable specified by args available in the ScannerS TRSM output.
    '''

    #################################### kwargs ####################################

    # default production mode is ggF, but user can chose otherwise
    if 'prodMode' in kwargs:
        prodMode = kwargs['prodMode']

    else: prodMode = 'gg'

    # path to gg -> HSM cross sections (e.g. 13.6 TeV cross sections)
    if 'pathRun3Data' in kwargs:
        run3 = True
        pathRun3Data = kwargs['pathRun3Data']

        if 'keyMassRun3' in kwargs:
            keyMassRun3 = kwargs['keyMassRun3']

        else: keyMassRun3 = 'mass'

        if 'keyCrossSecRun3' in kwargs:
            keyCrossSecRun3 = kwargs['keyCrossSecRun3']

        else: keyCrossSecRun3 = 'crossSec'


    else:
        run3 = False

    # normalise the cross sections gg -> Ha Hb -> SM1 SM2 by 
    # standard model HH cross section
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH
    # and standard model bb gamgam branching ratio
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR?sortcol=0;table=1;up=0#sorted_table
    if 'normSM' in kwargs:
        normSM = kwargs['normSM']

    else:
        normSM = (31.05 * 10**(-3)) * 0.002637

    # this stores some additional observables (BR, XS) in the
    # returned dictionary to the user if set to True
    if 'saveAll' in kwargs:
        saveAll = kwargs['saveAll']

    else: saveAll = False

    # excludes observables which do not obey the constraint
    # mH3 > mH1 + mH2
    if 'kineticExclude' in kwargs:
        kineticExclude = kwargs['kineticExclude']

        # the tolerance to uphold the constraint
        # mH3 - (mH1 + mH2) > kineticExcludeEps
        if 'kineticExcludeEps' in kwargs:
            kineticExcludeEps = kwargs['kineticExcludeEps']

        else:
            kineticExcludeEps = 10**(-10)

    else:
        kineticExclude = False


    ################################################################################
    
    df = pandas.read_table(pathObservables, index_col=0)    

    # if dataframe is empty, meaning no ScannerS output in pathObservables 
    # return an empty dictionary
    if len(df) == 0:
        return {}

    else:
        pass

    # this dictionary will be returned to the user
    observables = {}
    
    # for temporary storage (unles saveAll = True)
    # then observables and tempObservables will be merged
    tempObservables = {}
    
    tempObservables['b_H3_H1H2'] = [i for i in df['b_H3_H1H2']]
    tempObservables['b_H3_H1H1'] = [i for i in df['b_H3_H1H1']]
    tempObservables['b_H3_H2H2'] = [i for i in df['b_H3_H2H2']]

    tempObservables['x_H1'] = [i for i in df[f'x_H1_{prodMode}']]
    tempObservables['x_H2'] = [i for i in df[f'x_H2_{prodMode}']]
    tempObservables['x_H3'] = [i for i in df[f'x_H3_{prodMode}']]
        
    tempObservables[f'b_H1_{SM1}'] = [i for i in df[f'b_H1_{SM1}']] #"b_H1_bb"
    tempObservables[f'b_H1_{SM2}'] = [i for i in df[f'b_H1_{SM2}']] #"b_H1_gamgam"
    tempObservables[f'b_H2_{SM1}'] = [i for i in df[f'b_H2_{SM1}']] #"b_H2_bb"
    tempObservables[f'b_H2_{SM2}'] = [i for i in df[f'b_H2_{SM2}']] #"b_H2_gamgam"
    

        
    # branching ratio H1(SM1) H2(SM2)    
    tempObservables[f'b_H1_{SM1}_H2_{SM2}'] = [tempObservables[f'b_H1_{SM1}'][i] * tempObservables[f'b_H2_{SM2}'][i]
    for i in range(len(df))]

    # branching ratio H1(SM2) H2(SM1)
    tempObservables[f'b_H1_{SM2}_H2_{SM1}'] = [tempObservables[f'b_H1_{SM2}'][i] * tempObservables[f'b_H2_{SM1}'][i]
        for i in range(len(df))]

    # branching ratio H1H2 -> SM1 SM2    
    tempObservables[f'b_H1H2_{SM1}{SM2}'] = [tempObservables[f'b_H1_{SM1}_H2_{SM2}'][i] + tempObservables[f'b_H1_{SM2}_H2_{SM1}'][i] 
        for i in range(len(df))]

    # symmetry factor in the case H1H1 and H2H2 decays to SM1, SM2
    # and SM1 != SM2
    if SM1 != SM2:
        symFact = 2

    else: symFact = 1
    
    # branching ratio H1H1 -> SM1 SM2
    tempObservables[f'b_H1H1_{SM1}{SM2}'] = [symFact * tempObservables[f'b_H1_{SM1}'][i] * tempObservables[f'b_H1_{SM2}'][i]
        for i in range(len(df))]
    
    # branching ratio H2H2 -> SM1 SM2
    tempObservables[f'b_H2H2_{SM1}{SM2}'] = [symFact * tempObservables[f'b_H2_{SM1}'][i] * tempObservables[f'b_H2_{SM2}'][i]
        for i in range(len(df))]

    # save cross sections from pathRun3Data in observables for calculating
    # cross sections using the NWA later
    if run3 == True:
        dfRun3 = pandas.read_table(pathRun3Data)
        epsilon = 10**(-6)
        
        # quick sanity check
        if abs(len(dfRun3[keyMassRun3]) + len(dfRun3[keyCrossSecRun3]) - 2 * len(dfRun3)) > epsilon:
            raise Exception(f'length of columns in {pathRun3Data} are not equal')

        # create splines fitting the cross sections
        run3_x_HSM_gg = CubicSpline(np.array(dfRun3[keyMassRun3]), np.array(dfRun3[keyCrossSecRun3]))

        # create TRSM cross sections from the cross sections given in pathRun3Data
        tempObservables['x_H3'] = [(df['R31'][i]**2) * run3_x_HSM_gg(df['mH3'][i]) for i in range(len(df))]

    else: pass

    # cross sections gg -> H3 -> H1H2
    tempObservables['x_H3_H1H2'] = [tempObservables['x_H3'][i] * tempObservables['b_H3_H1H2'][i] 
        for i in range(len(df))]
    
    # cross sections gg -> H3 -> H1H1
    tempObservables['x_H3_H1H1'] = [tempObservables['x_H3'][i] * tempObservables['b_H3_H1H1'][i] 
        for i in range(len(df))]

    # cross sections gg -> H3 -> H2H2
    tempObservables['x_H3_H2H2'] = [tempObservables['x_H3'][i] * tempObservables['b_H3_H2H2'][i] 
        for i in range(len(df))]
    
    # cross section gg -> H3 -> H1(SM1) H2(SM2)
    observables[f'x_H3_H1_{SM1}_H2_{SM2}'] = [(tempObservables['x_H3_H1H2'][i] * tempObservables[f'b_H1_{SM1}_H2_{SM2}'][i])/normSM
        for i in range(len(df))]
    
    # cross section gg -> H3 -> H1(SM2) H2(SM1)
    observables[f'x_H3_H1_{SM2}_H2_{SM1}'] = [(tempObservables['x_H3_H1H2'][i] * tempObservables[f'b_H1_{SM2}_H2_{SM1}'][i])/normSM
        for i in range(len(df))]
    
    # cross section gg -> H3 -> H1 H2 -> SM1 SM2
    observables[f'x_H3_H1H2_{SM1}{SM2}'] = [(tempObservables['x_H3_H1H2'][i] * tempObservables[f'b_H1H2_{SM1}{SM2}'][i])/normSM
        for i in range(len(df))]
    
    # cross section gg -> H3 -> H1 H1 -> SM1 SM2
    observables[f'x_H1H1_{SM1}{SM2}'] = [(tempObservables['x_H3_H1H1'][i] * tempObservables[f'b_H1H1_{SM1}{SM2}'][i])/normSM
        for i in range(len(df))]
    
    # cross section gg -> H3 -> H2 H2 -> SM1 SM2
    observables[f'x_H2H2_{SM1}{SM2}'] = [(tempObservables['x_H3_H2H2'][i] * tempObservables[f'b_H2H2_{SM1}{SM2}'][i])/normSM
        for i in range(len(df))]

    # sanity checks to see all rows in the dataframe are of equal length
    # these lines can be ignored
    epsilon = 10**(-6)
    rows = 0
    
    for key in observables:
        rows = rows + len(observables[key])
    
    check = rows/(len(df) * len(observables))
    if  abs(check - 1)  > + epsilon:
        raise Exception('length of lists not equal in ppXNPSM_massfree')
    
    # if user wants to store specific observables found in the
    # ScannerS TRSM output (e.g. vevs, angles etc.) the user
    # can specify the observables in args
    for arg in args:
        observables[arg] = [i for i in df[arg]]

    # make sure that user gets the pathRun3Data TRSM cross sections
    if run3 == True:
        observables['x_H3'] = tempObservables['x_H3']

    # if user wants all the observables required when calculating
    # the cross sections
    if saveAll == True:
        observables = tempObservables | observables

    else:
        pass

    # keep only observables obeying mH3 > mH1 + mH2
    if kineticExclude == True:

        # create temporary dictionary
        kineticExcludedObs = {}
        for key in observables:
            kineticExcludedObs[key] = []

        # loop over dataframe
        for i in range(len(df)):

            # if mH3 > mH1 + mH2 keep the observables otherwise continue
            if observables['mH3'][i] - (observables['mH1'][i] + observables['mH2'][i]) > kineticExcludeEps:
                for key in observables:
                    kineticExcludedObs[key].append(observables[key][i])

            else:
                continue

        observables = kineticExcludedObs

    return observables


def ppXNPSM_massfree(BPdirectory, axes1, axes2, axes3, SM1, SM2, normalizationSM = (31.02 * 10**(-3)) * 0.0026, **kwargs):

    #################################### kwargs ####################################

    # if 'run3' in kwargs and kwargs['run3'] == True:

        # run3 = True

    if 'pathRun3Data' in kwargs:
        run3 = True
        pathRun3Data = kwargs['pathRun3Data']

        # else: raise Exception('run3 is set to True, path to run 3 cross sections required')

        if 'keyMassRun3' in kwargs:
            keyMassRun3 = kwargs['keyMassRun3']

        else: keyMassRun3 = 'mass'

        if 'keyCrossSecRun3' in kwargs:
            keyCrossSecRun3 = kwargs['keyCrossSecRun3']

        else: keyCrossSecRun3 = 'crossSec'


    else:
        run3 = False

    ################################################################################
    
    df = pandas.read_table(BPdirectory)#, index_col = 0)
    # PC
    # df = pandas.read_table ( r"\\wsl.localslhost\Ubuntu\home\iram\scannerS\ScannerS-master\build\output_file.tsv" , index_col =0)
    
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
    # if energy == 13
    x_H3_gg_H1H2 = [i for i in df["x_H3_gg"]]
    x_H3_gg_H1H1 = x_H3_gg_H1H2.copy()
    x_H3_gg_H2H2 = x_H3_gg_H1H2.copy()
    # elif energy == 13.6
    # x_H3_gg_H1H2 = run3Interp(massList)
    
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
    # b_H1H2_bbgamgam = [b_H1_bb[i] * b_H2_gamgam[i] + b_H2_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
    b_H1H1_bbgamgam = [b_H1_bb[i] * b_H1_gamgam[i] for i in range(len(b_H1_bb))]
    b_H2H2_bbgamgam = [b_H2_bb[i] * b_H2_gamgam[i] for i in range(len(b_H2_bb))]

    if run3 == True:
        del x_H3_gg_H1H2, x_H3_gg_H1H1, x_H3_gg_H2H2

        dfRun3 = pandas.read_table(pathRun3Data)
        run3_x_HSM_gg = CubicSpline(np.array(dfRun3[keyMassRun3]), np.array(dfRun3[keyCrossSecRun3]))
        x_H3_gg_H1H2 = [(df['R31'][i]**2) * run3_x_HSM_gg(mH3_H1H2[i]) for i in range(len(mH3_H1H2))]
        x_H3_gg_H1H1 = x_H3_gg_H1H2.copy()
        x_H3_gg_H2H2 = x_H3_gg_H1H2.copy()

    else: pass

    ggF_bbgamgam_xs_SM_Higgs = normalizationSM
    # bbgamgam BR: https://inspirehep.net/files/a34811e0b9462ca5900081ffe6c92bdb
    # ggF XS: https://cds.cern.ch/record/2764447/files/ATL-PHYS-SLIDE-2021-092.pdf
    # ggF_bbgamgam_xs_SM_Higgs = (31.02 * 10**(-3)) * 0.0026  
    # ggF_bbgamgam_xs_SM_Higgs = (31.02 * 10**(-3)) * (10**(-2)*0.028)  
    # ggF_bbgamgam_xs_SM_Higgs = 1 
    
    # rescaled cross-section
    pp_X_H1H2_bbgamgam = [(b_H1H2_bbgamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H1H2_bbgamgam))]
    # pp_X_H1H2_bbgamgam = [x_H3_gg_H1H2[i] *  b_H3_H1H2[i] for i in range(len(b_H1H2_bbgamgam))]
    
    pp_X_H1H1_bbgamgam = [(b_H1H1_bbgamgam[i] * x_H3_gg_H1H1[i] * b_H3_H1H1[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H1H1_bbgamgam))]
    # pp_X_H1H1_bbgamgam = [ x_H3_gg_H1H1[i] * b_H3_H1H1[i] for i in range(len(b_H1H1_bbgamgam))]
    
    pp_X_H2H2_bbgamgam = [(b_H2H2_bbgamgam[i] * x_H3_gg_H2H2[i] * b_H3_H2H2[i])/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H2H2_bbgamgam))]
    # pp_X_H2H2_bbgamgam = [x_H3_gg_H2H2[i] * b_H3_H2H2[i] for i in range(len(b_H2H2_bbgamgam))]
    
    
    pp_X_H1_bb_H2_gamgam = [b_H1_bb_H2_gamgam[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
    # pp_X_H1_bb_H2_gamgam = [x_H3_gg_H1H2[i] * b_H3_H1H2[i] for i in range(len(b_H3_H1H2))]
    pp_X_H1_gamgam_H2_bb = [b_H1_gamgam_H2_bb[i] * x_H3_gg_H1H2[i] * b_H3_H1H2[i]/ggF_bbgamgam_xs_SM_Higgs for i in range(len(b_H3_H1H2))]
    # pp_X_H1_gamgam_H2_bb = [x_H3_gg_H1H2[i] * b_H3_H1H2[i] for i in range(len(b_H3_H1H2))]
    
    
        
    H1H2 = np.array([mH1_H1H2, mH2_H1H2, mH3_H1H2, pp_X_H1H2_bbgamgam, pp_X_H1_bb_H2_gamgam, pp_X_H1_gamgam_H2_bb])
    H1H1 = np.array([mH1_H1H1, mH2_H1H1, mH3_H1H1, pp_X_H1H1_bbgamgam])
    H2H2 = np.array([mH1_H2H2, mH2_H2H2, mH3_H2H2, pp_X_H2H2_bbgamgam])
    
    return H1H2, H1H1, H2H2


def comparer(observables, H1H2, H1H1=None, H2H2=None, SM1='bb', SM2='gamgam', eps=10**(-17)):
    '''
    Script that checks that the output from observable and ppXNPSM_massfree
    is the same so that ppXNPSM can be deprecated and replaced by the better
    function observables
    '''
    if len(observables['mH1']) == len(H1H2[0]):
        print(len(observables['mH1']), len(H1H2[0]))
      
    else:
        raise Exception('something went wrong the masses are not of equal length')

    if len(observables['mH2']) == len(H1H2[1]):
        print(len(observables['mH2']), len(H1H2[1]))
        
    else:
        raise Exception('something went wrong the masses are not of equal length')
    
    if len(observables['mH3']) == len(H1H2[2]):
        print(len(observables['mH3']), len(H1H2[2]))
        
    else:
        raise Exception('something went wrong the masses are not of equal length')

    if len(observables[f'x_H3_H1H2_{SM1}{SM2}']) == len(H1H2[3]):
        print(len(observables[f'x_H3_H1H2_{SM1}{SM2}']), len(H1H2[3]))

    else:
        raise Exception('something went wrong the total cross sections are not equal')
    
    if len(observables[f'x_H3_H1_{SM1}_H2_{SM2}']) == len(H1H2[4]):
        print(len(observables[f'x_H3_H1_{SM1}_H2_{SM2}']), len(H1H2[4]))

    else:
        raise Exception('Something went wrong the cross section 4 is not equal')
    
    if len(observables[f'x_H3_H1_{SM2}_H2_{SM1}']) == len(H1H2[5]):
        print(len(observables[f'x_H3_H1_{SM2}_H2_{SM1}']), len(H1H2[5]))
        
    else:
        raise Exception('Something went wrong the cross section 5 is not equal')

    print('Checking H1H2...')
    
    for i in range(len(H1H2[0])):
        if (abs(observables['mH1'][i] - H1H2[0][i]) > eps or
        abs(observables['mH2'][i] - H1H2[1][i]) > eps or
        abs(observables['mH3'][i] - H1H2[2][i]) > eps or
        abs(observables[f'x_H3_H1H2_{SM1}{SM2}'][i] - H1H2[3][i]) > eps or
        abs(observables[f'x_H3_H1_{SM1}_H2_{SM2}'][i] - H1H2[4][i]) > eps or
        abs(observables[f'x_H3_H1_{SM2}_H2_{SM1}'][i] - H1H2[5][i]) > eps):
            print(f'epsilon: {eps}')
            print('mH1', abs(observables['mH1'][i] - H1H2[0][i]))
            print('mH2', abs(observables['mH2'][i] - H1H2[1][i]))
            print('mH3', abs(observables['mH3'][i] - H1H2[2][i]))
            print(f'x_H3_H1H2_{SM1}{SM2}', abs(observables[f'x_H3_H1H2_{SM1}{SM2}'][i] - H1H2[3][i]))
            print(f'x_H3_H1_{SM1}_H2_{SM2}', abs(observables[f'x_H3_H1_{SM1}_H2_{SM2}'][i] - H1H2[4][i]))
            print(f'x_H3_H1_{SM2}_H2_{SM1}', abs(observables[f'x_H3_H1_{SM2}_H2_{SM1}'][i] - H1H2[5][i]))
            raise Exception('something went wrong in one of the observables above...')

        else:
            pass

    print('H1H2 passed tests')

    # note H1H1 and H2H2 misses a symmetry factor when SM1 != SM2 
    # in ppXNPSM_massfree so will allways fail
    if H1H1 != None and H2H2 != None:
        print('note H1H1 and H2H2 misses a symmetry factor when SM1 != SM2\n\
              in ppXNPSM_massfree so this test will allways fail')
        
        if (len(observables['mH1']) == len(H1H1[0]) and
            len(observables['mH1']) == len(H2H2[0])):
            pass
        
        else:
            raise Exception('something went wrong the masses are not of equal length')

        if (len(observables['mH2']) == len(H1H1[1]) and
            len(observables['mH2']) == len(H2H2[1])):
            pass
        
        else:
            raise Exception('something went wrong the masses are not of equal length')
    
        if (len(observables['mH3']) == len(H1H1[2]) and
            len(observables['mH3']) == len(H2H2[2])):
            pass
        
        else:
            raise Exception('something went wrong the masses are not of equal length')

        if (len(observables[f'x_H3_H1H1_{SM1}{SM2}']) == len(H1H1[3]) and
            len(observables[f'x_H3_H2H2_{SM1}{SM2}']) == len(H2H2[3])):
            pass

        else:
            raise Exception('something went wrong the total cross sections are not equal')
        
        print('Checking H1H1...')
        for i in range(len(H1H1[0])):
            if (abs(observables['mH1'][i] - H1H1[0][i]) > eps and
            abs(observables['mH2'][i] - H1H1[1][i]) > eps and
            abs(observables['mH3'][i] - H1H1[2][i]) > eps and
            abs(observables[f'x_H3_H1H1_{SM1}{SM2}'][i] - H1H1[3][i]) > eps):
                print(f'epsilon: {eps}')
                print('mH1', abs(observables['mH1'][i] - H1H1[0][i]))
                print('mH2', abs(observables['mH2'][i] - H1H1[1][i]))
                print('mH3', abs(observables['mH3'][i] - H1H1[2][i]))
                print(f'x_H3_H1H1_{SM1}{SM2}', abs(observables[f'x_H3_H1H1_{SM1}{SM2}'][i] - H1H1[3][i]))
                raise Exception('something went wrong in one of the observables above...')

            else:
                pass

        print('H1H1 passed tests')

        print('Checking H2H2...')
        for i in range(len(H2H2[0])):
            if (abs(observables['mH1'][i] - H2H2[0][i]) > eps and
            abs(observables['mH2'][i] - H2H2[1][i]) > eps and
            abs(observables['mH3'][i] - H2H2[2][i]) > eps and
            abs(observables[f'x_H3_H2H2_{SM1}{SM2}'][i] - H2H2[3][i]) > eps):
                print(f'epsilon: {eps}')
                print('mH1', abs(observables['mH1'][i] - H2H2[0][i]))
                print('mH2', abs(observables['mH2'][i] - H2H2[1][i]))
                print('mH3', abs(observables['mH3'][i] - H2H2[2][i]))
                print(f'x_H3_H2H2_{SM1}{SM2}', abs(observables[f'x_H3_H2H2_{SM1}{SM2}'][i] - H2H2[3][i]))
                raise Exception('something went wrong in one of the observables above...')

            else:
                pass

        print('H2H2 passed tests')

    else:
        pass

    print('Testing complete, passed all tests!')

    


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


def plotmarkerAuto(markers, manualmarkers, visible, decimals, fsize, x, y, n):
    for i in range(len(markers)):
        pointS, pointX, br = pointfinder(5, (markers[i])[0], (markers[i])[1], x, y, n)
        plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        if visible == True:
            plt.plot(pointS, pointX, marker = 'o', mfc = 'none', color = 'r')


def plotmarkers(x, y, n, BP, mode, decimals, fsize):
    
    ''' deprecated '''
    
    if BP == 'BP2':
        
        if mode == 'XSH':
            
            # pointS, pointX, br = pointfinder(5, 45, 220, x, y, n)
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
            # plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            # region 1
        
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 125, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
            
            # region 2 & 3  
        
            pointS, pointX, br = pointfinder(5, 80, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
        
            pointS, pointX, br = pointfinder(5, 15, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 30, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 18, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 30, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 45, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 60, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 21, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 36, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 51, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 66, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 81, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 24, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 39, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 64, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 79, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 94, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
            pointS, pointX, br = pointfinder(5, 109, 240, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
        
        elif mode == 'XSS':
            
            # pointS, pointX, br = pointfinder(5, 50, 145, x, y, n)
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
            # plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            # region 1
            
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 125, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
            
            # region 2

            pointS, pointX, br = pointfinder(5, 22, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 20, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 38, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 42, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 55, 200, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 25, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 46, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 70, 225, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            # region 3 (high x mass)

            pointS, pointX, br = pointfinder(5, 60, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 77, 175, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 75, 190, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 85, 190, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 90, 203, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 98, 215, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            # region 3 (low x mass)

            pointS, pointX, br = pointfinder(5, 20, 135, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 40, 135, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 58, 135, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 40, 150, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 60, 150, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
            
            
        
        elif mode == 'XHH':
            
            # region 1
            
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 125, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
        
        else:
            raise Exception('Invalid mode in markerplot')
    
    elif BP == 'BP3':
        
        if mode == 'XSH':
            
            # plt.plot(180, 475, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 180, 475, x, y, n)
            # plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            # plt.plot(225, 400, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 225, 400, x, y, n)
            # plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            # region 2
    
            pointS, pointX, br = pointfinder(5, 200, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 200, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 390, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 230, 450, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 275, 500, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 300, 490, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 325, 480, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
        
        elif mode == 'XHH':
            
            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            # region 2
    
            pointS, pointX, br = pointfinder(5, 200, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 200, 375, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 390, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 230, 450, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 275, 500, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 300, 490, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 325, 480, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
            
            # region 3
            
            # plt.plot(220, 300, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 220, 300, x, y, n)
            # plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            
            pointS, pointX, br = pointfinder(5, 235, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 200, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 160, 275, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 190, 300, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 235, 300, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 235, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 223, 325, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 350, 465, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

            pointS, pointX, br = pointfinder(5, 375, 450, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)

        elif mode == 'XSS':
            
            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.text(pointS, pointX, r'%s'%str(round(br,decimals)), fontsize = fsize)




def plotmarkers2(x, y, n, BP, mode, formvar, xtext, ytext, fsize, rsize, lwidth = 1, fgcolor = "w"):
    
    ''' not like plotmarkerAuto. This uses annotate and has more options. 
    All points are hard coded using pointfinder '''
    
    if BP == 'BP2':
        
        if mode == 'XSH':
            
            # pointS, pointX, br = pointfinder(5, 45, 220, x, y, n)
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
            # plt.text(pointS, pointX, r'%s'%str(round(br, decimals)), fontsize = fsize)
        
            # region 1
        
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 110, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            # region 2 & 3  
        
            pointS, pointX, br = pointfinder(5, 80, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
        
            pointS, pointX, br = pointfinder(5, 15, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 30, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 18, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 30, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 45, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 60, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 21, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 36, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 51, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 66, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 81, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 24, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 39, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 64, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 79, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 94, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
            pointS, pointX, br = pointfinder(5, 109, 240, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
        
        elif mode == 'XSS':
            
            # pointS, pointX, br = pointfinder(5, 50, 145, x, y, n)
            # plt.plot(pointS, pointX, marker = "x", color = 'r')
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            # region 1
            
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 125, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            # region 2

            pointS, pointX, br = pointfinder(5, 22, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 20, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 38, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 42, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 55, 200, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 25, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 46, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 70, 225, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            # region 3 (high x mass)

            pointS, pointX, br = pointfinder(5, 60, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 77, 175, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 75, 190, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 85, 190, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 90, 203, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 98, 215, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            # region 3 (low x mass)

            pointS, pointX, br = pointfinder(5, 20, 135, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 40, 135, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 58, 135, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 40, 150, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 60, 150, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            
        
        elif mode == 'XHH':
            
            # region 1
            
            pointS, pointX, br = pointfinder(5, 40, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 60, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 80, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 100, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 120, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 45, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 65, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 85, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 105, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 125, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 50, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 70, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 90, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 60, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 80, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 100, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 70, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 90, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 110, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
        
        else:
            raise Exception('Invalid mode in markerplot')
    
    elif BP == 'BP3':
        
        if mode == 'XSH':
            
            # plt.plot(180, 475, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 180, 475, x, y, n)
            # plt.annotate(formvar.format(br), (pointS, pointX),
                 # textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 # path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            # plt.plot(225, 400, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 225, 400, x, y, n)
            # plt.annotate(formvar.format(br), (pointS, pointX),
                 # textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 # path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            pointS, pointX, br = pointfinder(5, 140, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            pointS, pointX, br = pointfinder(5, 200, 475, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            # region 2
    
            pointS, pointX, br = pointfinder(5, 200, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 200, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 390, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 230, 450, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 275, 500, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            pointS, pointX, br = pointfinder(5, 275, 450, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 300, 490, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 325, 480, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
        
        elif mode == 'XHH':
            
            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            # region 2
    
            pointS, pointX, br = pointfinder(5, 200, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 200, 375, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 390, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 230, 450, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 275, 500, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 300, 490, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 325, 480, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
            
            # region 3
            
            # plt.plot(220, 300, marker = 'x', color = 'r')
            # pointS, pointX, br = pointfinder(5, 220, 300, x, y, n)
            # plt.annotate(formvar.format(br), (pointS, pointX),
                 # textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 # path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            
            pointS, pointX, br = pointfinder(5, 235, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 200, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 160, 275, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 190, 300, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 235, 300, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 235, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 223, 325, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 350, 465, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

            pointS, pointX, br = pointfinder(5, 375, 450, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])

        elif mode == 'XSS':
            
            # region 1            

            pointS, pointX, br = pointfinder(5, 140, 350, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 140, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 425, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 175, 575, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])
    
            pointS, pointX, br = pointfinder(5, 225, 525, x, y, n)
            plt.annotate(formvar.format(br), (pointS, pointX),
                 textcoords = 'offset points', xytext= (xtext,ytext), fontsize = fsize, rotation = rsize, 
                 path_effects=[matplotlib.patheffects.withStroke(linewidth=lwidth, foreground=fgcolor)])





            
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

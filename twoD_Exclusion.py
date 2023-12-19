#-*- coding: utf-8 -*-
import pandas

import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.interpolate
mpl.rcParams.update(mpl.rcParamsDefault)

import subprocess
import configparser
import os
import datetime
import multiprocessing
import sys
import glob
import json

import functions as TRSM
import Exclusion_functions as excl
import parameterData
import twoDPlotter as twoDPlot


if __name__ == "__main__":

    #### BP2: ####

    # twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP2_check_prel_Mproc', 'compiled_AtlasBP2_check_prel_Mproc.tsv',
    #                   msKey='mHa_ub', mxKey='mHc_ub')   

    # twoDPlot.exclusionPlotter('compiled_AtlasBP2_check_prel_Mproc.tsv', 'plotsLimits/BP2', 0, 
    #                  xlims=(1, 124), ylims=(126, 500), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1_SM1_H2_SM2')

    dictBP2 = twoDPlot.pandasDynamicReader('compiled_AtlasBP2_check_prel_Mproc.tsv', ['ms', 'mx', 'ObservedLimit', 'x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'])
    twoDPlot.exclusionCheck(dictBP2['ObservedLimit'], dictBP2, ['x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'], 10**(-8))

    ## BP2: Observed Limits ##

    x = dictBP2['ms']
    y = dictBP2['mx']
    z = dictBP2['ObservedLimit']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP2: Exclusion Limits', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{obs}$', xlims=(1, 124), ylims=(126, 500))

    plt.savefig('plotsLimits/BP2/ObservedLimit1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP2: SM tot ##
   
    x = dictBP2['ms']
    y = dictBP2['mx']
    z = dictBP2['x_H3_H1H2_SM1SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP2: $\sigma(pp \\to X \\to SH \\to b\\bar{b}\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))

    plt.savefig('plotsLimits/BP2/x_H3_H1H2_SM1SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z

    
    ## BP2: SM H1 -> bb, H2 -> gamgam (1) ##
   
    x = dictBP2['ms']
    y = dictBP2['mx']
    z = dictBP2['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP2: $\sigma(pp \\to X \\to S(b\\bar{b})H(\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))

    plt.savefig('plotsLimits/BP2/x_H3_H1_SM1_H2_SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP2: SM H1 -> bb, H2 -> gamgam (2) ##
   
    x = dictBP2['ms']
    y = dictBP2['mx']
    z = dictBP2['x_H3_H1_SM2_H2_SM1']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP2: $\sigma(pp \\to X \\to S(\gamma\gamma)H(b\\bar{b}))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))

    plt.savefig('plotsLimits/BP2/x_H3_H1_SM2_H2_SM1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP2: ObsLim/(1) ##
   
    x = dictBP2['ms']
    y = dictBP2['mx']
    z = dictBP2['ObservedLimit']/dictBP2['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP2: $\sigma_{obs}/\sigma(S(b\\bar{b})H(\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))

    plt.savefig('plotsLimits/BP2/ObsDividedH1SM1H2SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    #### BP3: ####

    # twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP3_check_prel_Mproc', 'compiled_AtlasBP3_check_prel_Mproc.tsv',
    #                   msKey='mHb_ub', mxKey='mHc_ub')   

    # twoDPlot.exclusionPlotter('compiled_AtlasBP3_check_prel_Mproc.tsv', 'plotsLimits/BP3', 0, 
    #                  xlims=(126, 500), ylims=(255, 650), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1_SM1_H2_SM2')
    
    dictBP3 = twoDPlot.pandasDynamicReader('compiled_AtlasBP3_check_prel_Mproc.tsv', ['ms', 'mx', 'ObservedLimit', 'x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'])

    twoDPlot.exclusionCheck(dictBP3['ObservedLimit'], dictBP3, ['x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'], 10**(-8))

    ## BP3: Observed Limits ##

    x = dictBP3['ms']
    y = dictBP3['mx']
    z = dictBP3['ObservedLimit']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP3: Exclusion Limits', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{obs}$', xlims=(126, 500), ylims=(255, 650))

    plt.savefig('plotsLimits/BP3/ObservedLimit1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP3: SM tot ##
   
    x = dictBP3['ms']
    y = dictBP3['mx']
    z = dictBP3['x_H3_H1H2_SM1SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP3: $\sigma(pp \\to X \\to SH \\to b\\bar{b}\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 650))

    plt.savefig('plotsLimits/BP3/x_H3_H1H2_SM1SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z

    
    ## BP3: SM H1 -> bb, H2 -> gamgam (1) ##
   
    x = dictBP3['ms']
    y = dictBP3['mx']
    z = dictBP3['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP3: $\sigma(pp \\to X \\to S(b\\bar{b})H(\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 650))

    plt.savefig('plotsLimits/BP3/x_H3_H1_SM1_H2_SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP3: SM H1 -> bb, H2 -> gamgam (2) ##
   
    x = dictBP3['ms']
    y = dictBP3['mx']
    z = dictBP3['x_H3_H1_SM2_H2_SM1']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP3: $\sigma(pp \\to X \\to S(\gamma\gamma)H(b\\bar{b}))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 650))

    plt.savefig('plotsLimits/BP3/x_H3_H1_SM2_H2_SM1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP3: ObsLim/(1) ##
   
    x = dictBP3['ms']
    y = dictBP3['mx']
    z = dictBP3['ObservedLimit']/dictBP3['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP3: $\sigma_{obs}/\sigma(S(b\\bar{b})H(\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 650))

    plt.savefig('plotsLimits/BP3/ObsDividedH1SM1H2SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    #### BP5: ####

    # twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP5_check_prel_Mproc', 'compiled_AtlasBP5_check_prel_Mproc.tsv',
    #                   msKey='mHa_ub', mxKey='mHc_ub')   

    # twoDPlot.exclusionPlotter('compiled_AtlasBP5_check_prel_Mproc.tsv', 'plotsLimits/BP5', 0, 
    #                  xlims=(1, 124), ylims=(126, 500), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1_SM1_H2_SM2')

    dictBP5 = twoDPlot.pandasDynamicReader('compiled_AtlasBP5_check_prel_Mproc.tsv', ['ms', 'mx', 'ObservedLimit', 'x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'])
    twoDPlot.exclusionCheck(dictBP5['ObservedLimit'], dictBP5, ['x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'], 10**(-8))

    ## BP5: Observed Limits ##

    x = dictBP5['ms']
    y = dictBP5['mx']
    z = dictBP5['ObservedLimit']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP5: Exclusion Limits', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{obs}$', xlims=(1, 124), ylims=(126, 500))

    plt.savefig('plotsLimits/BP5/ObservedLimit1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP5: SM tot ##
   
    x = dictBP5['ms']
    y = dictBP5['mx']
    z = dictBP5['x_H3_H1H2_SM1SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP5: $\sigma(pp \\to X \\to SH \\to b\\bar{b}\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))

    plt.savefig('plotsLimits/BP5/x_H3_H1H2_SM1SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z

    
    ## BP5: SM H1 -> bb, H2 -> gamgam (1) ##
   
    x = dictBP5['ms']
    y = dictBP5['mx']
    z = dictBP5['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP5: $\sigma(pp \\to X \\to S(b\\bar{b})H(\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))

    plt.savefig('plotsLimits/BP5/x_H3_H1_SM1_H2_SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP5: SM H1 -> bb, H2 -> gamgam (2) ##
   
    x = dictBP5['ms']
    y = dictBP5['mx']
    z = dictBP5['x_H3_H1_SM2_H2_SM1']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP5: $\sigma(pp \\to X \\to S(\gamma\gamma)H(b\\bar{b}))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))

    plt.savefig('plotsLimits/BP5/x_H3_H1_SM2_H2_SM1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP5: ObsLim/(1) ##
   
    x = dictBP5['ms']
    y = dictBP5['mx']
    z = dictBP5['ObservedLimit']/dictBP5['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP5: $\sigma_{obs}/\sigma(S(b\\bar{b})H(\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))

    plt.savefig('plotsLimits/BP5/ObsDividedH1SM1H2SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    #### BP6: ####

    # twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP6_check_prel_Mproc', 'compiled_AtlasBP6_check_prel_Mproc.tsv',
    #                   msKey='mHb_ub', mxKey='mHc_ub')   

    # twoDPlot.exclusionPlotter('compiled_AtlasBP6_check_prel_Mproc.tsv', 'plotsLimits/BP6', 0, 
    #                  xlims=(126, 500), ylims=(255, 1000), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1_SM1_H2_SM2')
    
    dictBP6 = twoDPlot.pandasDynamicReader('compiled_AtlasBP6_check_prel_Mproc.tsv', ['ms', 'mx', 'ObservedLimit', 'x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'])

    twoDPlot.exclusionCheck(dictBP6['ObservedLimit'], dictBP6, ['x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'], 10**(-8))


    ## BP6: Observed Limits ##

    x = dictBP6['ms']
    y = dictBP6['mx']
    z = dictBP6['ObservedLimit']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP6: Exclusion Limits', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{obs}$', xlims=(126, 500), ylims=(255, 1000))

    plt.savefig('plotsLimits/BP6/ObservedLimit1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP6: SM tot ##
   
    x = dictBP6['ms']
    y = dictBP6['mx']
    z = dictBP6['x_H3_H1H2_SM1SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP6: $\sigma(pp \\to X \\to SH \\to b\\bar{b}\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 1000))

    plt.savefig('plotsLimits/BP6/x_H3_H1H2_SM1SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z

    
    ## BP6: SM H1 -> bb, H2 -> gamgam (1) ##
   
    x = dictBP6['ms']
    y = dictBP6['mx']
    z = dictBP6['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP6: $\sigma(pp \\to X \\to S(b\\bar{b})H(\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 1000))

    plt.savefig('plotsLimits/BP6/x_H3_H1_SM1_H2_SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP6: SM H1 -> bb, H2 -> gamgam (2) ##
   
    x = dictBP6['ms']
    y = dictBP6['mx']
    z = dictBP6['x_H3_H1_SM2_H2_SM1']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP6: $\sigma(pp \\to X \\to S(\gamma\gamma)H(b\\bar{b}))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 1000))

    plt.savefig('plotsLimits/BP6/x_H3_H1_SM2_H2_SM1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP6: ObsLim/(1) ##
   
    x = dictBP6['ms']
    y = dictBP6['mx']
    z = dictBP6['ObservedLimit']/dictBP6['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP6: $\sigma_{obs}/\sigma(S(b\\bar{b})H(\gamma\gamma))$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 1000))

    plt.savefig('plotsLimits/BP6/ObsDividedH1SM1H2SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


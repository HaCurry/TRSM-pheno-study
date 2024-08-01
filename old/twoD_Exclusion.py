#-*- coding: utf-8 -*-
import pandas

import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.interpolate
mpl.rcParams.update(mpl.rcParamsDefault)
import mplhep as hep

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

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19

    #### BP2: ####

    twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP2_check_prel_Mproc_constraint', 'compiled_AtlasBP2_check_prel_Mproc_constraint.tsv',
                      msKey='mHa_ub', mxKey='mHc_ub')   

    # twoDPlot.exclusionPlotter('compiled_AtlasBP2_check_prel_Mproc_constraint.tsv', 'plotsLimits/BP2', 0, 
    #                  xlims=(1, 124), ylims=(126, 500), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1_SM1_H2_SM2')

    dictBP2 = twoDPlot.pandasDynamicReader('compiled_AtlasBP2_check_prel_Mproc_constraint.tsv', ['ms', 'mx', 'ObservedLimit', 'x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'])
    twoDPlot.exclusionCheck(dictBP2['ObservedLimit'], dictBP2, ['x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'], 10**(-8))

    ## BP2: Observed Limits ##

    x = dictBP2['ms']
    y = dictBP2['mx']
    z = dictBP2['ObservedLimit']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP2: observed limits', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{obs}$', xlims=(1, 124), ylims=(126, 500))
    plt.tight_layout()

    plt.savefig('plots2D/BP2_BR_XSH/BP2_ATLAS/BP2_ObservedLimit.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP2: SM tot ##
   
    x = dictBP2['ms']
    y = dictBP2['mx']
    z = dictBP2['x_H3_H1H2_SM1SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP2: $\sigma(pp \\to X \\to SH \\to b\\bar{b}\gamma\gamma))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))
    plt.tight_layout()

    plt.savefig('plots2D/BP2_BR_XSH/BP2_ATLAS/BP2_x_H3_H1H2_SM1SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z

    
    ## BP2: SM H1 -> bb, H2 -> gamgam (1) ##
   
    x = dictBP2['ms']
    y = dictBP2['mx']
    z = dictBP2['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP2: $\sigma(pp \\to X \\to S(b\\bar{b})H(\gamma\gamma))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))
    plt.tight_layout()

    plt.savefig('plots2D/BP2_BR_XSH/BP2_ATLAS/BP2_x_H3_H1_SM1_H2_SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP2: SM H1 -> bb, H2 -> gamgam (2) ##
   
    x = dictBP2['ms']
    y = dictBP2['mx']
    z = dictBP2['x_H3_H1_SM2_H2_SM1']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D(r'BP2: $\sigma(pp \to X \to S(\gamma\gamma)H(b\bar{b}))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))
    plt.tight_layout()

    plt.savefig('plots2D/BP2_BR_XSH/BP2_ATLAS/BP2_x_H3_H1_SM2_H2_SM1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP2: ObsLim/(1) ##

    # plt.figure(figsize=(8.5, 5.2)) 
    # plt.figure(figsize=(6.4, 4.8)) # default figsize (6.4, 4.8)
   
    x = dictBP2['ms']
    y = dictBP2['mx']
    z = dictBP2['ObservedLimit']/dictBP2['x_H3_H1_SM1_H2_SM2']
    
    # twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.0f}')
    nanmarkz, nanmarkx, nanmarky = [], [], []
    for i in range(len(z)):
        if np.isnan(z[i]):
            nanmarkz.append(z[i])
            nanmarkx.append(x[i])
            nanmarky.append(y[i])
        else:
            plt.annotate('{:.0f}'.format(z[i]), (x[i], y[i]),
                         textcoords='offset points', xytext=(-3,-2), fontsize=9, rotation=45, 
                         path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground='w')])
    plt.scatter(nanmarkx, nanmarky, facecolors='None', edgecolors='grey', linestyle='dotted', label='Excluded by ScannerS')
    plt.legend()
    
    plt.scatter(x, y, c=z)

    twoDPlot.plotAuxTitleAndBounds2D(r'BP2: $\sigma(\mathrm{lim})/\sigma(gg \ \to \ h _{3} \ \to \ h _{1}(b\bar{b}) \ h _{2}(\gamma\gamma) )$', 
                                     r'$M_{1}$ [GeV]', r'$M_{3}$ [GeV]', 
                                     r'$\sigma(\mathrm{lim})/\sigma(gg \ \to \ h _{3} \ \to h _{1}(b\bar{b}) \ h _{2}(\gamma\gamma) )$', xlims=(1, 124), ylims=(126, 500))
    plt.tight_layout()

    plt.savefig('plots2D/BP2_BR_XSH/BP2_ATLAS/BP2_ObsDividedH1SM1H2SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    #### BP3: ####

    twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP3_check_prel_Mproc_constraint', 'compiled_AtlasBP3_check_prel_Mproc_constraint.tsv',
                      msKey='mHb_ub', mxKey='mHc_ub')   

    # twoDPlot.exclusionPlotter('compiled_AtlasBP3_check_prel_Mproc_constraint.tsv', 'plotsLimits/BP3', 0, 
    #                  xlims=(126, 500), ylims=(255, 650), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1_SM1_H2_SM2')
    
    dictBP3 = twoDPlot.pandasDynamicReader('compiled_AtlasBP3_check_prel_Mproc_constraint.tsv', ['ms', 'mx', 'ObservedLimit', 'x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'])

    twoDPlot.exclusionCheck(dictBP3['ObservedLimit'], dictBP3, ['x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'], 10**(-8))

    ## BP3: Observed Limits ##

    x = dictBP3['ms']
    y = dictBP3['mx']
    z = dictBP3['ObservedLimit']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP3: observed limits', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{obs}$ at ATLAS limit points', xlims=(126, 500), ylims=(255, 650))
    plt.tight_layout()

    plt.savefig('plots2D/BP3_BR_XSH/BP3_ATLAS/BP3_ObservedLimit.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP3: SM tot ##
   
    x = dictBP3['ms']
    y = dictBP3['mx']
    z = dictBP3['x_H3_H1H2_SM1SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP3: $\sigma(pp \\to X \\to SH \\to b\\bar{b}\gamma\gamma))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 650))
    plt.tight_layout()

    plt.savefig('plots2D/BP3_BR_XSH/BP3_ATLAS/BP3_x_H3_H1H2_SM1SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z

    
    ## BP3: SM H1 -> bb, H2 -> gamgam (1) ##
   
    x = dictBP3['ms']
    y = dictBP3['mx']
    z = dictBP3['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP3: $\sigma(pp \\to X \\to S(b\\bar{b})H(\gamma\gamma))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 650))
    plt.tight_layout()

    plt.savefig('plots2D/BP3_BR_XSH/BP3_ATLAS/BP3_x_H3_H1_SM1_H2_SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP3: SM H1 -> bb, H2 -> gamgam (2) ##
   
    x = dictBP3['ms']
    y = dictBP3['mx']
    z = dictBP3['x_H3_H1_SM2_H2_SM1']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP3: $\sigma(pp \\to X \\to S(\gamma\gamma)H(b\\bar{b}))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 650))
    plt.tight_layout()

    plt.savefig('plots2D/BP3_BR_XSH/BP3_ATLAS/BP3_x_H3_H1_SM2_H2_SM1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP3: ObsLim/(1) ##

    # plt.figure(figsize=(8.5, 5.2)) 
    # plt.figure(figsize=(6.4, 4.8)) # default figsize (6.4, 4.8)
   
    x = dictBP3['ms']
    y = dictBP3['mx']
    z = dictBP3['ObservedLimit']/dictBP3['x_H3_H1_SM1_H2_SM2']
    

    # twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.0f}', rot=45, xytxt=(-3,-2), fontsize=9)
    nanmarkz, nanmarkx, nanmarky = [], [], []
    for i in range(len(z)):
        if np.isnan(z[i]):
            nanmarkz.append(z[i])
            nanmarkx.append(x[i])
            nanmarky.append(y[i])
        else:
            plt.annotate('{:.0f}'.format(z[i]), (x[i], y[i]),
                         textcoords='offset points', xytext=(-3,-2), fontsize=9, rotation=45, 
                         path_effects=[mpl.patheffects.withStroke(linewidth=1.5, foreground='w')])
    plt.scatter(nanmarkx, nanmarky, facecolors='None', edgecolors='grey', linestyle='dotted', label='Excluded by ScannerS')
    plt.legend()

    plt.scatter(x, y, c=z)

    twoDPlot.plotAuxTitleAndBounds2D(r'BP3: $\left. \sigma(\mathrm{lim}) \right/ \sigma(gg \ \to \  h _{3} \ \to \ h _{1}(b\bar{b}) \ h _{2}(\gamma\gamma) )$', r'$M_{2}$ [GeV]', r'$M_{3}$ [GeV]', r'$\left. \sigma(\mathrm{lim}) \right/ \sigma(gg \ \to \ h _{3} \ \to \ h _{1}(\gamma\gamma) \ h _{2}(b\bar{b}) )$', xlims=(126, 500), ylims=(255, 650))
    plt.tight_layout()

    plt.savefig('plots2D/BP3_BR_XSH/BP3_ATLAS/BP3_ObsDividedH1SM1H2SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    #### BP5: ####

    twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP5_check_prel_Mproc_constraint', 'compiled_AtlasBP5_check_prel_Mproc_constraint.tsv',
                      msKey='mHa_ub', mxKey='mHc_ub')   

    # twoDPlot.exclusionPlotter('compiled_AtlasBP5_check_prel_Mproc_constraint.tsv', 'plotsLimits/BP5', 0, 
    #                  xlims=(1, 124), ylims=(126, 500), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1_SM1_H2_SM2')

    dictBP5 = twoDPlot.pandasDynamicReader('compiled_AtlasBP5_check_prel_Mproc_constraint.tsv', ['ms', 'mx', 'ObservedLimit', 'x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'])
    twoDPlot.exclusionCheck(dictBP5['ObservedLimit'], dictBP5, ['x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'], 10**(-8))

    ## BP5: Observed Limits ##

    x = dictBP5['ms']
    y = dictBP5['mx']
    z = dictBP5['ObservedLimit']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP5: observed limits', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{obs}$', xlims=(1, 124), ylims=(126, 500))
    plt.tight_layout()

    plt.savefig('plots2D/BP5_BR_XSH/BP5_ATLAS/BP5_ObservedLimit.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP5: SM tot ##
   
    x = dictBP5['ms']
    y = dictBP5['mx']
    z = dictBP5['x_H3_H1H2_SM1SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP5: $\sigma(pp \\to X \\to SH \\to b\\bar{b}\gamma\gamma))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))
    plt.tight_layout()

    plt.savefig('plots2D/BP5_BR_XSH/BP5_ATLAS/BP5_x_H3_H1H2_SM1SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z

    
    ## BP5: SM H1 -> bb, H2 -> gamgam (1) ##
   
    x = dictBP5['ms']
    y = dictBP5['mx']
    z = dictBP5['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP5: $\sigma(pp \\to X \\to S(b\\bar{b})H(\gamma\gamma))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))
    plt.tight_layout()

    plt.savefig('plots2D/BP5_BR_XSH/BP5_ATLAS/BP5_x_H3_H1_SM1_H2_SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP5: SM H1 -> bb, H2 -> gamgam (2) ##
   
    x = dictBP5['ms']
    y = dictBP5['mx']
    z = dictBP5['x_H3_H1_SM2_H2_SM1']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP5: $\sigma(pp \\to X \\to S(\gamma\gamma)H(b\\bar{b}))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(1, 124), ylims=(126, 500))
    plt.tight_layout()

    plt.savefig('plots2D/BP5_BR_XSH/BP5_ATLAS/BP5_x_H3_H1_SM2_H2_SM1.pdf')
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
    plt.tight_layout()

    plt.savefig('plots2D/BP5_BR_XSH/BP5_ATLAS/BP5_ObsDividedH1SM1H2SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    #### BP6: ####

    twoDPlot.exclusionCompiler('/**/settingsCalc_Nofree*.json', 'calc_AtlasBP6_check_prel_Mproc_constraint', 'compiled_AtlasBP6_check_prel_Mproc_constraint.tsv',
                      msKey='mHb_ub', mxKey='mHc_ub')   

    # twoDPlot.exclusionPlotter('compiled_AtlasBP6_check_prel_Mproc_constraint.tsv', 'plotsLimits/BP6', 0, 
    #                  xlims=(126, 500), ylims=(255, 1000), keyX='ms', keyY='mx', keyA='ObservedLimit', keyB='x_H3_H1_SM1_H2_SM2')
    
    dictBP6 = twoDPlot.pandasDynamicReader('compiled_AtlasBP6_check_prel_Mproc_constraint.tsv', ['ms', 'mx', 'ObservedLimit', 'x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'])

    twoDPlot.exclusionCheck(dictBP6['ObservedLimit'], dictBP6, ['x_H3_H1H2_SM1SM2', 'x_H3_H1_SM1_H2_SM2', 'x_H3_H1_SM2_H2_SM1'], 10**(-8))


    ## BP6: Observed Limits ##

    x = dictBP6['ms']
    y = dictBP6['mx']
    z = dictBP6['ObservedLimit']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP6: observed limits', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{obs}$', xlims=(126, 500), ylims=(255, 1000))
    plt.tight_layout()

    plt.savefig('plots2D/BP6_BR_XSH/BP6_ATLAS/BP6_ObservedLimit1.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP6: SM tot ##
   
    x = dictBP6['ms']
    y = dictBP6['mx']
    z = dictBP6['x_H3_H1H2_SM1SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP6: $\sigma(pp \\to X \\to SH \\to b\\bar{b}\gamma\gamma))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 1000))
    plt.tight_layout()

    plt.savefig('plots2D/BP6_BR_XSH/BP6_ATLAS/BP6_x_H3_H1H2_SM1SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z

    
    ## BP6: SM H1 -> bb, H2 -> gamgam (1) ##
   
    x = dictBP6['ms']
    y = dictBP6['mx']
    z = dictBP6['x_H3_H1_SM1_H2_SM2']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP6: $\sigma(pp \\to X \\to S(b\\bar{b})H(\gamma\gamma)) at ATLAS limit points$', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 1000))
    plt.tight_layout()

    plt.savefig('plots2D/BP6_BR_XSH/BP6_ATLAS/BP6_x_H3_H1_SM1_H2_SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


    ## BP6: SM H1 -> bb, H2 -> gamgam (2) ##
   
    x = dictBP6['ms']
    y = dictBP6['mx']
    z = dictBP6['x_H3_H1_SM2_H2_SM1']
    
    plt.scatter(x, y, c=z)
    twoDPlot.plotAuxAnnotator2D(x, y, z, '{:.1e}')
    twoDPlot.plotAuxTitleAndBounds2D('BP6: $\sigma(pp \\to X \\to S(\gamma\gamma)H(b\\bar{b}))$ at ATLAS limit points', '$M_{S}$ [GeV]', '$M_{X}$', '$\sigma_{excl}$', xlims=(126, 500), ylims=(255, 1000))
    plt.tight_layout()

    plt.savefig('plots2D/BP6_BR_XSH/BP6_ATLAS/BP6_x_H3_H1_SM2_H2_SM1.pdf')
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
    plt.tight_layout()

    plt.savefig('plots2D/BP6_BR_XSH/BP6_ATLAS/BP6_ObsDividedH1SM1H2SM2.pdf')
    # plt.show()
    plt.close()

    del x, y, z


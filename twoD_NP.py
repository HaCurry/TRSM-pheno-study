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


# def plotAuxTitleAndBounds2D(title, xtitle, ytitle, ztitle, **kwargs):

#     if ('xlims' in kwargs) and ('ylims' in kwargs):
#         plt.xlim(kwargs['xlims'])        
#         plt.ylim(kwargs['ylims'])

#     elif ('xlims' in kwargs) or ('ylims' in kwargs):
#         raise Exception('Either specify both xlims and ylims or none')
    
#     else:
#         pass
            
#     plt.title(title)
#     plt.xlabel(xtitle)
#     plt.ylabel(ytitle)
#     plt.colorbar(label=ztitle)


# def plotAuxVar2D(x, y, n, nInterp=500):
#     x = np.asarray(x)
#     y = np.asarray(y)
#     z = np.asarray(n)

#     # Set up a regular grid of interpolation points
#     xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
#     xi, yi = np.meshgrid(xi, yi)

#     return x, y, z, xi, yi


# def plotAuxRegion2D(label1, label2, label3, xyText1, xyText2, xyText3, plot1, plot2, plot3):
    
#     plt.plot(plot1[0], plot1[1], ls = 'dashed')
#     plt.text(xyText1[0], xyText1[1], label1, size = 9, bbox =dict(facecolor='C0', alpha=0.5, pad=0.7))

#     plt.plot(plot2[0], plot2[1], ls = 'dashed')
#     plt.text(xyText2[0], xyText2[1], label2, size = 9, bbox =dict(facecolor='C1', alpha=0.5, pad=0.7))#, rotation=18)

#     plt.plot(plot3[0], plot3[1], ls = 'dashed')
#     plt.text(xyText3[0], xyText3[1], label3, size = 9, bbox =dict(facecolor='C2', alpha=0.5, pad=0.7))#, rotation=32)


# def pandasReader(path, axis1Key, axis2Key, axis3Key, zKey):

#     BP2_df = pandas.read_table(path, index_col=0) 
#     axis1 = np.array([i for i in BP2_df[axis1Key]])
#     axis2 = np.array([i for i in BP2_df[axis2Key]])
#     axis3 = np.array([i for i in BP2_df[axis3Key]])
#     z = np.array([i for i in BP2_df[zKey]])

#     return axis1, axis2, axis3, z 
    
    

if __name__ == '__main__':

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19

    ############
    #### BR ####
    ############

    #### BP2 ####

    # twoDPlot.checkCreator2d(100, 'plots2D/BP2_BR_XSH/config_BP2_BR_XSH.tsv', (126, 500), (1, 124), 'mH3', 'mH1', 'mH2',
    #              ths=1.352, thx=1.175, tsx=-0.407, vs=120, vx=890)

    # twoDPlot.runTRSM('../../../TRSMBroken', 'plots2D/BP2_BR_XSH', 'config_BP2_BR_XSH.tsv', 'output_BP2_BR_XSH.tsv', 'check', capture_output=False)
       
    # twoDPlot.calculateSort2D('plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 'plots2D/BP2_BR_XSH', 'calc_BP2.tsv', 'bb', 'gamgam')

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_b_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/calc_BP2.tsv', 'mH1', 'mH2', 'mH3', 'b_H3_H1H2')
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_b_H3_H1H2)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, vmin=0.1, vmax=0.55, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\mathrm{BR}(h _{3}\to h _{1}h _{2})$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r"$\mathrm{BR}(h _{3} \to h _{1}h _{2})$", xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = 2 M_{1}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))

    plt.tight_layout()
    plt.savefig('plots2D/BP2_BR_XSH/BP2_BR_XSH_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    #### BP3 ####

    # twoDPlot.checkCreator2d(100, 'plots2D/BP3_BR_XSH/config_BP3_BR_XSH.tsv', (255, 650), (126, 500), 'mH3', 'mH2', 'mH1',
    #              ths=-0.129, thx=0.226, tsx=-0.899, vs=140, vx=100)

    # twoDPlot.runTRSM('../../../TRSMBroken', 'plots2D/BP3_BR_XSH', 'config_BP3_BR_XSH.tsv', 'output_BP3_BR_XSH.tsv', 'check', capture_output=False)

    # twoDPlot.calculateSort2D('plots2D/BP3_BR_XSH/output_BP3_BR_XSH.tsv', 'plots2D/BP3_BR_XSH', 'calc_BP3.tsv', 'bb', 'gamgam')

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_b_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/calc_BP3.tsv', 'mH1', 'mH2', 'mH3', 'b_H3_H1H2')
      
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_b_H3_H1H2)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    plt.imshow(zi, vmin=0, vmax=0.6, origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\mathrm{BR}(h _{3}\to h _{1}h _{2})$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r"$\mathrm{BR}(h _{3} \to h _{1}h _{2})$", xlims=(126, 500), ylims=(255, 650))

    twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = M_{2}$', (298, 575), (405, 514), (440, 424),
                    ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
        
    plt.tight_layout()
    plt.savefig('plots2D/BP3_BR_XSH/BP3_BR_XSH_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    #### BP5 ####
    
    # twoDPlot.checkCreator2d(100, 'plots2D/BP5_BR_XSH/config_BP5_BR_XSH.tsv', (126, 500), (1, 124), 'mH3', 'mH1', 'mH2',
    #                ths=-1.498, thx=0.251, tsx=0.271, vs=50, vx=720)

    # twoDPlot.runTRSM('../../../TRSMBroken', 'plots2D/BP5_BR_XSH/', 'config_BP5_BR_XSH.tsv', 'output_BP5_BR_XSH.tsv', 'check', capture_output=False)

    # twoDPlot.calculateSort2D('plots2D/BP5_BR_XSH/output_BP5_BR_XSH.tsv', 'plots2D/BP5_BR_XSH', 'calc_BP5.tsv', 'bb', 'gamgam')

    BP5_mH1, BP5_mH2, BP5_mH3, BP5_b_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'b_H3_H1H2')
      
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP5_mH1, BP5_mH3, BP5_b_H3_H1H2)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=0.80, vmax=1.0, origin='lower',
    #           extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=0, vmax=1, origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP5: $BR(X\to SH)$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))

    plt.savefig('plots2D/BP5_BR_XSH/BP5_BR_XSH_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    #### BP6 ####

    # twoDPlot.checkCreator2d(50, 'plots2D/BP6_BR_XSH/config_BP6_BR_XSH.tsv', (255, 850), (126, 400), 'mH3', 'mH2', 'mH1',
    #                ths=0.207, thx=0.146, tsx=0.782, vs=220, vx=150)

    # twoDPlot.runTRSM('../../../TRSMBroken', 'plots2D/BP6_BR_XSH/', 'config_BP6_BR_XSH.tsv', 'output_BP6_BR_XSH.tsv', 'check', capture_output=False)

    # twoDPlot.calculateSort2D('plots2D/BP6_BR_XSH/output_BP6_BR_XSH.tsv', 'plots2D/BP6_BR_XSH', 'calc_BP6.tsv', 'bb', 'gamgam')

    BP6_mH1, BP6_mH2, BP6_mH3, BP6_b_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH/calc_BP6.tsv', 'mH1', 'mH2', 'mH3', 'b_H3_H1H2')

    # twoDPlot.calculateSort2D('plots2D/BP6_BR_XSH_try2/output_BP6_BR_XSH.tsv', 'plots2D/BP6_BR_XSH_try2', 'calc_BP6', 'bb', 'gamgam')

    # BP6_mH1, BP6_mH2, BP6_mH3, BP6_b_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH_try2/calc_BP6', 'mH1', 'mH2', 'mH3', 'b_H3_H1H2')
      
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP6_mH2, BP6_mH3, BP6_b_H3_H1H2)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, vmin=0.50, vmax=0.85, origin='lower',
               # extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP6: $BR(X\to SH)$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(126, 500), ylims=(255, 1000))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{S}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = M_{S}$', (298, 575), (337, 445), (353, 336),
                    ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
        
    plt.savefig('plots2D/BP6_BR_XSH/BP6_BR_XSH_fig.pdf')
    # plt.savefig('plots2D/BP6_BR_XSH_try2/BP6_BR_XSH_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi

    ########################################################################################################################################################
    ########################################################################################################################################################

    ############
    #### XS ####
    ############

    #### BP2 ####

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_x_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/calc_BP2.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1H2')
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_x_H3_H1H2)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower', vmin = 10**(-2), vmax = 7*10**(-1),#norm=mpl.colors.LogNorm(vmin = 10**(-2), vmax = 7*10**(-1)),
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\sigma(gg\to h _{3}) \times \mathrm{BR}_{h _{3}\to h _{1}h _{2}}$", r"$M_{2}$", r"$M_{3}$", r'$\sigma _{gg\to h _{3}\times \mathrm{BR}_{h _{3}\to h _{1}h _{2}}$ [pb]', xlims=(1, 124), ylims=(126, 500))
    twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\sigma(gg \ \to \ h _{3} \ \to \ h _{1}h _{2})$", r"$M_{2}$", r"$M_{3}$", r'$\sigma( gg \ \to \ h _{3} \ \to \ h _{1}h _{2})$ [pb]', xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = 2 M_{1}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    
    plt.tight_layout()
    plt.savefig('plots2D/BP2_BR_XSH/BP2_XS_XSH_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    #### BP3 ####

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_x_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/calc_BP3.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1H2')
      
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_x_H3_H1H2)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    plt.imshow(zi, origin='lower', vmin = 6*10**(-3), vmax = 4*10**(-1),#norm=mpl.colors.LogNorm(vmin = 6*10**(-3), vmax = 4*10**(-1)),
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\sigma _{gg\to h _{3}\times \mathrm{BR}_{h _{3}\to h _{1}h _{2}}$", r"$M_{1}$", r"$M_{3}$", r'$\sigma _{gg\to h _{3} \times \mathrm{BR}_{h _{3}\to h _{1}h _{2}}$ [pb]', xlims=(126, 500), ylims=(255, 650))
    twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\sigma (gg \ \to \ h _{3} \ \to \ h _{1}h _{2})$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r'$\sigma(gg \ \to \ h _{3} \ \to h _{1}h _{2})$ [pb]', xlims=(126, 500), ylims=(255, 650))

    twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = M_{2}$', (298, 575), (405, 514), (440, 424),
                    ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
        
    plt.tight_layout()
    plt.savefig('plots2D/BP3_BR_XSH/BP3_XS_XSH_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    #### BP5 ####

    BP5_mH1, BP5_mH2, BP5_mH3, BP5_x_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1H2')
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP5_mH1, BP5_mH3, BP5_x_H3_H1H2)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower', norm=mpl.colors.LogNorm(),
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP5: $\sigma(X\to SH)$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    
    plt.savefig('plots2D/BP5_BR_XSH/BP5_XS_XSH_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    #### BP6 ####

    BP6_mH1, BP6_mH2, BP6_mH3, BP6_x_H3_H1H2 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH/calc_BP6.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1H2')
      
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP6_mH2, BP6_mH3, BP6_x_H3_H1H2)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    plt.imshow(zi, origin='lower', norm=mpl.colors.LogNorm(),
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP6: $\sigma(X\to SH)$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(126, 500), ylims=(255, 1000))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{S}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = M_{S}$', (298, 575), (337, 445), (353, 336),
                    ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
        
    plt.savefig('plots2D/BP6_BR_XSH/BP6_XS_XSH_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    #############
    #### NWA ####
    #############

    # plt.rcParams['axes.labelsize'] = 19
    # plt.rcParams['axes.titlesize'] = 19
    # mpl.rcParams["text.usetex"] = True
    # # mpl.rcParams['mathtext.fontset'] = 'cm'
    # mpl.rcParams['font.family'] = 'cm'
    # mpl.rcParams['mathtext.fontset'] = 'cm'
    # mpl.rcParams['font.family'] = 'STIXGeneral'

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19

    #### BP2: ####            

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 'mH1', 'mH2', 'mH3', 'w_H3')

    BP2_NWA_H3 = BP2_w_H3/BP2_mH3

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_NWA_H3)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\Gamma_{h_{3}}/M_{3}$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r'$\Gamma_{h_{3}}/M_{3}$', xlims=(1, 124), ylims=(126, 500), cbarfmt='{x:.3f}')
    # plt.title(r"BP2: $\Gamma_{h_{3}}/M_{3}$")
    # plt.colorbar(label=r'$\Gamma_{h_{3}}/M_{3}$', format='{x:.3f}')
    
    plt.tight_layout()
    plt.savefig('plots2D/BP2_BR_XSH/BP2_NWA.pdf')
    plt.show()

    # increase fontsize so that subsubscripts are visible, enable plt.tight_layout() and maybe flush the colorbar agains the figure border


    #### BP3: ####            

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/output_BP3_BR_XSH.tsv', 'mH1', 'mH2', 'mH3', 'w_H3')

    BP3_NWA_H3 = BP3_w_H3/BP3_mH3

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_NWA_H3)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\Gamma_{h_{3}}/M_{3}$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r'$\Gamma_{h_{3}}/M_{3}$', xlims=(126, 500), ylims=(255, 650), cbarfmt='{x:.3f}')

    plt.tight_layout()
    plt.savefig('plots2D/BP3_BR_XSH/BP3_NWA.pdf')
    plt.show()

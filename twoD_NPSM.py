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
# print(ampl.__file__)

if __name__ == '__main__':
    # ampl.use_atlas_style()
    # hep.style.use('ATLAS')
    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19
    # plt.style.use('print')
    # plt.rcParams['axes.labelsize'] = 19
    # plt.rcParams['axes.titlesize'] = 19
    # mpl.rcParams["text.usetex"] = True
    # # mpl.rcParams['mathtext.fontset'] = 'cm'
    # mpl.rcParams['font.family'] = 'cm'

    norm = (31.02 * 10**(-3)) * 0.0026

    ###############
    #### XS SM ####
    ###############

    #### BP2: ####

    ## BP2: SM TOT ##

    twoDPlot.calculateSort2D('plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 'plots2D/BP2_BR_XSH', 'calc_BP2.tsv', 'bb', 'gamgam')

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_x_H3_SM1SM2 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/calc_BP2.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1H2_SM1SM2')
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_x_H3_SM1SM2/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\sigma(X\to SH \to bb\gamma\gamma)$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))

    plt.text(60, 225, "test", size=20, color='black', path_effects=[mpl.patheffects.withStroke(linewidth=4, foreground='white')])    

    plt.savefig('plots2D/BP2_BR_XSH/BP2_XS_XSH_bbgamgam_tot_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi

    ## BP2: SM H1 -> bb, H2 -> gamgam (1) ##

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/calc_BP2.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_x_H3_H1_SM1_H2_SM2/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\left.\sigma(gg \ \to \ h_{3})\times\mathrm{BR}(h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma)) \right/ \sigma(\mathrm{SM})$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r"$\left.\sigma(gg \ \to \ h_{3})\times\mathrm{BR}(h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma))\right/ \sigma(\mathrm{SM})$", xlims=(1, 124), ylims=(126, 500))
    twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\left.\sigma(gg \ \to \ h_{3} \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma)) \right/ \sigma(\mathrm{SM})$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r"$\left.\sigma(gg \ \to \ h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma))\right/ \sigma(\mathrm{SM})$", xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = 2 M_{1}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))

    plt.tight_layout()
    plt.savefig('plots2D/BP2_BR_XSH/BP2_XS_XSH_bbgamgam_1_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi

    ## BP2: SM H1 -> gamgam, H2 -> bb (2) ##

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/calc_BP2.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_x_H3_H1_SM2_H2_SM1/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\sigma(gg \ \to \ h_{3})\times\mathrm{BR}(h_{3} \ \to \ h_{1}(\gamma\gamma) \ h_{2}(b\bar{b}))$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r"$\sigma(gg \ \to \ h_{3})\times\mathrm{BR}(h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma))$", xlims=(1, 124), ylims=(126, 500))
    twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\left. \sigma(gg \ \to \ h_{3} \ \to \ h_{1}(\gamma\gamma) \ h_{2}(b\bar{b}))\right/ \sigma(\mathrm{SM})$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r"$\left. \sigma(gg \ \to \ h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma))\right/ \sigma(\mathrm{SM})$", xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = 2 M_{1}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))

    plt.tight_layout()
    plt.savefig('plots2D/BP2_BR_XSH/BP2_XS_XSH_bbgamgam_2_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    ## BP2: SM Ratio (1)/(2) ##

    
    BP2_mH1, BP2_mH2, BP2_mH3, BP2_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/calc_BP2.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    BP2_mH1_2, BP2_mH2_2, BP2_mH3_2, BP2_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/calc_BP2.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')

    print(BP2_mH1 == BP2_mH1_2)
    print(BP2_mH2 == BP2_mH2_2)
    print(BP2_mH3 == BP2_mH3_2)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_x_H3_H1_SM1_H2_SM2/BP2_x_H3_H1_SM2_H2_SM1)
    
        
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # contf = plt.imshow(zi, origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # levels=[0,1,15,30,45,60,75,90,105,120]
    levels = [0, 1, 30, 60, 90, 120]
    # contf = plt.contourf(xi, yi, zi, levels=levels)#, cmap=cmap)
    plt.contour(xi, yi, zi, levels=[1], colors='red', linewidths=0.5, extent=(min(BP2_mH1), max(BP2_mH1), min(BP2_mH3), max(BP2_mH3)))
    
    ax = plt.gca()
    CS = ax.contour(xi, yi, zi, levels=[20, 60, 100], linewidths=0.5, colors='black', extent=(min(BP2_mH1), max(BP2_mH1), min(BP2_mH3), max(BP2_mH3)))

    # from: https://matplotlib.org/2.0.2/examples/pylab_examples/patheffect_demo.html
    # and chatGPT
    from matplotlib import patheffects as pe
    clbls = ax.clabel(CS, CS.levels, use_clabeltext=True)
    plt.setp(clbls, path_effects=[pe.withStroke(linewidth=3, foreground="w")])

    ################################ zoom box ################################
    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
    from mpl_toolkits.axes_grid1.inset_locator import mark_inset   
    axins = zoomed_inset_axes(ax, 3, loc = 'upper left', borderpad=1.2) # zoom = 6
    # axins.contourf(xi, yi, zi, levels=levels)#, cmap=cmap)
    axins.imshow(zi, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    axins.contour(xi, yi, zi, levels=[1], linewidths=0.5, colors='red', extent=(min(BP2_mH1), max(BP2_mH1), min(BP2_mH3), max(BP2_mH3)))

    # sub region of the original image
    x1, x2, y1, y2 = 1, 12, 130, 160
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.yaxis.tick_right()

    # draw a bbox of the region of the inset axes in the parent axes and
    # connecting lines between the bbox and the inset axes area
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
    ##########################################################################

    ax.set_xlim(1, 124)
    ax.set_ylim(126, 500)
    # twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\left.\sigma(h_{1}(b\bar{b}) \  h_{2}(\gamma\gamma)) \right/ \sigma(h_{1}(\gamma\gamma) \ h_{2}(b\bar{b}))$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", 
    #                                  r'$\sigma(\left. h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma)) \right/ \sigma( h_{1}(\gamma\gamma) \  h_{2}(b\bar{b}))$', xlims=(1, 124), ylims=(126, 500),
    #                                  cbarvisible=False)

    # twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = 2 M_{1}$', (3, 235), (26, 134), (75, 134),
    #                 ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    fig = plt.gcf()
    fig.colorbar(contf, ax=ax, label =r'$\left.\sigma(h_{1}(b\bar{b}) \  h_{2}(\gamma\gamma)) \right/ \sigma(h_{1}(\gamma\gamma) \ h_{2}(b\bar{b}))$' )

    plt.tight_layout()
    plt.savefig('plots2D/BP2_BR_XSH/BP2_XS_XSH_bbgamgam_ratio_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    # plt.colorbar()
    # plt.show()
    plt.close()


    #### BP3: ####

    ## BP3: SM H1 -> bb, H2 -> gamgam (1) ##

    twoDPlot.calculateSort2D('plots2D/BP3_BR_XSH/output_BP3_BR_XSH.tsv', 'plots2D/BP3_BR_XSH', 'calc_BP3.tsv', 'bb', 'gamgam')

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/calc_BP3.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
      
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM1_H2_SM2/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    plt.imshow(zi, origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\sigma(gg \ \to \ h_{3}) \times \mathrm{BR}(h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma))$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r'$\sigma_(gg \ \to \ h_{3}) \times \mathrm{BR}(h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma))$', xlims=(126, 500), ylims=(255, 650))
    twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\left. \sigma(gg \ \to \ h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma))\right/ \sigma(\mathrm{SM})$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r'$\left.\sigma_(gg \ \to \ h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma))\right/ \sigma(\mathrm{SM})$', xlims=(126, 500), ylims=(255, 650))

    twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = M_{2}$', (298, 575), (405, 514), (440, 424),
                    ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))

    plt.tight_layout()
    plt.savefig('plots2D/BP3_BR_XSH/BP3_XS_XSH_bbgamgam_1_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    ## BP3: SM H1 -> gamgam, H2 -> bb (2) ##

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/calc_BP3.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')
      
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM2_H2_SM1/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    plt.imshow(zi, origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\sigma(gg \ \to \ h_{3}) \times \mathrm{BR}(h_{3} \ \to \ h_{1}(\gamma\gamma) \ h_{2}(b\bar{b}))$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r'$\sigma(gg \ \to \ h_{3}) \times \mathrm{BR}(h_{3} \ \to \ h_{1}(\gamma\gamma) \ h_{2}(b\bar{b}))$', xlims=(126, 500), ylims=(255, 650))
    twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\left. \sigma(gg \ \to \ h_{3} \ \to \ h_{1}(\gamma\gamma)) \ h_{2}(b\bar{b}))\right/ \sigma(\mathrm{SM})$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r'$\left.\sigma_(gg \ \to \ h_{3} \ \to \ h_{1}(b\bar{b}) \ h_{2}(\gamma\gamma))\right/ \sigma(\mathrm{SM})$', xlims=(126, 500), ylims=(255, 650))

    twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = M_{2}$', (298, 575), (405, 514), (440, 424),
                    ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))

    plt.tight_layout()
    plt.savefig('plots2D/BP3_BR_XSH/BP3_XS_XSH_bbgamgam_2_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    #### BP3: ####

    ## BP3: SM (1)/(2) ##

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/calc_BP3.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    BP3_mH1_2, BP3_mH2_2, BP3_mH3_2, BP3_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/calc_BP3.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')

    print(BP3_mH1 == BP3_mH1_2)
    print(BP3_mH2 == BP3_mH2_2)
    print(BP3_mH3 == BP3_mH3_2)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_x_H3_H1_SM1_H2_SM2/BP3_x_H3_H1_SM2_H2_SM1) 
       
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # plt.contour(xi, yi, zi, levels=[1.05], colors='red', linewidths=0.5, extent=(x.min(), x.max(), y.min(), y.max()))

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\sigma(gg \ \to \ h_{3} \ \to \ h_{1}(b\bar{b}) \  h_{2}(\gamma\gamma)) / \sigma(gg \ \to \ h_{3} \ \to \ h_{1}(\gamma\gamma) \ h_{2}(b\bar{b}))$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r'$\sigma_(gg \ \to \ h_{3} \ \to \ h_{1}(b\bar{b}) \  h_{2}(\gamma\gamma)) / \sigma_{gg \ \to \ h_{3} \ \to \ h_{1}(\gamma\gamma) \ h_{2}(b\bar{b})}$', xlims=(126, 500), ylims=(255, 650))
    # twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\left.\sigma(h_{1}(b\bar{b}) \  h_{2}(\gamma\gamma)) \right/ \sigma(h_{1}(\gamma\gamma) \ h_{2}(b\bar{b}))$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r'$\left.\sigma(h_{1}(b\bar{b}) \  h_{2}(\gamma\gamma)) \right/ \sigma(h_{1}(\gamma\gamma) \ h_{2}(b\bar{b}))$', xlims=(126, 500), ylims=(255, 650))

    # twoDPlot.plotAuxRegion2D(r'$M_{3} = 2 M_{2}$', r'$M_{3} = M_{1} + M_{2}$', r'$M_{3} = M_{2}$', (298, 575), (405, 514), (440, 424),
    #                 ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))

    plt.tight_layout()
    plt.savefig('plots2D/BP3_BR_XSH/BP3_XS_XSH_bbgamgam_ratio_fig.pdf')
    plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    # #### BP5 ####

    # ## SM TOT ##

    # BP5_mH1, BP5_mH2, BP5_mH3, BP5_x_H3_SM1SM2 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1H2_SM1SM2')
    
    # x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP5_mH1, BP5_mH3, BP5_x_H3_SM1SM2/norm)

    # zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP5: $\sigma(X\to SH \to bb\gamma\gamma)$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    # twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
    #                 ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    
    # plt.savefig('plots2D/BP5_BR_XSH/BP5_XS_XSH_bbgamgam_tot_fig.pdf')
    # plt.show()
    # plt.close()

    # plt.scatter(x, y, c=z, cmap='viridis')
    # plt.colorbar()
    # plt.show()
    # plt.close()

    # del x, y, z, xi, yi

    # ## SM H1 -> bb, H2 -> gamgam (1) ##

    # BP5_mH1, BP5_mH2, BP5_mH3, BP5_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    
    # x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP5_mH1, BP5_mH3, BP5_x_H3_H1_SM1_H2_SM2/norm)

    # zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP5: $\sigma(X\to S(bb) H(\gamma\gamma))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    # twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
    #                 ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    
    # plt.savefig('plots2D/BP5_BR_XSH/BP5_XS_XSH_bbgamgam_1_fig.pdf')
    # plt.show()
    # plt.close()

    # plt.scatter(x, y, c=z, cmap='viridis')
    # plt.colorbar()
    # plt.show()
    # plt.close()

    # del x, y, z, xi, yi

    # ## SM H1 -> gamgam, H2 -> bb (2) ##

    # BP5_mH1, BP5_mH2, BP5_mH3, BP5_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')
    
    # x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP5_mH1, BP5_mH3, BP5_x_H3_H1_SM2_H2_SM1/norm)

    # zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP5: $\sigma(X\to S(\gamma\gamma)H(bb) )$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    # twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
    #                 ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    
    # plt.savefig('plots2D/BP5_BR_XSH/BP5_XS_XSH_bbgamgam_2_fig.pdf')
    # plt.show()
    # plt.close()

    # plt.scatter(x, y, c=z, cmap='viridis')
    # plt.colorbar()
    # plt.show()
    # plt.close()

    # del x, y, z, xi, yi


    # ## SM Ratio (1)/(2) ##

    
    # BP5_mH1, BP5_mH2, BP5_mH3, BP5_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    # BP5_mH1_2, BP5_mH2_2, BP5_mH3_2, BP5_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')

    # print(BP5_mH1 == BP5_mH1_2)
    # print(BP5_mH2 == BP5_mH2_2)
    # print(BP5_mH3 == BP5_mH3_2)

    # x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP5_mH1, BP5_mH3, BP5_x_H3_H1_SM1_H2_SM2/BP5_x_H3_H1_SM2_H2_SM1)
    
        
    # zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP5: $\sigma(X\to S(bb) H(\gamma\gamma)) / \sigma(X\to S(\gamma\gamma) H(bb))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    # twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
    #                 ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    
    # plt.savefig('plots2D/BP5_BR_XSH/BP5_XS_XSH_bbgamgam_ratio_fig.pdf')
    # plt.show()
    # plt.close()

    # plt.scatter(x, y, c=z, cmap='viridis')
    # plt.colorbar()
    # plt.show()
    # plt.close()

    # #### BP6 ####

    # ## SM H1 -> bb, H2 -> gamgam (1) ##

    # BP6_mH1, BP6_mH2, BP6_mH3, BP6_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH/calc_BP6.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
      
    # x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP6_mH2, BP6_mH3, BP6_x_H3_H1_SM1_H2_SM2/norm)

    # zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    # #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP6: $\sigma(X\to S(\gamma\gamma)H(bb))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(126, 500), ylims=(255, 1000))

    # twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{S}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = M_{S}$', (298, 575), (337, 445), (353, 336),
    #                 ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
        
    # plt.savefig('plots2D/BP6_BR_XSH/BP6_XS_XSH_bbgamgam_1_fig.pdf')
    # plt.show()
    # plt.close()

    # plt.scatter(x, y, c=z, cmap='viridis')
    # plt.colorbar()
    # plt.show()
    # plt.close()

    # del x, y, z, xi, yi


    # ## SM H1 -> gamgam, H2 -> bb (2) ##

    # BP6_mH1, BP6_mH2, BP6_mH3, BP6_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH/calc_BP6.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')
      
    # x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP6_mH1, BP6_mH3, BP6_x_H3_H1_SM2_H2_SM1/norm)

    # zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    # #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP6: $\sigma(X\to S(bb)H(\gamma\gamma))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(126, 500), ylims=(255, 650))

    # twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{S}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = M_{S}$', (298, 575), (337, 445), (353, 336),
    #                 ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
        
    # plt.savefig('plots2D/BP6_BR_XSH/BP6_XS_XSH_bbgamgam_2_fig.pdf')
    # plt.show()
    # plt.close()

    # plt.scatter(x, y, c=z, cmap='viridis')
    # plt.colorbar()
    # plt.show()
    # plt.close()

    # del x, y, z, xi, yi


    # #### BP6 ####

    # ## SM (1)/(2) ##

    # BP6_mH1, BP6_mH2, BP6_mH3, BP6_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH/calc_BP6.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    # BP6_mH1_2, BP6_mH2_2, BP6_mH3_2, BP6_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH/calc_BP6.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')

    # print(BP6_mH1 == BP6_mH1_2)
    # print(BP6_mH2 == BP6_mH2_2)
    # print(BP6_mH3 == BP6_mH3_2)

    # x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP6_mH1, BP6_mH3, BP6_x_H3_H1_SM1_H2_SM2/BP6_x_H3_H1_SM2_H2_SM1)

    # zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    # #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    # twoDPlot.plotAuxTitleAndBounds2D(r"BP6: $\sigma(X\to S(\gamma\gamma)H(bb))/\sigma(X\to S(bb)H(\gamma\gamma))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(126, 500), ylims=(255, 650))

    # twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{S}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = M_{S}$', (298, 575), (337, 445), (353, 336),
    #                 ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
        
    # plt.savefig('plots2D/BP6_BR_XSH/BP6_XS_XSH_bbgamgam_ratio_fig.pdf')
    # plt.show()
    # plt.close()

    # plt.scatter(x, y, c=z, cmap='viridis')
    # plt.colorbar()
    # plt.show()
    # plt.close()

    # del x, y, z, xi, yi

    #### BP5: ####

    ## BP5: SM TOT ##

    twoDPlot.calculateSort2D('plots2D/BP5_BR_XSH/output_BP5_BR_XSH.tsv', 'plots2D/BP5_BR_XSH', 'calc_BP5.tsv', 'bb', 'gamgam')

    BP5_mH1, BP5_mH2, BP5_mH3, BP5_x_H3_SM1SM2 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1H2_SM1SM2')
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP5_mH1, BP5_mH3, BP5_x_H3_SM1SM2/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP5: $\sigma(X\to SH \to bb\gamma\gamma)$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    
    plt.savefig('plots2D/BP5_BR_XSH/BP5_XS_XSH_bbgamgam_tot_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi

    ## BP5: SM H1 -> bb, H2 -> gamgam (1) ##

    BP5_mH1, BP5_mH2, BP5_mH3, BP5_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP5_mH1, BP5_mH3, BP5_x_H3_H1_SM1_H2_SM2/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP5: $\sigma(X\to S(bb) H(\gamma\gamma))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    
    plt.savefig('plots2D/BP5_BR_XSH/BP5_XS_XSH_bbgamgam_1_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi

    ## BP5: SM H1 -> gamgam, H2 -> bb (2) ##

    BP5_mH1, BP5_mH2, BP5_mH3, BP5_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')
    
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP5_mH1, BP5_mH3, BP5_x_H3_H1_SM2_H2_SM1/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP5: $\sigma(X\to S(\gamma\gamma)H(bb) )$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    
    plt.savefig('plots2D/BP5_BR_XSH/BP5_XS_XSH_bbgamgam_2_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    ## BP5: SM Ratio (1)/(2) ##

    
    BP5_mH1, BP5_mH2, BP5_mH3, BP5_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    BP5_mH1_2, BP5_mH2_2, BP5_mH3_2, BP5_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP5_BR_XSH/calc_BP5.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')

    print(BP5_mH1 == BP5_mH1_2)
    print(BP5_mH2 == BP5_mH2_2)
    print(BP5_mH3 == BP5_mH3_2)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP5_mH1, BP5_mH3, BP5_x_H3_H1_SM1_H2_SM2/BP5_x_H3_H1_SM2_H2_SM1)
    
        
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.imshow(zi, origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP5: $\sigma(X\to S(bb) H(\gamma\gamma)) / \sigma(X\to S(\gamma\gamma) H(bb))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(1, 124), ylims=(126, 500))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{H}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = 2 M_{S}$', (3, 235), (26, 134), (75, 134),
                    ([0, 130], [2*125.09, 2*125.09]), ([0,130], [125.09, 130+125.09]), ([0,130],[0, 2*130]))
    
    plt.savefig('plots2D/BP5_BR_XSH/BP5_XS_XSH_bbgamgam_ratio_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()


    #### BP6: ####

    ## BP6: SM H1 -> bb, H2 -> gamgam (1) ##

    twoDPlot.calculateSort2D('plots2D/BP6_BR_XSH/output_BP6_BR_XSH.tsv', 'plots2D/BP6_BR_XSH', 'calc_BP6.tsv', 'bb', 'gamgam')

    BP6_mH1, BP6_mH2, BP6_mH3, BP6_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH/calc_BP6.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
      
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP6_mH2, BP6_mH3, BP6_x_H3_H1_SM1_H2_SM2/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    plt.imshow(zi, origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP6: $\sigma(X\to S(\gamma\gamma)H(bb))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(126, 500), ylims=(255, 1000))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{S}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = M_{S}$', (298, 575), (337, 445), (353, 336),
                    ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
        
    plt.savefig('plots2D/BP6_BR_XSH/BP6_XS_XSH_bbgamgam_1_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    ## BP6: SM H1 -> gamgam, H2 -> bb (2) ##

    BP6_mH1, BP6_mH2, BP6_mH3, BP6_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH/calc_BP6.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')
      
    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP6_mH2, BP6_mH3, BP6_x_H3_H1_SM2_H2_SM1/norm)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    plt.imshow(zi, origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP6: $\sigma(X\to S(bb)H(\gamma\gamma))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(126, 500), ylims=(255, 1000))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{S}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = M_{S}$', (298, 575), (337, 445), (353, 336),
                    ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
        
    plt.savefig('plots2D/BP6_BR_XSH/BP6_XS_XSH_bbgamgam_2_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi


    #### BP6: ####

    ## BP6: SM (1)/(2) ##

    BP6_mH1, BP6_mH2, BP6_mH3, BP6_x_H3_H1_SM1_H2_SM2 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH/calc_BP6.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM1_H2_SM2')
    BP6_mH1_2, BP6_mH2_2, BP6_mH3_2, BP6_x_H3_H1_SM2_H2_SM1 = twoDPlot.pandasReader('plots2D/BP6_BR_XSH/calc_BP6.tsv', 'mH1', 'mH2', 'mH3', 'x_H3_H1_SM2_H2_SM1')

    print(BP6_mH1 == BP6_mH1_2)
    print(BP6_mH2 == BP6_mH2_2)
    print(BP6_mH3 == BP6_mH3_2)

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP6_mH2, BP6_mH3, BP6_x_H3_H1_SM1_H2_SM2/BP6_x_H3_H1_SM2_H2_SM1)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')


    plt.imshow(zi, origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
    #             extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    twoDPlot.plotAuxTitleAndBounds2D(r"BP6: $\sigma(X\to S(\gamma\gamma)H(bb))/\sigma(X\to S(bb)H(\gamma\gamma))$ with $M_{S}$, $M_{X}$ free", r"$M_{S}$", r"$M_{X}$", 'test', xlims=(126, 500), ylims=(255, 1000))

    twoDPlot.plotAuxRegion2D(r'$M_{X} = 2 M_{S}$', r'$M_{X} = M_{S} + M_{H}$', r'$M_{X} = M_{S}$', (298, 575), (337, 445), (353, 336),
                    ([120, 510], [2*120, 2*510]), ([120, 510], [120+125.09, 510+125.09]), ([120, 510], [120, 510]))
        
    plt.savefig('plots2D/BP6_BR_XSH/BP6_XS_XSH_bbgamgam_ratio_fig.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    # plt.show()
    plt.close()

    del x, y, z, xi, yi



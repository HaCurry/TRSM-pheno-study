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

if __name__ == '__main__':

    plt.style.use(hep.style.ATLAS)
    hep.style.use({"mathtext.default": "rm"})
    mpl.rcParams['axes.labelsize'] = 19
    mpl.rcParams['axes.titlesize'] = 19

    #################
    #### NWA h_3 ####
    #################

    #### BP2: ####            

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 'mH1', 'mH2', 'mH3', 'w_H3')
    # BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3 = twoDPlot.kineticExcluder(BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3)

    BP2_NWA_H3 = BP2_w_H3/BP2_mH3

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_NWA_H3)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    contf = plt.contourf(xi, yi, zi, extent=[x.min(), x.max(), y.min(), y.max()])

    twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\Gamma(h_{3})/M_{3}$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r'$\Gamma(h_{3})/M_{3}$', xlims=(1, 124), ylims=(126, 500), cbarfmt='{x:.3f}')
    # plt.title(r"BP2: $\Gamma_{h_{3}}/M_{3}$")
    # plt.colorbar(label=r'$\Gamma_{h_{3}}/M_{3}$', format='{x:.3f}')
    
    plt.tight_layout()
    plt.savefig('plots2D/BP2_BR_XSH/BP2_NWA.pdf')
    # plt.show()
    # increase fontsize so that subsubscripts are visible, enable plt.tight_layout() and maybe flush the colorbar agains the figure border
    plt.close()

    del BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3, x, y, z

    #### BP3: ####            

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/output_BP3_BR_XSH.tsv', 'mH1', 'mH2', 'mH3', 'w_H3')
    # BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3 = twoDPlot.kineticExcluder(BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3)

    BP3_NWA_H3 = BP3_w_H3/BP3_mH3

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_NWA_H3)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    contf = plt.contourf(xi, yi, zi, extent=[x.min(), x.max(), y.min(), y.max()])

    twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\Gamma(h_{3})/M_{3}$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r'$\Gamma(h_{3})/M_{3}$', xlims=(126, 500), ylims=(255, 650), cbarfmt='{x:.3f}')

    plt.tight_layout()
    plt.savefig('plots2D/BP3_BR_XSH/BP3_NWA.pdf')
    # plt.show()
    plt.close()

    del BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3, x, y, z

    #################
    #### NWA h_2 ####
    #################

    #### BP2: ####            

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 'mH1', 'mH2', 'mH3', 'w_H2')
    # BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3 = twoDPlot.kineticExcluder(BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3)

    BP2_NWA_H3 = BP2_w_H3/BP2_mH2

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_NWA_H3)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    contf = plt.contourf(xi, yi, zi, extent=[x.min(), x.max(), y.min(), y.max()])

    twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\Gamma(h_{2})/M_{2}$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r'$\Gamma(h_{2})/M_{2}$', xlims=(1, 124), ylims=(126, 500))
    # plt.title(r"BP2: $\Gamma_{h_{3}}/M_{3}$")
    # plt.colorbar(label=r'$\Gamma_{h_{3}}/M_{3}$', format='{x:.3f}')
    
    plt.tight_layout()
    plt.savefig('plots2D/BP2_BR_XSH/BP2_NWA_h2.pdf')
    # plt.show()
    # increase fontsize so that subsubscripts are visible, enable plt.tight_layout() and maybe flush the colorbar agains the figure border
    plt.close()

    del BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3, x, y, z

    #### BP3: ####            

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/output_BP3_BR_XSH.tsv', 'mH1', 'mH2', 'mH3', 'w_H2')
    # BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3 = twoDPlot.kineticExcluder(BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3)

    BP3_NWA_H3 = BP3_w_H3/BP3_mH2

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_NWA_H3)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    contf = plt.contourf(xi, yi, zi, extent=[x.min(), x.max(), y.min(), y.max()])

    twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\Gamma(h_{2})/M_{2}$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r'$\Gamma(h_{2})/M_{2}$', xlims=(126, 500), ylims=(255, 650), cbarfmt='{x:.3f}')

    plt.tight_layout()
    plt.savefig('plots2D/BP3_BR_XSH/BP3_NWA_h2.pdf')
    # plt.show()
    plt.close()
    plt.scatter(x, y, c=z)
    plt.colorbar()
    # plt.show()
    plt.close()

    del BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3, x, y, z

    #################
    #### NWA h_1 ####
    #################

    #### BP2: ####            

    BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3 = twoDPlot.pandasReader('plots2D/BP2_BR_XSH/output_BP2_BR_XSH.tsv', 'mH1', 'mH2', 'mH3', 'w_H1')
    # BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3 = twoDPlot.kineticExcluder(BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3)

    BP2_NWA_H3 = BP2_w_H3/BP2_mH1

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP2_mH1, BP2_mH3, BP2_NWA_H3)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    contf = plt.contourf(xi, yi, zi, extent=[x.min(), x.max(), y.min(), y.max()])

    twoDPlot.plotAuxTitleAndBounds2D(r"BP2: $\Gamma(h_{1})/M_{1}$", r"$M_{1}$ [GeV]", r"$M_{3}$ [GeV]", r'$\Gamma(h_{1})/M_{1}$', xlims=(1, 124), ylims=(126, 500))
    # plt.title(r"BP2: $\Gamma_{h_{3}}/M_{3}$")
    # plt.colorbar(label=r'$\Gamma_{h_{3}}/M_{3}$', format='{x:.3f}')
    
    plt.tight_layout()
    plt.savefig('plots2D/BP2_BR_XSH/BP2_NWA_h1.pdf')
    # plt.show()
    # increase fontsize so that subsubscripts are visible, enable plt.tight_layout() and maybe flush the colorbar agains the figure border
    plt.close()

    del BP2_mH1, BP2_mH2, BP2_mH3, BP2_w_H3, x, y, z

    #### BP3: ####            

    BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3 = twoDPlot.pandasReader('plots2D/BP3_BR_XSH/output_BP3_BR_XSH.tsv', 'mH1', 'mH2', 'mH3', 'w_H1')
    # BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3 = twoDPlot.kineticExcluder(BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3)

    BP3_NWA_H3 = BP3_w_H3/BP3_mH1
    print(min(BP3_NWA_H3), max(BP3_NWA_H3))

    x, y, z, xi, yi = twoDPlot.plotAuxVar2D(BP3_mH2, BP3_mH3, BP3_NWA_H3)

    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    # plt.imshow(zi, origin='lower',
    #            extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')

    contf = plt.contourf(xi, yi, zi, extent=[x.min(), x.max(), y.min(), y.max()])

    twoDPlot.plotAuxTitleAndBounds2D(r"BP3: $\Gamma(h_{1})/M_{1}$", r"$M_{2}$ [GeV]", r"$M_{3}$ [GeV]", r'$\Gamma(h_{1})/M_{1}$', xlims=(126, 500), ylims=(255, 650))
    plt.xlim(126, 500)
    plt.ylim(255, 650)
    plt.tight_layout()
    plt.savefig('plots2D/BP3_BR_XSH/BP3_NWA_h1.pdf')
    # plt.show()
    plt.close()

    plt.scatter(x,y,c=z)
    plt.colorbar()
    # plt.show()
    plt.close()

    del BP3_mH1, BP3_mH2, BP3_mH3, BP3_w_H3, x, y, z

import subprocess
import os
import re

import numpy as np
import pandas
import matplotlib
import matplotlib.pyplot as plt

def SusHiInputFileNNLO(mass, energy,
                       pdfLO='MMHT2014lo68cl.LHgrid',
                       pdfNLO='MMHT2014nlo68cl.LHgrid',
                       pdfNNLO=' MMHT2014nnlo68cl.LHgrid', 
                       pdfN3LO='MMHT2014nnlo68cl.LHgrid',
                       **kwargs):

    if 'renormScalemuR' in kwargs:
        renormScalemuR = kwargs['renormScalemuR']

    else:
        renormScalemuR = 0.5

    if 'factScalemuF' in kwargs:
        factScalemuF = kwargs['factScalemuF']

    else:
        factScalemuF = 0.5

    # everything set to default (see the example SM-NNLO.in input given by SusHi)
    # except electroweak cont. for ggh set to 0 (the LHCHWG recommendations and
    # ScannerS have no electroweak cont.)
    inputFile = f'''Block SUSHI
  1   0		# model: 0 = SM, 1 = MSSM, 2 = 2HDM, 3 = NMSSM
  2   11	# 11 = scalar Higgs (h), 21 = pseudoscalar Higgs (A)
  3   0		# collider: 0 = p-p, 1 = p-pbar
  4   {energy:.8e}	# center-of-mass energy in GeV
  5   2		# order ggh: -1 = off, 0 = LO, 1 = NLO, 2 = NNLO, 3 = N3LO
  6   2 	# order bbh: -1 = off, 0 = LO, 1 = NLO, 2 = NNLO
  7   0 	# electroweak cont. for ggh:
                # 0 = no, 1 = light quarks at NLO, 2 = SM EW factor
 19   1		# 0 = silent mode of SusHi, 1 = normal output
 20   0         # ggh@nnlo subprocesses: 0=all, 10=ind. contributions
Block SMINPUTS		# Standard Model inputs
  1   1.27934000e+02	# alpha_em^(-1)(MZ) SM MSbar
  2   1.16637000e-05	# G_Fermi
  3   1.17200000e-01	# alpha_s(MZ) SM MSbar
  4   9.11876000e+01	# m_Z(pole)
  5   4.18000000e+00	# m_b(m_b)
  6   1.73300000e+02	# m_t(pole)
  8   1.27500000e+00	# m_c(m_c)
Block MASS
  25  {mass:.8e}	# Higgs mass
Block DISTRIB
  1   0		# distribution : 0 = sigma_total, 1 = dsigma/dpt,
        #                2 = dsigma/dy,   3 = d^2sigma/dy/dpt
        #                (values for pt and y: 22 and 32)
  2   0		# pt-cut: 0 = no, 1 = pt > ptmin, 2 = pt < ptmax,
        #         3 = ptmin < pt < ptmax
 21   30.d0	# minimal pt-value ptmin in GeV
 22   100.d0	# maximal pt-value ptmax in GeV
  3   0		# rapidity-cut: 0 = no, 1 = Abs[y] < ymax,
        #    2 = Abs[y] > ymin, 3 = ymin < Abs[y] < ymax
 31   0.5d0	# minimal rapidity ymin
 32   1.5d0	# maximal rapidity ymax
  4   0		# 0 = rapidity, 1 = pseudorapidity
Block SCALES
  1   {renormScalemuR:.2f} 	# renormalization scale muR/mh
  2   {factScalemuF:.2f}	# factorization scale muF/mh
 11   1.0 	# renormalization scale muR/mh for bbh
 12   0.25	# factorization scale muF/mh for bbh
  3   0         # 1 = Use (muR,muF)/Sqrt(mh^2+pt^2) for dsigma/dpt and d^2sigma/dy/dpt
Block RENORMBOT # Renormalization of the bottom sector
  1   0  	# m_b used for bottom Yukawa:     0 = OS, 1 = MSbar(mb), 2 = MSbar(muR)
Block PDFSPEC
  1   {pdfLO}	# name of pdf (lo)
  2   {pdfNLO}	# name of pdf (nlo)
  3   {pdfNNLO}	# name of pdf (nnlo)
  4   {pdfN3LO}	# name of pdf (n3lo)
 10  0		# set number - if different for LO, NLO, NNLO, N3LO use entries 11, 12, 13, 14
Block VEGAS
# parameters for NLO SusHi
         1    10000   # Number of points
         2        5   # Number of iterations
         3       10   # Output format of VEGAS integration
# parameters for ggh@nnlo:
         4     2000   # Number of points
         5        5   # Number of iterations
        14     5000   # Number of points in second run
        15        2   # Number of iterations in second run
         6        0   # Output format of VEGAS integration
# parameters for bbh@nnlo:
         7     2000   # Number of points
         8        5   # Number of iterations
        17     5000   # Number of points in second run
        18        2   # Number of iterations in second run
         9        0   # Output format of VEGAS integration
Block FACTORS
  1   1.d0	# factor for yukawa-couplings: c
  2   1.d0	# t
  3   1.d0	# b '''

    return inputFile


def SusHiInputFileN3LO(mass, energy,
                       pdfLO = 'MMHT2014lo68cl.LHgrid',
                       pdfNLO = 'PDF4LHC15_nlo_100.LHgrid',
                       pdfNNLO = 'PDF4LHC15_nnlo_100.LHgrid',
                       pdfN3LO = 'PDF4LHC15_nnlo_100.LHgrid',
                       **kwargs):

    inputFile = f'''Block SUSHI
  1   0         # model: 0 = SM, 1 = MSSM, 2 = 2HDM, 3 = NMSSM
  2   11        # 11 = scalar Higgs (h), 21 = pseudoscalar Higgs (A)
  3   0         # collider: 0 = p-p, 1 = p-pbar
  4   {energy:.8e}  # center-of-mass energy in GeV
  5   3         # order ggh: -1 = off, 0 = LO, 1 = NLO, 2 = NNLO, 3 = N3LO
  6   2         # order bbh: -1 = off, 0 = LO, 1 = NLO, 2 = NNLO
  7   2         # electroweak cont. for ggh:
                # 0 = no, 1 = light quarks at NLO, 2 = SM EW factor
 19   1         # 0 = silent mode of SusHi, 1 = normal output
 20   10         # ggh@nnlo subprocesses: 0=all, 10=ind. contributions
Block SMINPUTS          # Standard Model inputs
  1   1.27934000e+02    # alpha_em^(-1)(MZ) SM MSbar
  2   1.16637000e-05    # G_Fermi
  3   1.18000000e-01    # alpha_s(MZ) SM MSbar
  4   9.11876000e+01    # m_Z(pole)
  5   4.18000000e+00    # m_b(m_b)
  6   1.72500000e+02    # m_t(pole)
  8   1.12000000e+00    # m_c(m_c) <- yields mc^OS=1.64GeV
Block MASS
  25  {mass:.8e}      # Higgs mass
Block GGHMT
        -1    3   # factor out exact LO result at LO(=1)/NLO(=2)/etc.
         0   -1   # expand through 1/mt^n at LO [-1=exact]
         1    4   # expand gg through 1/mt^n at NLO
         2    4   # expand gg through 1/mt^n at NNLO
        10    1   # [0/1]: match to high energy limit at NLO  [n/y]
        20    1   # [0/1]: match to high energy limit at NNLO [n/y]
        30    1   # [0/1]: match to high energy limit at N3LO [n/y]
Block GGHSOFT # parameters for soft expansion
         1    1  16  0   # NLO  [0/1=n/y] [order] sig(x)/x^[n]
         2    1  16  0   # NNLO [0/1=n/y] [order] sig(x)/x^[n]
         3    1  16  0   # N3LO [0/1=n/y] [order] sig(x)/x^[n]
Block DISTRIB
  1   0         # distribution : 0 = sigma_total, 1 = dsigma/dpt,
                #                2 = dsigma/dy,   3 = d^2sigma/dy/dpt
                #                (values for pt and y: 22 and 32)
  2   0         # pt-cut: 0 = no, 1 = pt > ptmin, 2 = pt < ptmax,
                #         3 = ptmin < pt < ptmax
 21   30.d0     # minimal pt-value ptmin in GeV
 22   100.d0    # maximal pt-value ptmax in GeV
  3   0         # rapidity-cut: 0 = no, 1 = Abs[y] < ymax,
                #    2 = Abs[y] > ymin, 3 = ymin < Abs[y] < ymax
 31   0.5d0     # minimal rapidity ymin
 32   1.5d0     # maximal rapidity ymax
  4   0         # 0 = rapidity, 1 = pseudorapidity
Block SCALES
  1   0.5       # renormalization scale muR/mh
  2   0.5       # factorization scale muF/mh
 11   1.0       # renormalization scale muR/mh for bbh
 12   0.25      # factorization scale muF/mh for bbh
  3   0         # 1 = Use (muR,muF)/Sqrt(mh^2+pt^2) for dsigma/dpt and d^2sigma/dy/dpt
Block RENORMBOT # Renormalization of the bottom sector
  1   0         # m_b used for bottom Yukawa:     0 = OS, 1 = MSbar(mb), 2 = MSbar(muR)
  4 4.92 #
Block PDFSPEC
  1   {pdfLO}     # name of pdf (lo)
  2   {pdfNLO} # name of pdf (nlo)
  3   {pdfNNLO} # name of pdf (nnlo)
  4   {pdfNNLO} # name of pdf (n3lo)
 10  0          # set number - if different for LO, NLO, NNLO, N3LO use entries 11, 12, 13, 14
Block VEGAS
# parameters for NLO SusHi
         1    15000   # Number of points
         2        8   # Number of iterations
         3       10   # Output format of VEGAS integration
# parameters for ggh@nnlo:
         4     4000   # Number of points
         5       10   # Number of iterations
        14    10000   # Number of points in second run
        15        4   # Number of iterations in second run
         6        0   # Output format of VEGAS integration
# parameters for bbh@nnlo:
         7     2000   # Number of points
         8        5   # Number of iterations
        17     5000   # Number of points in second run
        18        2   # Number of iterations in second run
         9        0   # Output format of VEGAS integration
Block FACTORS
  1   1.d0      # factor for yukawa-couplings: c
  2   1.d0      # t
  3   1.d0      # b'''

    return inputFile


def SusHiCrossSections(masses, energy, order, pathOutputCrossSec, pathOutputCrossSecPlots,
                       pathTemp, pathSUSHI, **kwargs):

    crossSec = []

    # pathTemp = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/SusHiOutputsTemp'
    # pathSUSHI = '/afs/cern.ch/user/i/ihaque/scannerS/ScannerS-master/build/sh-bbyy-pheno/testing/SusHi_HiggsCrossSections/SusHi_install/SusHi-1.6.1/bin/sushi' 

    # absolute paths for the config and output files do not work because
    # sushi cannot handle hyphens in the paths for some reason.
    # hence the need of separating paths into absolute... & relative...
    absolutePathExecutionConfig = os.path.join(pathTemp, 'temp_config.in')
    absolutePathExecutionOutput = os.path.join(pathTemp, 'temp_output.out')
    relativePathExecutionConfig = 'temp_config.in'
    relativePathExecutionOutput = 'temp_output.out'

    crossSecList = []
    for mass in masses:

        # creates contents of pathExecutionConfig
        if order == 'NNLO':
            inputFileContents = SusHiInputFileNNLO(mass, energy,
                                               pdfLO='MMHT2014lo68cl.LHgrid',
                                               pdfNLO='PDF4LHC15_nlo_30_pdfas.LHgrid' ,
                                               pdfNNLO='PDF4LHC15_nnlo_30_pdfas.LHgrid',
                                               **kwargs)

        elif order == 'N3LO':
            inputFileContents = SusHiInputFileN3LO(mass, energy,
                                               **kwargs)

        else: 
            raise Exception('order needs to be either \'NNLO\' or \'N3LO\'')

        with open(absolutePathExecutionConfig , "w") as inputFile:
            inputFile.write(inputFileContents)

        # for subprocesses.run below
        runSUSHI = [pathSUSHI, relativePathExecutionConfig, relativePathExecutionOutput]

        # run the executable
        shell_output = subprocess.run(runSUSHI, cwd=pathTemp)

        print('\n\n===============================================\n\n')

        outputFileRows = ''
        with open(absolutePathExecutionOutput) as outputFile:
            for row in outputFile:
                outputFileRows = outputFileRows + row

        # regex pattern
        pattern = re.compile('1.*# ggh XS in pb')

        # match object
        lineCrossSec = pattern.findall(outputFileRows)

        if len(lineCrossSec) != 1:
            raise Exception('Something went wrong, there should only be one \'ggh XS in pb\' match')

        print(lineCrossSec)
        crossSec = float(lineCrossSec[0].split()[1])
        print(crossSec)
        crossSecList.append((mass, crossSec))

    dfOut = pandas.DataFrame(crossSecList, columns=['mass', 'SMCrossSec'])
    print(dfOut)
    dfOut.to_csv(pathOutputCrossSec, sep='\t')

    plt.plot(np.array(dfOut['mass']), np.array(dfOut['SMCrossSec']), marker='o')
    plt.yscale('log')
    plt.savefig(pathOutputCrossSecPlots)
    plt.close()

if __name__ == '__main__':
    print('Hejsan!')




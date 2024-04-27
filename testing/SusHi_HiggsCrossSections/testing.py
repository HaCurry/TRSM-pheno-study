import os

import matplotlib
import matplotlib.pyplot as plt
import pandas
import scipy.interpolate as interp

if __name__ == '__main__':

    pathPlots = '/eos/user/i/ihaque/SusHiPlots'

    dfOld = pandas.read_table('14TeV_YR4CrossSections.tsv')
    dfScannerS = pandas.read_table('13TeV_ScannerSCrossSections.tsv')
    dfScannerSNew = pandas.read_table('test.tsv')

    YR4Old = interp.CubicSpline(dfOld['mass'], dfOld['SMCrossSec'])
    ScannerS = interp.CubicSpline(dfScannerS['mass'], dfScannerS['SMCrossSec'])
    ScannerSNew = interp.CubicSpline(dfScannerSNew['mass'], dfScannerSNew['SMCrossSec'])

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(dfScannerS['mass'], YR4Old(dfScannerS['mass'])/1E3)
    ax.plot(dfScannerS['mass'], ScannerS(dfScannerS['mass'])/1E3)
    ax.plot(dfScannerS['mass'], YR4Old(dfScannerS['mass'])/ScannerS(dfScannerS['mass']))
    ax.plot(dfScannerS['mass'], YR4Old(dfScannerS['mass'])/ScannerSNew(dfScannerS['mass']))
    ax.set_yscale('log')
    ax.set_xlim(0, 1000)
    ax.set_ylim(9E-1, 8E0)
    plt.savefig(os.path.join(pathPlots, 'tabort.pdf'))

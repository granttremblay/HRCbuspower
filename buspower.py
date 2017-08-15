#!/usr/bin/env python

"""
buspower.py: Plot the current, voltage, and power of the HRC Primary bus
"""

__author__ = "Dr. Grant R. Tremblay"
__license__ = "MIT"

import sys
import os

import datetime as dt

from astropy.io import ascii

import matplotlib.pyplot as plt
from matplotlib.dates import epoch2num

try:
    import plotly.plotly
except ImportError:
    print("plotly is not installed. Disabling this functionality.")

import numpy as np
from scipy import stats

def convert_time(rawtimes):
    """
    Convert input CXC time (sec) to the time base required for the matplotlib
    plot_date function (days since start of the Year 1 A.D - yes, really).

    :param times: iterable list of times, in units of CXCsec (sec since 1998.0)
    :rtype: plot_date times (days since Year 1 A.D.)
    """

    # rawtimes is in units of CXC seconds, or seconds since 1998.0
    # Compute the Delta T between 1998.0 (CXC's Epoch) and 1970.0 (Unix Epoch)

    seconds_since_1998_0 = rawtimes[0]

    cxctime = dt.datetime(1998, 1, 1, 0, 0, 0)
    unixtime = dt.datetime(1970, 1, 1, 0, 0, 0)

    # Calculate the first offset from 1970.0, needed by matplotlib's plotdate
    # The below is equivalent (within a few tens of seconds) to the command
    # t0 = Chandra.Time.DateTime(times[0]).unix
    delta_time = (cxctime - unixtime).total_seconds() + seconds_since_1998_0

    plotdate_start = epoch2num(delta_time)

    # Now we use a relative offset from plotdate_start
    # the number 86,400 below is the number of seconds in a UTC day

    times = (np.asarray(rawtimes) - rawtimes[0]) / 86400. + plotdate_start

    return times

def compute_power(rawvolts, rawamps):
    """
    Compute the power. Looks trivial, but I'm gonna implement
    smoothing later.
    """

    power = rawvolts * rawamps

    return power


def make_plot(time, voltage, current, power):
    plt.style.use('ggplot')

    labelsizes = 13

    plt.rcParams['font.size'] = labelsizes
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = labelsizes
    plt.rcParams['xtick.labelsize'] = labelsizes
    plt.rcParams['ytick.labelsize'] = labelsizes

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(8, 12))
    ax1.plot_date(time, voltage,
                  markersize=1.5, color='gray',
                  alpha=0.8, label='2PRBSVL : Daily'
                  )


    ax1.set_title('HRC Primary Bus Power over Mission Lifetime')
    #ax1.set_xlabel('Year')
    ax1.set_ylabel('Volts')

    ax2.plot_date(time, current,
                  markersize=1.5, color='gray',
                  alpha=0.8, label='2PRBSCR : 5 Daily'
                  )


    ax2.set_ylabel('Amps')

    ax3.plot_date(time, power, markersize=1.5, label='Power')
    ax3.set_ylabel('Watts')
    ax3.set_xlabel('Year')

    ax1.legend(loc=1)
    ax2.legend(loc=1)
    ax3.legend(loc=1)

    plt.tight_layout()
    plt.show()

    # if kwargs is not None:
    #    for key, value in kwargs.iteritems()

def bindata(x, y, bins):
    """Bin the data, make errorbars"""

    bin_means, bin_edges, binnumber \
        = stats.binned_statistic(x, y, statistic='mean', bins=bins)

    bin_width = (bin_edges[1] - bin_edges[0])
    bin_centers = bin_edges[1:] - bin_width/2

    return bin_means, bin_edges, bin_width, bin_centers
    # nbins = 1000
    #
    # x, _ = np.histogram(times, bins=nbins)
    # sy, _ = np.histogram(times, bins=nbins, weights=power)
    # sy2, _ = np.histogram(times, bins=nbins, weights=power * power)
    #
    # mean = sy / x
    # std = np.sqrt(sy2/x - mean*mean)
    #
    # return x, sy, mean, std


def make_plotly_plot():
    """Optionally, make an interactive online plot at plot.ly"""
    pass
    #plotly.plotly.plot(rawtimes, rawvolts)

def main():

    vtab_daily = ascii.read('2PRBSVL_daily.csv')
    ctab_daily = ascii.read('2PRBSCR_daily.csv')

    match = set(vtab_daily['times']) == set(ctab_daily['times'])

    # make sure these match!
    if match:
        rawtimes = vtab_daily['times']
        rawvolts = vtab_daily['means']
        rawamps = ctab_daily['midvals']
    else:
        print("MSID times do not match!")
        sys.exit()

    #bintimes, bindata , mean, std = bindata(convert_time(rawtimes), voltage)

    power = compute_power(rawvolts, rawamps)

    make_plot(convert_time(rawtimes), rawvolts, rawamps, power)



if __name__ == '__main__':
    main()

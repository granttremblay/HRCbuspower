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


def make_plot(**kwargs):
    pass
    # if kwargs is not None:
    #    for key, value in kwargs.iteritems()

def make_plotly_plot():
    """Optionally, make an interactive online plot at plot.ly"""
    pass
    #plotly.plotly.plot(rawtimes, rawvolts)

def main():

    vtab = ascii.read('2PRBSVL.csv')
    ctab = ascii.read('2PRBSCR.csv')

    match = set(vtab['times']) == set(ctab['times'])

    # make sure these match!
    if match:
        rawtimes = vtab['times']
        rawvolts = vtab['vals']
        rawamps = ctab['vals']
    else:
        print("MSID times do not match!")
        sys.exit()

    convert_time(rawtimes)
    fig, ax = plt.subplots()
    ax.plot_date(convert_time(rawtimes), rawvolts)
    plt.show()


if __name__ == '__main__':
    main()

#!/usr/bin/env python

"""
anomaly_2011.py: Make a zoom-in and HRC/ACIS comparison
plot for the 2011 voltage drop
"""

__author__ = "Dr. Grant R. Tremblay"
__license__ = "MIT"

import sys

import datetime as dt

from astropy.io import ascii

import matplotlib.pyplot as plt
from matplotlib.dates import epoch2num


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



def make_plot(hrcdailytimes, acisdailytimes, fivemintimes, hrcdailyvolts,
          acisvolts, hrc5minvolts):

    plt.style.use('ggplot')

    labelsizes = 13

    plt.rcParams['font.size'] = labelsizes
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = labelsizes
    plt.rcParams['xtick.labelsize'] = labelsizes
    plt.rcParams['ytick.labelsize'] = labelsizes

    # plt.rc('font', family='Helvetica')

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=False, figsize=(12, 12))

    ax1.plot_date(hrcdailytimes, hrcdailyvolts,
                  markersize=1.5,
                  alpha=0.8, label='HRC 2PRBSVL'
                  )

    ax1.plot_date(acisdailytimes, acisvolts,
                  markersize=1.5,
                  alpha=0.8, label='ACIS 1DE28AVO'
                  )



    ax2.plot_date(fivemintimes, hrc5minvolts, markersize=1.5,
                  label='HRC 5 Minute Stats', color='gray', alpha=0.6)

    ax2.plot_date(hrcdailytimes, hrcdailyvolts, markersize=2.5, label='HRC Daily Stats')

    ax2.hlines(28.9, dt.date(2011,5,1), dt.date(2013,12,1), linestyle='dashed', colors='gray')
    ax2.hlines(28.27, dt.date(2012,5,1), dt.date(2013,12,1), linestyle='dashed', colors='gray')
    ax2.hlines(28.03, dt.date(2013,6,1), dt.date(2013,12,1), linestyle='dashed', colors='gray')


    ax1.set_title('HRC and ACIS +28V Bus Voltage Drop')
    ax1.set_ylabel('Voltage (Volts)')
    ax1.set_xlabel('Year')

    ax2.set_xlim([dt.date(2011,2,1), dt.date(2013,12,1)])
    ax2.set_ylim(26, 29.5)

    ax2.set_ylabel('Voltage(Volts)')
    ax2.set_xlabel('Year')



    ax1.legend(loc=1)
    ax2.legend(loc=1)

    plt.tight_layout()
    plt.show(block=True)
    fig.savefig('anomaly.pdf')

    # if kwargs is not None:
    #    for key, value in kwargs.iteritems()



def main():


    hrctab_daily = ascii.read('2PRBSVL_daily.csv')
    acistab_daily = ascii.read('1DE28AVO_daily.csv')

    hrc2011tab_5min = ascii.read('2PRBSVL_5min_2011.csv')

    hrcdailytimes = hrctab_daily['times']
    acisdailytimes = acistab_daily['times']
    fivemintimes = hrc2011tab_5min['times']

    hrcdailyvolts = hrctab_daily['means']
    hrc5minvolts = hrc2011tab_5min['means']

    acisvolts = acistab_daily['means']

    make_plot(convert_time(hrcdailytimes), convert_time(acisdailytimes),
              convert_time(fivemintimes), hrcdailyvolts,
              acisvolts, hrc5minvolts)


if __name__ == '__main__':
    main()

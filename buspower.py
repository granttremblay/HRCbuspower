#!/usr/bin/env python

"""
buspower.py: Plot the current, voltage, and power of the HRC Primary bus
"""

__author__ = "Dr. Grant R. Tremblay"
__license__ = "MIT"

import sys
import os

from astropy.io import ascii

import matplotlib.pyplot as plt
from matplotlib.dates import epoch2num

import numpy as np

def convert_time(rawtimes):

    # Number of seconds between 1970.0, the Unix epoch,
    # and rawtimes[0]
    t0 = 946814335.816

    plotdate0 = epoch2num(t0)

    return (np.asarray(rawtimes) - rawtimes[0]) / 86400. + plotdate0

def main():

    vtab = ascii.read('2PRBSVL.csv')
    ctab = ascii.read('2PRBSCR.csv')

    match = set(vtab['times']) == set(ctab['times'])

    if match:
        rawtimes = vtab['times']
        rawvolts = vtab['vals']
        rawamps = ctab['vals']
    else:
        print("MSID times do not match!")
        sys.exit()

    fig, ax = plt.subplots()
    ax.plot(rawtimes, rawvolts)
    ax.plot(rawtimes, rawamps)
    plt.show()


if __name__ == '__main__':
    main()

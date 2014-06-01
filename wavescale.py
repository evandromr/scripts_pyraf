#!/usr/bin/env python
#
# Find wavelenght solution to a calibration spectra
#
import glob
from pyraf import iraf

iraf.onedspec()
iraf.onedspec.identify.unlearn()

calspec = str(raw_input("Enter input spectra: "))

linelist = str(raw_input(
'Enter name of iraf file with list of lines (linelists$thar.dat): '))

if linelist == '':
    linelist = 'linelists$thar.dat'

iraf.onedspec.identify.coordlist = linelist
iraf.onedspec.identify(images=calspec)

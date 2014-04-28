#!/usr/bin/env python
#
# A simple script to combine spectra calling IRAF's scombine task
#
# Load Python standard modules
import glob
# Load third-party modules
import astropy.io.fits as fits
from pyraf import iraf


# choose spectra to combine
specre = str(raw_input("Enter regular expression for spectra files: "))
specfiles = glob.glob(specre)
specstring = ', '.join(specfiles)

# choose spectra output name
specout = str(raw_input("Enter output combined spectra name: "))

# unlearn previous settings
iraf.scombine.unlearn()

# Unse gain and readout noise from header or user defined
print "Using READNOISE and GAIN keywords of first spectra"
check = str(raw_input("Manually choose gain and rdnoise? Y/N: "))
if (check == 'Y') or (check == 'y'):
    rdnoise = float(raw_input("Enter ReadOutNoise: "))
    gain = float(raw_input("Enter Gain: "))
else:
    rdnoise = fits.getval(specfiles[0], 'RDNOISE')
    gain = fits.getval(specfiles[0], 'GAIN')

# setup
iraf.scombine.group = 'all'
iraf.scombine.combine = 'median'
iraf.scombine.reject = 'sigclip'
iraf.scombine.rdnoise = rdnoise
iraf.scombine.gain = gain

# call scombine
iraf.scombine(input=specstring, output=specout)

# visualize combined spectra with splot to check
iraf.splot.unlearn()
iraf.splot(specout)

print '--- DONE ---'

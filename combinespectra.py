#!/usr/bin/env python
#
# A simple script to combine spectra calling IRAF's scombine task
#
# Load Python standard modules
import glob
# Load third-party modules
from pyraf import iraf


# choose spectra to combine
specre = str(raw_input("Enter regular expression for spectra files: "))
specfiles = glob.glob(specre)
specstring = ', '.join(specfiles)

# choose spectra output name
specout = str(raw_input("Enter output combined spectra name: "))

# unlearn previous settings
iraf.scombine.unlearn()

# setup
iraf.scombine.scale = 'exposure'
iraf.scombine.rdnoise = 'rdnoise'
iraf.scombine.gain = 'gain'

# call scombine
iraf.scombine(input=specstring, output=specout)

# visualize combined spectra with splot to check
iraf.splot.unlearn()
iraf.splot(specout)

print '--- DONE ---'

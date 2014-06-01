#!/usr/bin/env python
#
# A script to reduce data from the Coude Spectrograph from the 1.6m telescope
# of the Observatorio do Pico dos Dias - Brazil
#
# Load Python standard modules
import glob
# Load third-party modules
from pyraf import iraf


print 'Loading IRAF packages ...'
iraf.imred()
iraf.ccdred()
iraf.specred()

print 'unlearning previous settings...'
iraf.ccdred.unlearn()
iraf.ccdred.ccdproc.unlearn()
iraf.ccdred.combine.unlearn()
iraf.specred.apall.unlearn()

# regular expression of files (e.g bias_00*.fits, flat-2000jan01_?.*)
imre = str(raw_input('Enter regular expression for images: '))
imlist = glob.glob(imre)
imin = ', '.join(imlist)

ref = str(raw_input('Enter reference aperture image (or Hit Enter): '))

# extract aperture spectra for science images
print 'Extracting aperture spectrum...'
iraf.specred.apall.readnoise = 'rdnoise'
iraf.specred.apall.gain = 'gain'
iraf.specred.apall.reference = ref
iraf.specred.apall(input=imin)

print '--- DONE ---'

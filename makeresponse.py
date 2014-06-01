#!/usr/bin/env python
#
# A script to reduce data from the Coude Spectrograph from the 1.6m telescope
# of the Observatorio do Pico dos Dias - Brazil
#
# Load Python standard modules
import glob
# Load third-party modules
import ds9
from pyraf import iraf


print 'Loading IRAF packages ...'
iraf.imred()
iraf.ccdred()
iraf.specred()

print 'unlearning previous settings...'
iraf.ccdred.unlearn()
iraf.ccdred.ccdproc.unlearn()
iraf.ccdred.combine.unlearn()
iraf.ccdred.zerocombine.unlearn()
iraf.ccdred.flatcombine.unlearn()
iraf.specred.response.unlearn()

# regular expression of files (e.g bias_00*.fits, flat-2000jan01_?.*)
theflat = str(raw_input('Enter flat image: '))

iraf.specred.extinction = ''
iraf.specred.caldir = ''
iraf.specred.observatory = 'lna'

print 'Create a response for flat...'
iraf.specred.response.interactive = True
iraf.specred.response.high_reject = 3.0
iraf.specred.response.low_reject = 3.0
iraf.specred.response(calibration=theflat,
                      normalization=theflat,
                      response='nFlat')

# check output flat image
print 'openning a ds9 window if not already openned...'
ds9.ds9()

print 'Check output file:'
iraf.imstatistics('nFlat')
print ' Running "imexamine" task..'
iraf.imexamine('nFlat', 1)

print '--- DONE ---'

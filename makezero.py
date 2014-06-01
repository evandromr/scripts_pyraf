#!/usr/bin/env python
#
# A script to reduce data from the Coude Spectrograph from the 1.6m telescope
# of the Observatorio do Pico dos Dias - Brazil
#
# Load Python standard modules
import glob
import os
import shutil
# Load third-party modules
import ds9
from pyraf import iraf


print 'Loading IRAF packages ...'
iraf.imred()
iraf.ccdred()

print 'unlearning previous settings...'
iraf.ccdred.unlearn()
iraf.ccdred.ccdproc.unlearn()
iraf.ccdred.combine.unlearn()
iraf.ccdred.zerocombine.unlearn()

# regular expression of files (e.g bias_00*.fits, flat-2000jan01_?.*)
zerore = str(raw_input('\nEnter regular expression for zero level images: '))

# list of files that match that regular expression
zerolist = glob.glob(zerore)
zeroin = ', '.join(zerolist)

print '\ncreating a zero_files/ dir to store original data'
if not os.path.isdir('zero_files'):
    os.mkdir('zero_files')

allfiles = zerolist
for file in allfiles:
    shutil.copy(file, 'zero_files/')

# combine bias images
print 'Combining zero level images...'
iraf.ccdred.zerocombine.ccdtype = ''
iraf.ccdred.zerocombine.reject = 'ccdclip'
iraf.ccdred.zerocombine.rdnoise = 'rdnoise'
iraf.ccdred.zerocombine.gain = 'gain'
iraf.ccdred.zerocombine(input=zeroin)

for zero in zerolist:
    os.remove(zero)

print 'openning a ds9 window if not already openned...'
ds9.ds9()

# check output image
print 'Check output file:'
iraf.imstatistics('Zero')

print ' Running "imexamine" task..'
iraf.imexamine('Zero', 1)

print '--- DONE ---'

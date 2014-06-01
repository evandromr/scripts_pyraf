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
iraf.ccdred.flatcombine.unlearn()

# regular expression of files (e.g bias_00*.fits, flat-2000jan01_?.*)
flatre = str(raw_input('Enter regular expression for flat images: '))

# list of files that match that regular expression
flatlist = glob.glob(flatre)
flatin = ', '.join(flatlist)

print 'creating a flat_files/ dir to store original data'
if not os.path.isdir('flat_files'):
    os.mkdir('flat_files')

allfiles = flatlist
for file in allfiles:
    shutil.copy(file, 'flat_files/')

# combine flat images
print 'Combining flat images ...'
iraf.ccdred.flatcombine.ccdtype = ''
iraf.ccdred.flatcombine.process = 'no'
iraf.ccdred.flatcombine.reject = 'ccdclip'
iraf.ccdred.flatcombine.rdnoise = 'rdnoise'
iraf.ccdred.flatcombine.gain = 'gain'
iraf.ccdred.flatcombine.output = 'Flat'
iraf.ccdred.flatcombine(input=flatin)

for file in flatlist:
    os.remove(file)

print 'openning a ds9 window if not already openned...'
ds9.ds9()

# check output flat image
print 'Check output file:'
iraf.imstatistics('Flat')
print ' Running "imexamine" task..'
iraf.imexamine('Flat', 1)

print '--- DONE ---'

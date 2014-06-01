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
from pyraf import iraf


print 'Loading IRAF packages ...'
iraf.imred()
iraf.ccdred()

print 'unlearning previous settings...'
iraf.ccdred.unlearn()
iraf.ccdred.ccdproc.unlearn()
iraf.ccdred.combine.unlearn()

# regular expression of files (e.g bias_00*.fits, flat-2000jan01_?.*)
imre = str(raw_input('Enter images to process: '))

zero = str(raw_input('Enter Zero level image (or Hit Enter if none): '))
flat = str(raw_input('Enter Flat-field image (or Hit Enter if none): '))
trimsec = str(raw_input('Enter trim section(or Hit Enter if none): '))

zeroquery = True
flatquery = True
trimquery = True

if zero == '':
    zeroquery = False
if flat == '':
    flatquery = False
if trimsec == '':
    trimquery = False

# list of files that match that regular expression
imlist = glob.glob(imre)
imin = ', '.join(imlist)

print 'creating a raw_files/ dir to store original data'
if not os.path.isdir('raw_files'):
    os.mkdir('raw_files')

allfiles = imlist
for file in allfiles:
    shutil.copy(file, 'raw_files/')

# correct images
print 'Running ccdproc task...'
iraf.ccdred.ccdproc.ccdtype = ''
iraf.ccdred.ccdproc.noproc = False
iraf.ccdred.ccdproc.fixpix = False
iraf.ccdred.ccdproc.overscan = False
iraf.ccdred.ccdproc.darkcor = False
iraf.ccdred.ccdproc.illumcor = False
iraf.ccdred.ccdproc.fringecor = False
iraf.ccdred.ccdproc.readcor = False
iraf.ccdred.ccdproc.scancor = False
iraf.ccdred.ccdproc.readaxis = 'line'
iraf.ccdred.ccdproc.zerocor = zeroquery
iraf.ccdred.ccdproc.zero = zero
iraf.ccdred.ccdproc.flatcor = flatquery
iraf.ccdred.ccdproc.flat = flat
iraf.ccdred.ccdproc.trim = trimquery
iraf.ccdred.ccdproc.trimsec = trimsec
iraf.ccdred.ccdproc(images=imin)

for file in imlist:
    os.remove(file)

print '--- DONE ---'

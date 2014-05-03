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
iraf.specred()

print 'unlearning previous settings...'
iraf.ccdred.unlearn()
iraf.ccdred.ccdproc.unlearn()
iraf.ccdred.combine.unlearn()
iraf.ccdred.zerocombine.unlearn()
iraf.ccdred.flatcombine.unlearn()
iraf.specred.response.unlearn()
iraf.specred.apall.unlearn()
iraf.specred.identify.unlearn()
iraf.specred.dispcor.unlearn()
iraf.imstatistics.unlearn()
iraf.imexamine.unlearn()
iraf.hedit.unlearn()
iraf.splot.unlearn()
iraf.continuum.unlearn()

# regular expression of files (e.g bias_00*.fits, flat-2000jan01_?.*)
zerore = str(raw_input('\nEnter regular expression for zero level images: '))
flatre = str(raw_input('Enter regular expression for flat images: '))
scire = str(raw_input('Enter regular expression for science images: '))
calre = str(raw_input('Enter regular expression for calibration images: '))

# list of files that match that regular expression
zerolist = glob.glob(zerore)
zeroin = ', '.join(zerolist)

flatlist = glob.glob(flatre)
flatin = ', '.join(flatlist)
flatzeros = ', '.join([f[:-5]+'_zero.fits' for f in flatlist])

scilist = glob.glob(scire)
sciin = ', '.join(scilist)
scizeros = ', '.join([sc[:-5]+'_zero.fits' for sc in scilist])
sciproc = ', '.join([sc[:-5]+'_proc.fits' for sc in scilist])
sciap = ', '.join([sc[:-5]+'_proc.ms.fits' for sc in scilist])
scispec = ', '.join([sc[:-5]+'_spec.fits' for sc in scilist])

callist = glob.glob(calre)
calin = ', '.join(callist)
calzeros = ', '.join([cal[:-5]+'_zero.fits' for cal in callist])
calproc = ', '.join([cal[:-5]+'_proc.fits' for cal in callist])
calap = ', '.join([cal[:-5]+'_proc.ms.fits' for cal in callist])

print 'openning a ds9 window if not already openned...'
ds9.ds9()

print 'creating a raw_files/ dir to store original data'
if not os.path.isdir('raw_files'):
    os.mkdir('raw_files')

allfiles = zerolist + flatlist + scilist + callist
for file in allfiles:
    shutil.copy(file, 'raw_files/')

# combine bias images
print 'Combining Bias images...'
iraf.ccdred.zerocombine.ccdtype = ''
iraf.ccdred.zerocombine.reject = 'ccdclip'
iraf.ccdred.zerocombine.rdnoise = 'rdnoise'
iraf.ccdred.zerocombine.gain = 'gain'
iraf.ccdred.zerocombine(input=zeroin)

for zero in zerolist:
    os.remove(zero)

# check output bias image
print 'Check output file:'
iraf.imstatistics('Zero')
print ' Running "imexamine" task..'
iraf.imexamine('Zero', 1)

# combine flat images
print 'Combining dome flat images ...'
iraf.ccdred.flatcombine.output = 'Flat'
iraf.ccdred.flatcombine.process = 'no'
iraf.ccdred.flatcombine.ccdtype = ''
iraf.ccdred.flatcombine.rdnoise = 'rdnoise'
iraf.ccdred.flatcombine.gain = 'gain'
iraf.ccdred.flatcombine(input=flatin)
for file in flatlist:
    os.remove(file)

# check output flat image
print 'Check output file:'
iraf.imstatistics('Flat')
print ' Running "imexamine" task..'
iraf.imexamine('Flat', 1)

iraf.specred.extinction = ''
iraf.specred.caldir = ''
iraf.specred.observatory = 'lna'

print 'Create a response for flat...'
iraf.specred.response.interactive = True
iraf.specred.response(calibration='Flat',
                      normalization='Flat',
                      response='nFlat')
# check output flat image
print 'Check output file:'
iraf.imstatistics('nFlat')
print ' Running "imexamine" task..'
iraf.imexamine('nFlat', 1)

# Trim data if necessary
trimquery = True
trimsection = str(raw_input('Enter trim section, or hit <Enter>: '))
if trimsection == '':
    trimquery = False

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
iraf.ccdred.ccdproc.zerocor = True
iraf.ccdred.ccdproc.zero = 'Zero'
iraf.ccdred.ccdproc.flatcor = True
iraf.ccdred.ccdproc.flat = 'nFlat'
iraf.ccdred.ccdproc.trim = trimquery
iraf.ccdred.ccdproc.trimsec = trimsection
# science images
iraf.ccdred.ccdproc(images=sciin)
# calibration images
iraf.ccdred.ccdproc(images=calin)

# extract aperture spectra for science images
print 'Extracting aperture spectra for science and calibration images ...'
iraf.specred.apall.readnoise = 'rdnoise'
iraf.specred.apall.gain = 'gain'
# science images
iraf.specred.apall(input=sciin)
# calibration images
iraf.specred.apall.reference = scilist[0]
iraf.specred.apall(input=calin)

print '--- DONE ---'

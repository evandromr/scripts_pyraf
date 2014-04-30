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
dflatre = str(raw_input('Enter regular expression for dome flat images: '))
iflatre = str(raw_input('Enter regular expression for internal flat images: '))
scire = str(raw_input('Enter regular expression for science images: '))
calre = str(raw_input('Enter regular expression for calibration images: '))

# list of files that match that regular expression
zerolist = glob.glob(zerore)
zeroin = ', '.join(zerolist)

dflatlist = glob.glob(dflatre)
dflatin = ', '.join(dflatlist)
dflatzeros = ', '.join([df[:-5]+'_zero.fits' for df in dflatlist])

iflatlist = glob.glob(iflatre)
iflatin = ', '.join(iflatlist)
iflatzeros = ', '.join([ifl[:-5]+'_zero.fits' for ifl in iflatlist])

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

allfiles = zerolist + dflatlist + iflatlist + scilist + callist
for file in allfiles:
    shutil.copy(file, 'raw_files/')

# combine bias images
print 'Combining Bias images...'
iraf.ccdred.zerocombine.output = 'Zero'
iraf.ccdred.zerocombine.combine = 'median'
iraf.ccdred.zerocombine.reject = 'ccdclip'
iraf.ccdred.zerocombine.ccdtype = ''
iraf.ccdred.zerocombine.rdnoise = 'RDNOISE'
iraf.ccdred.zerocombine.gain = 'GAIN'
iraf.ccdred.zerocombine(input=zeroin)

for zero in zerolist:
    os.remove(zero)

# check output bias image
print 'Check output file:'
iraf.imstatistics('Zero')
print ' Running "imexamine" task..'
iraf.imexamine('Zero', 1)

print 'Running zero level correction ...'
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
iraf.ccdred.ccdproc.trim = False
iraf.ccdred.ccdproc.flatcor = False
iraf.ccdred.ccdproc.zerocor = True
iraf.ccdred.ccdproc.zero = 'Zero'
# science images
iraf.ccdred.ccdproc(images=sciin)
# calibration images
iraf.ccdred.ccdproc(images=calin)
# dome flats
iraf.ccdred.ccdproc(images=dflatin)
# internal flats
iraf.ccdred.ccdproc(images=iflatin)

# combine flat images
print 'Combining dome flat images ...'
iraf.ccdred.flatcombine.output = 'dFlat'
iraf.ccdred.flatcombine.combine = 'median'
iraf.ccdred.flatcombine.reject = 'ccdclip'
iraf.ccdred.flatcombine.process = 'no'
iraf.ccdred.flatcombine.subsets = 'no'
iraf.ccdred.flatcombine.scale = 'mode'
iraf.ccdred.flatcombine.ccdtype = ''
iraf.ccdred.flatcombine.rdnoise = 'RDNOISE'
iraf.ccdred.flatcombine.gain = 'GAIN'
iraf.ccdred.flatcombine(input=dflatin)
for file in dflatlist:
    os.remove(file)

# check output flat image
print 'Check output file:'
iraf.imstatistics('dFlat')
print ' Running "imexamine" task..'
iraf.imexamine('dFlat', 1)

print 'Combining internal flat images ...'
iraf.ccdred.flatcombine.output = 'iFlat'
iraf.ccdred.flatcombine(input=iflatin)
for file in iflatlist:
    os.remove(file)

# check output flat image
print 'Check output file:'
iraf.imstatistics('iFlat')
print ' Running "imexamine" task..'
iraf.imexamine('iFlat', 1)

iraf.specred.extinction = ''
iraf.specred.caldir = ''
iraf.specred.observatory = 'lna'

print 'Create a response for dome flat...'
iraf.specred.response.interactive = True
iraf.specred.response(calibration='dFlat',
                      normalization='dFlat',
                      response='ndFlat')
# check output flat image
print 'Check output file:'
iraf.imstatistics('ndFlat')
print ' Running "imexamine" task..'
iraf.imexamine('ndFlat', 1)

print 'Create a response for internal flat...'
iraf.specred.response.interactive = True
iraf.specred.response(calibration='iFlat',
                      normalization='iFlat',
                      response='niFlat')
# check output flat image
print 'Check output file:'
iraf.imstatistics('niFlat')
print ' Running "imexamine" task..'
iraf.imexamine('niFlat', 1)


# Trim data if necessary
trimquery = True
trimsection = str(raw_input('Enter trim section, or hit <Enter>: '))
if trimsection == '':
    trimquery = False

# correct images
print 'Running Flat and Trimming correction...'
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
iraf.ccdred.ccdproc.zerocor = False
iraf.ccdred.ccdproc.flatcor = True
iraf.ccdred.ccdproc.trim = trimquery
iraf.ccdred.ccdproc.trimsec = trimsection
# science images
iraf.ccdred.ccdproc.flat = 'ndFlat'
iraf.ccdred.ccdproc(images=sciin)
# calibration images
iraf.ccdred.ccdproc.flat = 'niFlat'
iraf.ccdred.ccdproc(images=calin)

# extract aperture spectra for science images
print 'Extracting aperture spectra for science images ...'
iraf.specred.apall.readnoise = 'RDNOISE'
iraf.specred.apall.gain = 'GAIN'
iraf.specred.apall(input=sciin)

# extract aperture spectra for calibration images
print 'Extracting aperture spectra for calibration images ...'
iraf.specred.apall.readnoise = 'RDNOISE'
iraf.specred.apall.gain = 'GAIN'
iraf.specred.apall(input=calin)

print '--- DONE ---'

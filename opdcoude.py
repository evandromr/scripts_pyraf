#!/usr/bin/env python
#
# A script to reduce data from the Coude Spectrograph from the 1.6m telescope
# of the Observatorio do Pico dos Dias - Brazil
#
# Load Python standard modules
import glob
# Load third-party modules
import ds9
import astropy.io.fits as fits
from pyraf import iraf


print 'Loading IRAF packages ...'
iraf.imred()
iraf.ccdred()
iraf.onedspec()
iraf.twodspec()
iraf.apextract()

print 'unlearning previous settings...'
iraf.ccdred.ccdproc.unlearn()
iraf.ccdred.combine.unlearn()
iraf.ccdred.zerocombine.unlearn()
iraf.ccdred.flatcombine.unlearn()
iraf.apextract.unlearn()
iraf.apall.unlearn()
iraf.onedspec.identify.unlearn()
iraf.onedspec.dispcor.unlearn()
iraf.continuum.unlearn()

print 'openning a ds9 window if not already openned...'
ds9.ds9()

# regular expression of files (e.g bias_00*.fits, flat-2000jan01_?.*)
# if files in different folder, one can use the directory as part of the
# regular expresion e.g. /biasimages/bias_00??.fits
biasre = str(raw_input('\nEnter regular expression for Bias images: '))
flatsre = str(raw_input('Enter regular expression for Flat images: '))
sciencere = str(raw_input('Enter regular expression for Science images: '))
calre = str(raw_input('Enter regular expression for Calibration images: '))

# list of files that match that regular expression
biases = glob.glob(biasre)
flatses = glob.glob(flatsre)
sciences = glob.glob(sciencere)
calses = glob.glob(calre)

## Transforms python list in strings to be used by pyraf tasks
# bias
biasstring = ', '.join(biases)
# flat
flatsstring = ', '.join(flatses)
# science
sciencestring = ', '.join(sciences)
scienceprocstring = ', '.join([sc[:-5] + '_proc.fits' for sc in sciences])
scienceapalstring = ', '.join([sc[:-5] + '_proc.0001.fits' for sc in sciences])
sciencespecstring = ', '.join([sc[:-5] + '_spec.fits' for sc in sciences])
# calibration
calstring = ', '.join(calses)
calprocstring = ', '.join([cal[:-5] + '_proc.fits' for cal in calses])
calapalstring = ', '.join([cal[:-5] + '_proc.0001.fits' for cal in calses])

# combine bias images
print 'Combining Bias images...'
iraf.ccdred.ccdproc.unlearn()
iraf.ccdred.combine.unlearn()
iraf.ccdred.zerocombine.unlearn()
iraf.ccdred.zerocombine.output = 'Zero'
iraf.ccdred.zerocombine.combine = 'median'
iraf.ccdred.zerocombine.reject = 'sigclip'
iraf.ccdred.zerocombine.ccdtype = ''
iraf.ccdred.zerocombine.rdnoise = fits.getval(biases[0], 'RDNOISE')
iraf.ccdred.zerocombine.gain = fits.getval(biases[0], 'GAIN')
iraf.ccdred.zerocombine(input=biasstring)

# check output bias image
print 'Check output file:'
iraf.imstatistics('Zero')
print ' Running "imexamine" task..'
iraf.imexamine('Zero', 1)

# combine flat images
print 'Combining Flat images ...'
iraf.ccdred.ccdproc.unlearn()
iraf.ccdred.combine.unlearn()
iraf.ccdred.flatcombine.unlearn()
iraf.ccdred.flatcombine.output = 'Flat'
iraf.ccdred.flatcombine.combine = 'median'
iraf.ccdred.flatcombine.reject = 'sigclip'
iraf.ccdred.flatcombine.process = 'no'
iraf.ccdred.flatcombine.subsets = 'no'
iraf.ccdred.flatcombine.scale = 'mode'
iraf.ccdred.flatcombine.ccdtype = ''
iraf.ccdred.flatcombine.rdnoise = fits.getval(flatses[0], 'RDNOISE')
iraf.ccdred.flatcombine.gain = fits.getval(flatses[0], 'GAIN')
iraf.ccdred.flatcombine(input=flatsstring)

# check output flat image
print 'Check output file:'
iraf.imstatistics('Flat')
print ' Running "imexamine" task..'
iraf.imexamine('Flat', 1)

trimsection = str(raw_input('Enter trim section [col:umns,li:nes],\
 Or hit <Enter>: '))
if trimsection == '':
    trimsection = '[{0:d}:{1:d},{0:d}:{2:d}]'.format(
    1, fits.getval(sciences[0], 'NAXIS1'), fits.getval(sciences[0], 'NAXIS2'))

# correct images
print ''
print 'Running ccdproc task ...'
print ''
iraf.ccdred.ccdproc.unlearn()
iraf.ccdred.combine.unlearn()
iraf.ccdred.ccdproc.ccdtype = ''
iraf.ccdred.ccdproc.noproc = False
iraf.ccdred.ccdproc.fixpix = False
iraf.ccdred.ccdproc.overscan = False
iraf.ccdred.ccdproc.darkcor = False
iraf.ccdred.ccdproc.illumcor = False
iraf.ccdred.ccdproc.fringecor = False
iraf.ccdred.ccdproc.readcor = False
iraf.ccdred.ccdproc.scancor = False
iraf.ccdred.ccdproc.trim = True
iraf.ccdred.ccdproc.trimsec = trimsection
iraf.ccdred.ccdproc.readaxis = 'line'
iraf.ccdred.ccdproc.zerocor = True
iraf.ccdred.ccdproc.zero = 'Zero'
iraf.ccdred.ccdproc.flatcor = True
iraf.ccdred.ccdproc.flat = 'Flat'
iraf.ccdred.ccdproc.output = scienceprocstring
iraf.ccdred.ccdproc(images=sciencestring)
iraf.ccdred.ccdproc.output = calprocstring
iraf.ccdred.ccdproc(images=calstring)

# extract aperture spectra for science images
print 'Extracting aperture spectra for science images ...'
iraf.apextract.unlearn()
iraf.apall.unlearn()
iraf.apextract.dispaxis = 2
iraf.apall.format = 'onedspec'
iraf.apall.readnoise = fits.getval(sciences[0], 'RDNOISE')
iraf.apall.gain = fits.getval(sciences[0], 'GAIN')
iraf.apall(input=scienceprocstring)

# extract aperture spectra for calibration images
print 'Extracting aperture spectra for calibration images ...'
iraf.apextract.unlearn()
iraf.apall.unlearn()
iraf.apextract.dispaxis = 2
iraf.apall.format = 'onedspec'
iraf.apall.readnoise = fits.getval(calses[0], 'RDNOISE')
iraf.apall.gain = fits.getval(calses[0], 'GAIN')
iraf.apall(input=calprocstring)

print 'Combining spectras...'
iraf.ccdred.combine.unlearn()
iraf.ccdred.ccdproc.unlearn()
iraf.scombine.group = 'all'
iraf.scombine.combine = 'median'
iraf.scombine.reject = 'sigclip'
iraf.scombine.scale = 'exposure'
iraf.scombine.rdnoise = fits.getval(calses[0], 'RDNOISE')
iraf.scombine.gain = fits.getval(calses[0], 'GAIN')
iraf.scombine(input=calapalstring, output='calibration_spectra.fits')

print "The next step will ask you to identify lines in the calibration images"
raw_input("Press any key to continue:")

# make wavelengh solutions
linelist = str(raw_input('Enter name of iraf file with list \
                          of lines (linelists$thar.dat): '))
if linelist == '':
    linelist = 'linelists$thar.dat'
iraf.onedspec.identify.coordlist = linelist
iraf.onedspec.identify(images='calibration_spectra.fits')

print "Associating wavelenght with science spectra..."
iraf.hedit.unlearn()
iraf.dispcor.unlearn()
iraf.hedit.fields = 'REFSPEC1'
iraf.hedit.value = 'calibration_spectra'
iraf.hedit.add = True
iraf.hedit(images=scienceapalstring)

iraf.dispcor(input=scienceapalstring, output=sciencespecstring)

print '--- DONE ---'

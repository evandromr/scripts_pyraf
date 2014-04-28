#!/usr/bin/env python
#
# A script to reduce data from the Coude Spectrograph from the 1.6m telescope
# of the Observatorio do Pico dos Dias - Brazil
#
# Load Python standard modules
import glob
# Load third-party modules
import astropy.io.fits as fits
from pyraf import iraf


def checkfile(filename):
    '''Print statistics and open imexamine task for filename'''
    iraf.imstatistics.unlearn()
    iraf.imexamine.unlearn()
    print 'Check output file:'
    iraf.imstatistics(filename)
    print ' Running "imexamine" task..'
    iraf.imexamine(filename, 1)


def masterbias(biasre, combine='average', reject='minmax', out='Zero'):
    '''combine bias images

    ===
    Input:
        str: biasre - regular expression to bias files in the current directory
     --- Optional:
        str: combine - method to combine images (averate|median)
        str: reject - method to reject pixel values (minmax|sigclip|none|etc..)
        str: out - name of output master bias file

    Output:
        file: Zero.fits - combined zero-level images
    ===
    Examples:
        masterbias('bias*.fits')
        masterbias('zero_000?.fits', out='masterbias')
        masterbias('bias_*_new_*.fits', combine='median', reject='sigclip')
    '''

    biaslist = glob.glob(biasre)
    biasstring = ', '.join(biaslist)

    # load packages
    iraf.imred()
    iraf.ccdred()
    # unlearn settings
    iraf.imred.unlearn()
    iraf.ccdred.unlearn()
    iraf.ccdred.ccdproc.unlearn()
    iraf.ccdred.combine.unlearn()
    iraf.ccdred.zerocombine.unlearn()
    # setup task
    iraf.ccdred.ccdproc.instrument = 'coude'
    iraf.ccdred.zerocombine.output = out
    iraf.ccdred.zerocombine.combine = combine
    iraf.ccdred.zerocombine.reject = reject
    iraf.ccdred.zerocombine.ccdtype = ''
    iraf.ccdred.zerocombine.rdnoise = fits.getval(biaslist[0], 'RDNOISE')
    iraf.ccdred.zerocombine.gain = fits.getval(biaslist[0], 'GAIN')
    iraf.ccdred.zerocombine(input=biasstring)


def masterflat(flatre, combine='median', reject='sigclip', out='Flat',
               scale='mode'):
    '''combine flat images

    ===
    Input:
        str: flatre - regular expression to bias files in the current directory
     --- Optional:
        str: combine - method to combine images (averate|median)
        str: reject - method to reject pixel values (minmax|sigclip|none|etc..)
        str: out - name of output master flat file
        str: scale - mode to combine flat images (mode|average|exposure)

    Output:
        file: Flat.fits - combined flat field images
    ===
    Examples:
        masterbias('flat*.fits')
        masterbias('flatdome_000?.fits', out='masterflat')
        masterbias('flat_*_new_*.fits', combine='average', reject='minmax')
    '''

    flatlist = glob.glob(flatre)
    flatstring = ', '.join(flatlist)

    # load packages
    iraf.imred()
    iraf.ccdred()
    # unlearn settings
    iraf.imred.unlearn()
    iraf.ccdred.unlearn()
    iraf.ccdred.ccdproc.unlearn()
    iraf.ccdred.combine.unlearn()
    iraf.ccdred.flatcombine.unlearn()
    # setup task
    iraf.ccdred.ccdproc.instrument = 'coude'
    iraf.ccdred.flatcombine.output = out
    iraf.ccdred.flatcombine.combine = combine
    iraf.ccdred.flatcombine.reject = reject
    iraf.ccdred.flatcombine.ccdtype = ''
    iraf.ccdred.flatcombine.process = 'no'
    iraf.ccdred.flatcombine.subsets = 'no'
    iraf.ccdred.flatcombine.scale = scale
    iraf.ccdred.flatcombine.rdnoise = fits.getval(flatlist[0], 'RDNOISE')
    iraf.ccdred.flatcombine.gain = fits.getval(flatlist[0], 'GAIN')
    iraf.ccdred.flatcombine(input=flatstring)


def correctimages(imagesre, zero='Zero', flat='Flat'):
    '''Run ccdproc task to images'''
    iraf.imred()
    iraf.ccdred()

    imageslist = glob.glob(imagesre)
    imagesin = ', '.join(imageslist)
    imagesout = ', '.join([img[:-5]+'_proc.fits' for img in imageslist])

    trimsection = str(raw_input('Enter trim section (or Hit <Enter>): '))
    trimquery = True
    if trimsection == '':
        trimquery = False

    iraf.ccdred.ccdproc.unlearn()
    iraf.ccdred.combine.unlearn()
    iraf.ccdred.ccdproc.instrument = 'coude'

    iraf.ccdred.ccdproc.ccdtype = ''
    iraf.ccdred.ccdproc.noproc = False
    iraf.ccdred.ccdproc.fixpix = False
    iraf.ccdred.ccdproc.overscan = False
    iraf.ccdred.ccdproc.darkcor = False
    iraf.ccdred.ccdproc.illumcor = False
    iraf.ccdred.ccdproc.fringecor = False
    iraf.ccdred.ccdproc.readcor = False
    iraf.ccdred.ccdproc.scancor = False
    iraf.ccdred.ccdproc.trim = trimquery
    iraf.ccdred.ccdproc.trimsec = trimsection
    iraf.ccdred.ccdproc.readaxis = 'line'
    iraf.ccdred.ccdproc.zerocor = True
    iraf.ccdred.ccdproc.zero = zero
    iraf.ccdred.ccdproc.flatcor = True
    iraf.ccdred.ccdproc.flat = flat
    iraf.ccdred.ccdproc.output = imagesout
    iraf.ccdred.ccdproc(images=imagesin)


def specextract(imagesre):
    '''Extract aperture spectra for science images ...'''

    imageslist = glob.glob(imagesre)
    imagesin = ', '.join(imageslist)
    imagesout = ', '.join([img[:-5]+'_ap.fits' for img in imageslist])

    iraf.onedspec()
    iraf.twodspec()
    iraf.apextract()

    iraf.apextract.unlearn()
    iraf.apall.unlearn()

    iraf.apextract.dispaxis = 2

    iraf.apall.format = 'onedspec'
    iraf.apall.readnoise = fits.getval(imageslist[0], 'RDNOISE')
    iraf.apall.gain = fits.getval(imageslist[0], 'GAIN')
    iraf.apall(input=imagesin)

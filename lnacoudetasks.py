#!/usr/bin/env python
#
# A script with tasks to reduce data from the Coude Spectrograph
# at the 1.6m telescope of the Observatorio do Pico dos Dias - Brazil

# Load Python standard modules
import glob
# Load third-party modules
from pyraf import iraf


def checkfile(filename):
    '''Print statistics and run open imexamine task'''

    iraf.imstatistics.unlearn()
    iraf.imexamine.unlearn()
    print 'Check output file:'
    iraf.imstatistics(filename)
    print ' Running "imexamine" task..'
    iraf.imexamine(filename, 1)


def masterbias(biasre, output='Zero', combine='median', reject='minmax',
        ccdtype='', rdnoise='rdnoise', gain='gain'):
    '''run the task ccdred.zerocombine with chosen parameters

    Input:
    -------
     str biasre: regular expression to identify zero level images

    Output:
    -------
     file Zero.fits: combined zerolevel images
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
    iraf.ccdred.setinstrument.unlearn()
    # setup task
    iraf.ccdred.zerocombine.output = output
    iraf.ccdred.zerocombine.combine = combine
    iraf.ccdred.zerocombine.reject = reject
    iraf.ccdred.zerocombine.ccdtype = ccdtype
    iraf.ccdred.zerocombine.rdnoise = rdnoise
    iraf.ccdred.zerocombine.gain = gain
    # run task
    iraf.ccdred.zerocombine(input=biasstring)


def masterflat(flatre, output='Flat', combine='median', reject='sigclip',
               scale='mode', rdnoise='rdnoise', gain='gain'):
    '''combine flat images with the task ccdred.flatcombine

    Input:
    -------
     str: flatre - regular expression to bias files in the current directory

    Output:
    -------
     file: Flat.fits - combined flat field images
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
    iraf.ccdred.setinstrument.unlearn()
    # setup task
    iraf.ccdred.flatcombine.output = output
    iraf.ccdred.flatcombine.combine = combine
    iraf.ccdred.flatcombine.reject = reject
    iraf.ccdred.flatcombine.ccdtype = ''
    iraf.ccdred.flatcombine.process = 'no'
    iraf.ccdred.flatcombine.subsets = 'yes'
    iraf.ccdred.flatcombine.scale = scale
    iraf.ccdred.flatcombine.rdnoise = rdnoise
    iraf.ccdred.flatcombine.gain = gain
    iraf.ccdred.flatcombine(input=flatstring)


def subzero(imagesre, zero='Zero'):
    '''Run ccdproc remove Zero level noise'''

    imageslist = glob.glob(imagesre)
    imagesin = ', '.join(imageslist)

    # Load packages
    iraf.imred()
    iraf.ccdred()
    # Unlearn previouse settings
    iraf.ccdred.ccdproc.unlearn()
    iraf.ccdred.combine.unlearn()
    # setup and run task
    iraf.ccdred.ccdproc.ccdtype = ''
    iraf.ccdred.ccdproc.noproc = False
    iraf.ccdred.ccdproc.fixpix = False
    iraf.ccdred.ccdproc.overscan = False
    iraf.ccdred.ccdproc.darkcor = False
    iraf.ccdred.ccdproc.illumcor = False
    iraf.ccdred.ccdproc.fringecor = False
    iraf.ccdred.ccdproc.readcor = False
    iraf.ccdred.ccdproc.scancor = False
    iraf.ccdred.ccdproc.trim = False
    iraf.ccdred.ccdproc.trimsec = ''
    iraf.ccdred.ccdproc.readaxis = 'line'
    iraf.ccdred.ccdproc.zerocor = True
    iraf.ccdred.ccdproc.zero = zero
    iraf.ccdred.ccdproc.flatcor = False
    iraf.ccdred.ccdproc.flat = ''
    iraf.ccdred.ccdproc(images=imagesin)


def divflat(imagesre, flat='Flat'):
    '''Run ccdproc task to images'''

    imageslist = glob.glob(imagesre)
    imagesin = ', '.join(imageslist)

    # Load packages
    iraf.imred()
    iraf.ccdred()
    # Unlearn settings
    iraf.ccdred.ccdproc.unlearn()
    iraf.ccdred.combine.unlearn()
    # Setup and run task
    iraf.ccdred.ccdproc.ccdtype = ''
    iraf.ccdred.ccdproc.noproc = False
    iraf.ccdred.ccdproc.fixpix = False
    iraf.ccdred.ccdproc.overscan = False
    iraf.ccdred.ccdproc.darkcor = False
    iraf.ccdred.ccdproc.illumcor = False
    iraf.ccdred.ccdproc.fringecor = False
    iraf.ccdred.ccdproc.readcor = False
    iraf.ccdred.ccdproc.scancor = False
    iraf.ccdred.ccdproc.trim = False
    iraf.ccdred.ccdproc.trimsec = ''
    iraf.ccdred.ccdproc.readaxis = 'line'
    iraf.ccdred.ccdproc.zerocor = False
    iraf.ccdred.ccdproc.zero = ''
    iraf.ccdred.ccdproc.flatcor = True
    iraf.ccdred.ccdproc.flat = flat
    iraf.ccdred.ccdproc(images=imagesin)


def correctimages(imagesre, zero='Zero', flat='nFlat'):
    '''Run ccdproc task to correct images'''

    imageslist = glob.glob(imagesre)
    imagesin = ', '.join(imageslist)

    trimsection = str(raw_input('Enter trim section (or Hit <Enter>): '))
    trimquery = True
    if trimsection == '':
        trimquery = False

    # Load Packages
    iraf.imred()
    iraf.ccdred()
    # Unlearn Settings
    iraf.ccdred.ccdproc.unlearn()
    iraf.ccdred.combine.unlearn()
    # Setup and run task
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
    iraf.ccdred.ccdproc(images=imagesin)


def runapall(imagesre, gain='gain', rdnoise='rdnoise'):
    '''Extract aperture spectra for science images ...'''

    imageslist = glob.glob(imagesre)
    imagesin = ', '.join(imageslist)

    # load packages
    iraf.imred()
    iraf.ccdred()
    iraf.specred()
    # unlearn previous settings
    iraf.ccdred.combine.unlearn()
    iraf.ccdred.ccdproc.unlearn()
    iraf.specred.apall.unlearn()
    # setup and run task
    iraf.specred.apall.format = 'onedspec'
    iraf.specred.apall.readnoise = rdnoise
    iraf.specred.apall.gain = gain
    iraf.specred.apall(input=imagesin)


def flatresponse(input='Flat', output='nFlat'):
    ''' normalize Flat to correct illumination patterns'''

    iraf.imred()
    iraf.ccdred()
    iraf.specred()

    iraf.ccdred.combine.unlearn()
    iraf.ccdred.ccdproc.unlearn()
    iraf.specred.response.unlearn()
    iraf.specred.response.interactive = True
    iraf.specred.response.function = 'chebyshev'
    iraf.specred.response.order = 1
    iraf.specred.response(calibration=input, normalization=input,
            response=output)


def flatresponse2(input='Flat_zero', output='nFlat'):
    ''' normalize Flat to correct illumination patterns'''

    iraf.boxcar(input, 'Flatboxcar', 10, 10)
    iraf.imarith(input, '/', 'Flatboxcar', output)


def scalewavelenght(calspec):
    ''' Creates a wavelenght solution for 'calspec' '''
    iraf.imred()
    iraf.specred()

    linelist = str(raw_input('Enter file with list of lines (linelists$thar.dat) : '))
    if linelist == '':
        linelist = 'linelists$thar.dat'
    iraf.specred.identify.coordlist = linelist
    iraf.specred.identify(images=calspec)


def applywavesolution(inputre, calspec):
    ''' apply calibration solution to science spectra '''

    inputlist = glob.glob(inputre)
    inputstring = ', '.join(inputlist)
    outputstring = ', '.join([inp[:-5]+'_spec.fits' for inp in inputlist])

    iraf.hedit.unlearn()
    iraf.dispcor.unlearn()

    iraf.hedit.fields = 'REFSPEC1'
    iraf.hedit.value = calspec
    iraf.hedit.add = True
    iraf.hedit(images=inputstring)

    iraf.dispcor(input=inputstring, output=outputstring)


def combinespecs(inputre, scale='exposure', rdnoise='rdnoise', gain='gain'):
    ''' combine two or more spectra tha matches the input regular expression
    '''

    specfiles = glob.glob(specre)
    specstring = ', '.join(specfiles)

    print 'The following spectra will be combined: '
    print specfiles

    specout = str(raw_input('Enter output file name: '))

    iraf.scombine.unlearn()
    iraf.scombine.scale = scale
    iraf.scombine.rdnoise = rdnoise
    iraf.scombine.gain = gain

    iraf.scombine(input=specstring, output=specout)

    ask = str(raw_input('Plot output with splot? Y/N: '))
    if (ask == 'y') or (ask == 'Y'):
        iraf.splot.unlearn()
        iraf.splot(specout)

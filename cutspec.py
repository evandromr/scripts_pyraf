#!/usr/bin/env python
#
# A script to trim images
#
# Load Python standard modules
import glob
# Load third-party modules
from pyraf import iraf

iraf.imred()
iraf.ccdred()

imagesre = str(raw_input("Enter regular expression to images: "))
imageslist = glob.glob(imagesre)
imagesin = ', '.join(imageslist)
imagesout = ', '.join([img[:-5]+'_trimed.fits' for img in imageslist])

trimsection = str(raw_input('Enter trim section: '))

iraf.ccdred.ccdproc.unlearn()
iraf.ccdred.combine.unlearn()

iraf.ccdred.setinstrument.unlearn()
iraf.ccdred.setinstrument.review = False                                        
iraf.ccdred.setinstrument(instrument='coude')

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
iraf.ccdred.ccdproc.flatcor = False
iraf.ccdred.ccdproc.trim = True
iraf.ccdred.ccdproc.trimsec = trimsection
iraf.ccdred.ccdproc.output = imagesout
iraf.ccdred.ccdproc(images=imagesin)

print '--- DONE ---'

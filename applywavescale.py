#!/usr/bin/env python
#
# Associate wavelenght solution to science spectra
#
import glob
from pyraf import iraf

calspec = str(raw_input("Enter calibrated spectra: "))

inputre = str(raw_input("Enter regular expression for science spectra: "))
inputlist = glob.glob(inputre)
inputstring = ', '.join(inputlist)
outputstring = ', '.join([input[:-5]+'_spec.fits' for input in inputlist])

iraf.hedit.unlearn()
iraf.dispcor.unlearn()
iraf.hedit.fields = 'REFSPEC1'
iraf.hedit.value = calspec
iraf.hedit.add = True
iraf.hedit(images=inputstring)

iraf.dispcor(input=inputstring, output=outputstring)

print '--- DONE ---'

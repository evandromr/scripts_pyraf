#!/usr/bin/env python
#
# Associate wavelenght solution to science spectra
#
import glob
from pyraf import iraf

calspec = str(raw_input("Enter calibrated spectra: "))

inputre = str(raw_input("Enter regular expression for science spectra: "))
inputlist = glob.glob(inputre)

iraf.hedit.unlearn()
iraf.dispcor.unlearn()
iraf.hedit.fields = 'REFSPEC1'
iraf.hedit.value = calspec
iraf.hedit.add = True
for img in inputlist:
    iraf.hedit(images=img)
    iraf.dispcor(input=img, output=img[:-5]+'_spec')

print '--- DONE ---'

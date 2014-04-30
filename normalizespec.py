#!/usr/bin/env python
#
# Try to normalize spectra
#
from pyraf import iraf

iraf.continuum.unlearn()

spec = str(raw_input("Enter spectra to normalize: "))
out = str(raw_input("Enter name of ouput normalized spectra: "))

iraf.continuum.function = 'spline3'
iraf.continuum.order = 1
iraf.continuum.low_reject = 2.0
iraf.continuum.high_reject = 4.0
iraf.continuum(input=spec, output=out)

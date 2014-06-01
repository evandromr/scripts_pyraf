#!/usr/bin/env python
#
# Plot a wavelengh calibrated IRAF spectrum using matplotlib
#
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import numpy as np


input = str(raw_input('Enter spectra: '))

s = fits.open(input)

linit = float(s[0].header['CRVAL1'])
dell = float(s[0].header['CDELT1'])
numpix = float(s[0].header['NAXIS1'])

lfim = linit + numpix*dell

wave = np.arange(linit, lfim, dell)
data = s[0].data

plt.plot(wave, data)
plt.xlim(6150, 6750)
plt.ylim(0.8, 1.4)
plt.xlabel('Wavelenght [$\AA$]')
plt.ylabel('Relative Intensity')
plt.title(input)
plt.show()

plt.plot(wave, data)
plt.xlim(6150, 6750)
plt.ylim(0.8, 1.4)
plt.xlabel('Wavelenght [$\AA$]')
plt.ylabel('Relative Intensity')
plt.title(input)
plt.savefig('spectra.png')

from pyraf import iraf
from ds9 import ds9
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import glob

science = str(raw_input('Science images: '))
cal = str(raw_input('Calibration images: '))

sciimages = glob.glob(science)

flatcup = str(raw_input('Flat cupula: '))
flati = str(raw_input('Flat interno: '))

bias = str(raw_input('Zero level: '))
linelist = str(raw_input('Lista de linhas (linelists$thar.dat): '))

iraf.imred()
iraf.ccdred()
iraf.specred()
ds9()

iraf.zerocombine.unlearn()
iraf.zerocombine(input=bias, reject='avsigclip', ccdtype='',
                 rdnoise='rdnoise', gain='gain')

iraf.imstat('bias*')
iraf.imstat('Zero')

iraf.imexamine('Zero')

iraf.flatcombine.unlearn()
iraf.flatcombine(input=flatcup, output='Flat', ccdtype='', process=False,
                 subsets=False, rdnoise='rdnoise', gain='gain')

iraf.flatcombine(input=flati, output='iFlat', ccdtype='', process=False,
                 subsets=False, rdnoise='rdnoise', gain='gain')

iraf.imstat(flatcup)
iraf.imstat('Flat')

iraf.imstat(flati)
iraf.imstat('iFlat')

iraf.imexamine('Flat')
iraf.imexamine('iFlat')

iraf.response.unlearn()
iraf.response(calibration='Flat', normalization='Flat', response='nFlat',
              function='legendre', order='1')

iraf.response.unlearn()
iraf.response(calibration='iFlat', normalization='iFlat', response='niFlat',
              function='legendre', order='1')

iraf.imstat('nFlat')
iraf.imexamine('nFlat')

iraf.imstat('niFlat')
iraf.imexamine('niFlat')

iraf.ccdproc.unlearn()
iraf.ccdproc(images=science, ccdtype='', fixpix=False, overscan=False,
        darkcor=False, trim=True, zerocor=True, flatcor=True,
        trimsec='[*,20:4600]', zero='Zero', flat='nFlat')

iraf.ccdproc(images=cal, ccdtype='', fixpix=False, overscan=False,
        darkcor=False, trim=True, zerocor=True, flatcor=True,
        trimsec='[*,20:4600]', zero='Zero', flat='niFlat')

iraf.ccdlist('Zero, nFlat, niFlat, {0}, {1}'.format(science, cal))

iraf.imstat('Zero')
iraf.imstat('nFlat')
iraf.imstat(science)
iraf.imstat(cal)

ref = str(raw_input('Imagen de referencia (eg. hd161103_0001.fits):'))

iraf.imexamine(ref)

iraf.apall.unlearn()
iraf.apall(input=science, format='onedspec', readnoise='rdnoise',
        gain='gain')

iraf.apall(input=cal, format='onedspec', reference=ref,
        readnoise='rdnoise', gain='gain')

iraf.identify(images=cal[:-5]+'*.0001.fits', coordlist=linelist)

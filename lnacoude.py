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
import lnacoudetasks as coude


# regular expression of files (e.g bias_00*.fits, flat-2000jan01_?.*)
zerore = str(raw_input('\nEnter regex for zero level images: '))
flatre = str(raw_input('Enter regex for science flat images: '))
scire = str(raw_input('Enter regex for science images: '))
calre = str(raw_input('Enter regex for calibration images: '))
fcalre = str(raw_input('Enter regex for calibration flat images: '))

# list of files that match that regular expression
zerolist = glob.glob(zerore)
flatlist = glob.glob(flatre)
scilist = glob.glob(scire)
callist = glob.glob(calre)
fcallist = glob.glob(fcalre)

print 'creating a proc/ dir to store processed data'
if not os.path.isdir('proc'):
    os.mkdir('proc')

allfiles = zerolist + flatlist + scilist + callist + fcallist
for file in allfiles:
    shutil.copy(file, 'proc/')
os.chdir('proc')

print 'openning a ds9 window if not already openned...'
ds9.ds9()

# combine bias images
print 'Combining Bias images...'
coude.masterbias(zerore)
for zerofile in zerolist:
    os.remove(zerofile)

# check output bias image
coude.checkfile('Zero')

# combine flat images
print 'Combining flat images ...'
coude.masterflat(flatre)
for flatfile in flatlist:
    os.remove(flatfile)
# check output
coude.checkfile('Flat')

coude.masterflat(fcalre, output = 'cFlat')
for fcalfile in fcallist:
    os.remove(fcalfile)
coude.checkfile('cFlat')

# response
# coude.subzero('Flat')
coude.flatresponse('Flat')
coude.flatresponse('cFlat', 'ncFlat')
# check output
coude.checkfile('nFlat')
coude.checkfile('ncFlat')

# correct
coude.correctimages(scire, flat='nFlat')
coude.correctimages(calre, flat='ncFlat')
# extract
coude.runapall(scire)
coude.runapall(calre)

print '--- DONE ---'

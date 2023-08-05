#! usr/bin/env python3

from astropy.io import fits 
import sys 
import numpy as np
from astride import Streak
import spiceypy as spice
from sgp4.earth_gravity import wgs72
import datetime
import json


class utils:
	
	def split(filename):
		# Opening fits file
		file = filename
		hdu = fits.open(filename)

		# Header extraction
		hdr = hdu[0].header

		# Extraction of the data format
		data = hdu[0].data
		data_array = np.array(data)
		ndata = len(data_array)
	
		# Creation of the images 
		for i in range(ndata):
			hdul = fits.PrimaryHDU(data_array[i],hdr)
			new_hdul = fits.HDUList(hdul)
			imagename = 'image'+str(i+1)+'.fits'
			new_hdul.writeto(imagename, overwrite=True)



	def streak_detection(filename,outputfilename):
		# Creating and executing a streak instance
		streak = Streak(filename)
		streak.detect()
		streak.streaks
		streak.write_outputs()
		streak.plot_figures()
		file = open(outputfilename, 'w+')
		file.write(str(streak.streaks))
		file.close()



	def header_change(filename,keywords,values):
		# Check on match of dimension between keywords and values 
		nkey = len(keywords)
		nval = len(values)
		if nkey != nval:
			print('Keywords number not equal to values number! Please check list lengths.')
			return 
		else: 	
			# Update of the header values
			with fits.open(filename, mode='update') as hdul: 
					for i in range(nkey):
						hdul[0].header.set(keywords[i],values[i])
					hdul.flush()
			print('Header updated')
			return


# All the credit for the following function goes to Professor Mauro Massari (mauro.massari@polimi.it)
	def createTLEKernel(filename,kernelname,lsk):
	    
	    spice.furnsh(lsk)
	    # load TLEs freom .3le file 
	    tle = open(filename,'r').read().splitlines()
	    
	    # remove empty line (typically at the end)
	    while '' in tle:
	        tle.remove('')
	    
	    #check if it is a 3le of tle file
	    is3le = False
	    
	    if tle[0][0] == '0':
	        is3le = True
	            
	    if is3le:
	        numlines=3
	    else:
	        numlines=2

	    # compute how many objects are in the file
	    numobj = len(tle)//numlines
	    
	    #create kernel file
	    handle = spice.spkopn(kernelname,'SPK_file',100)
	    center = 399
	    inframe = 'J2000'
	    yearsvalid = 1
	    const = np.array([wgs72.j2, wgs72.j3, wgs72.j4, wgs72.xke, 120.0, 78.0, wgs72.radiusearthkm, 1])
	    epochs = np.array([0.0])

	    
	    for i in range(numobj):
	        if is3le:
	            id=-1*(int(tle[i*numlines+1][2:7])+100000)
	            [epochs[0],elem] = spice.getelm(2000,len(tle[i*numlines+1])+1,tle[i*numlines+1:i*numlines+numlines])
	            spice.spkw10(handle,id,center,inframe,epochs[0],epochs[0]+yearsvalid*365.25*86400,tle[i*numlines][2:],const,1,elem,epochs)
	            
	        else:
	            id=-1*(int(tle[i*numlines+1][2:7])+100000)
	            [epochs[0],elem] = spice.getelm(2000,len(tle[i*numlines])+1,tle[i*numlines:i*numlines+numlines])
	            spice.spkw10(handle,id,center,inframe,epochs[0],epochs[0]+yearsvalid*365.25*86400,tle[i*numlines+1][2:7],const,1,elem,epochs)
	            
	    
	    spice.spkcls(handle)        
	    spice.unload(lsk)


	def fix_RADEC(filename):
		hdul = fits.open(filename)
		ra = hdul[0].header['OBJCTRA']
		dec = hdul[0].header['OBJCTDEC']
		ra = ra.strip().replace(' ',':')
		dec = dec.strip().replace(' ',':')
		hdul[0].header.set('OBJCTRA',ra)
		hdul[0].header.set('OBJCTDEC',dec)
		hdul.writeto(filename, overwrite=True)


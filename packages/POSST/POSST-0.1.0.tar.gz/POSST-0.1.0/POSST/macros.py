#! usr/bin/env python3

import Poliscope
import spiceypy as spice
import spiceypy.utils.support_types as stypes
import datetime
import numpy as np
import json

from sgp4.earth_gravity import wgs72





class Preparation: 

	def Research(ID,tle,kernel,timewin,stpsz):
		# Check on timewin dimension: 
		while len(timewin) != 2: 
			print('Time window format not correct! please insert times in the following format : YYYY MON DD HR:MN:SC.###')
			timewin = np.array([0,0])
			timewin[0] = input('Time window start time: ')
			timewin[1] = input('Time window end time  : ')
		lsk = './Kernel/naif0012.tls'
		Poliscope.utils.createTLEKernel(tle,kernel,lsk)

		# Kernel loading 
		METAKR = './Kernel/metakr.txt'
		spice.furnsh(METAKR)
		spice.furnsh(kernel)

		# Time conversion to ET 
		start_time = spice.str2et(timewin[0])
		end_time = spice.str2et(timewin[1])

		# Creation of research window 
		cnfine = stypes.SPICEDOUBLE_CELL(2)
		spice.wninsd(start_time,end_time,cnfine)
		MAXIVL = 1000
		MAXWIN = 2*MAXIVL
		riswin = stypes.SPICEDOUBLE_CELL(MAXWIN)

		# Parameters to initialize the research 
		target = str(ID)
		obsfrm = 'POLIMI_TOPO'
		obs = '399999'
		abcorr = 'none'
		crdsys = 'LATITUDINAL'
		coord = 'LATITUDE'
		relate = '>'
		refval = 10*spice.rpd()
		adjust = 0.0


		# Research in the time window selected
		spice.gfposc(target, obsfrm, abcorr, obs, 
					crdsys, coord, relate, refval, 
					adjust, stpsz, MAXIVL, cnfine, riswin)
		spice.unload(METAKR)
		spice.unload(kernel)
		return riswin

	def Results(riswin, kernel, ID):
		TDBFMT = 'YYYY MON DD HR:MN:SC.### (UTC) ::UTC'
		# Loading of kernels needed for the analysis
		METAKR = './Kernel/metakr.txt'
		spice.furnsh(METAKR)
		spice.furnsh(kernel)

		# Result output and storage 
		winsiz = spice.wncard(riswin)
		if winsiz == 0: 
			print('No sightings found')
			return
		else:
			timevec = np.zeros((winsiz, 2))
			j = 0
			for i in range(winsiz):
				[timbeg, timend] = spice.wnfetd(riswin, i)
				timestr = spice.timout(timbeg, TDBFMT)
				tim = datetime.datetime.strptime(timestr[12:16],'%H:%M')
				mor = datetime.datetime.strptime('06:00','%H:%M')
				nig = datetime.datetime.strptime('22:00','%H:%M')
				isNight =  mor.time() > tim.time()
				if isNight:
					if i == 0:
						print('Visibility or window start time: ')
						print(' {:s}'.format(timestr))
					else:
						print('Visibility start time: ')
						print('{:s}'.format(timestr))

						timestr = spice.timout(timend, TDBFMT)
					if i == (winsiz-1):
						print('Visibility or window stop time: ')
						print(' {:s}'.format(timestr))
					else:
						print('Visibility stop time: ')
						print('{:s}'.format(timestr))

					# Extraction of times
					timevec[i] = [timbeg, timend]
					j = j+1

			timevec = timevec[timevec != [0,0]].reshape((j,2))
			return timevec


	def Selection(ID,timevec,kernel):
		TDBFMT = 'YYYY MON DD HR:MN:SC.### (UTC) ::UTC'
		# Loading of kernels needed for the analysis
		METAKR = './Kernel/metakr.txt'
		spice.furnsh(METAKR)
		spice.furnsh(kernel)


		ref = 'POLIMI_TOPO'
		abcorr = 'none'
		obs = 399999

		# Prompt the user to choose the obervation in which to evaluate RA and DEC for the selected object 
		time_needed = input('Input the wanted time in the format of display: ')
		i = 0
		time_token = timevec[i][0]
		time_token = spice.et2utc(time_token, 'C', 4, 25)
		while time_token != time_needed:
			i = i+1
			time_token = timevec[i][0]
			time_token = spice.et2utc(time_token, 'C', 4, 25)

		startim = timevec[i][0]
		endtim = timevec[i][1]

		step = 1

		time = startim
		window = []
		window.append(time)
		delta = endtim - time

		while delta > 0:
			time = time+1
			window.append(time)
			delta = endtim - time


		RA = np.zeros(len(window))
		DEC = RA

		for j in range(len(window)):
			[pos, lt] = spice.spkezp(int(ID), window[j], ref, abcorr, obs)
			[ran, ra, dec] = spice.recrad(pos)
			RA[j] = ra*spice.rpd()
			DEC[j] = dec*spice.rpd()

		spice.unload(METAKR)
		spice.unload(kernel)

		return RA, DEC, startim, endtim




	def Output(ID,start,RA,DEC,end,exptim):
		n = len(ID)
		data = {}
		data['Object'] = []
		for i in range(n):
			data['Object'].append({
				'ID':ID[i],
				'Start time': start[i],
				'RA': RA[i],
				'DEC': DEC[i],
				'End time': end[i],
				'Exposure': exptim[i]})

		with open('Data.txt','w') as outfile:
			json.dump(data,outfile)
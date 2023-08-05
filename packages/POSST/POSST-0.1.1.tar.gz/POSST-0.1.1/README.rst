======
POSST
======

The POSST module provides the necessary files in order to correctly operate and communicate with the POSST telescope. In the module various operations are possible, from sidereal to debris tracking. Some of these functions may be used independently in order to perform some photometry (or similar image processing), but the whole package is designed to be used together with the POSST telescope and scheduler. 

Currently the sub-modules present in the POSST module are: 


utils 
=====

Which is composed by functions that act on: 

* FITS files :

	* split: splits multiple FITS into single ones

	* header_change: changes values into the FITS header according to passed parameters

	* fix_RADEC: formats RA and DEC values in the FITS header so that photometry pipeline is able to read them

* SPICE kernel generation: 

	* createTLEKernel: generates a spk kernel in SPICE starting from a TLE or 3LE

* Image processing: 

	* streak_detection: generates an ASTRiDE instance that analyses and outputs all the detected streaks in the FITS file


Preparation
======

Functions in this sub-module are: 

* Preparation: 

	* Research: performs a visibility research in the time window selected for the object given in input

	* Results: prints out Research results 

	* Selection: allows to choose which time window to analyze in detail for telescope scheduling 

	* Output: outputs a json file with the information needed by the scheduler



modes 
=====

In this module the most common functions are used; the macros for the various modes are defined

1. Slew: creates the necessary instructions to perform a slew at the indicated rate (optional) to the desired position

2. Tracking: tracks the desired object at the desired time - possible closed loop control in future

3. Sidereal tracking: standard sidereal tracking observation 



image processing
================

TBD

"""
Selection of functions dealing with time-tag data in FITS format

"""

from astroraf.misc import progress_bar
import pyfits
import os
import numpy as np

#-------------------------------------------------------------------------------

def ttag_image(in_data, xtype='XCORR', ytype='YCORR', pha=(2, 30), 
               bins=(1024, 16384), times=None, ranges=((0, 1023), (0, 16384)),
               binning=(1, 1), NUV=False):
    """ 
    Bin an events list (*_rawtag_*.fits, *_corrtag_*.fits) into an image.
    
    Events can be filtered out by time, PHA, and/or X and Y ranges
    
    """
    
    from numpy import histogram2d, where, zeros

    if isinstance( in_data, str ):
        hdu = pyfits.open( in_data )
    else:
        hdu = in_data

    events = hdu['events'].data

    if NUV:
        bins = (1024, 1024)
        pha = (-1, 1)
        ranges = ( (0, 1023), (0, 1023) )

    if times:
        index = where( (events['TIME'] >= times[0]) & 
                       (events['TIME'] <= times[1]) )
        events =  events[index]

    index = where( (events['PHA'] >= pha[0]) & 
                   (events['PHA'] <= pha[1]) )

    if len(index[0]):
        image = histogram2d( events[ytype][index], 
                             events[xtype][index], 
                             bins=bins, range=ranges)[0]
    else:
        image = zeros( (bins[0]//binning[0], bins[1]//binning[1]) )

    return image



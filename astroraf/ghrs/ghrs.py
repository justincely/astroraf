"""
Functions for dealing with GHRS data

"""

import glob
from astropy.io import fits as pyfits
import numpy as np

from astroraf.spectra.spectools import cross_correlate

from pyraf import iraf
from iraf import stsdas, hst_calib, ctools

class assemble:
    """
    Assemble GHRS fits files into a single MEF file

    """

    def __init__(self, rootname):
        
        rootname = rootname[:9]

        if not self._files_available( rootname ):
            raise IOError('Missing files')

        self.outname = rootname + '_x1d.fits'
        
        self.hdu = pyfits.open( rootname + '_c0f.fits' )

        self.wavelength_file = rootname + '_c0f.fits'
        self.flux_file = rootname + '_c1f.fits'
        self.error_file = rootname + '_c2f.fits'
        self.background_file = rootname + '_c5f.fits'
        self.dq_file = rootname + '_cqf.fits'

        self.wavelength = self._get_data( self.wavelength_file )
        self.flux = self._get_data( self.flux_file )
        self.error = self._get_data( self.error_file )
        self.background = self._get_data( self.background_file )
        self.dq = self._get_data( self.dq_file )

        #self._align()

        #self._merge()

        #self._monotonize_all()


    def _files_available(self, rootname):
        """Check that all necessary files exist
        """

        all_files = glob.glob( rootname + '*.fits' )
                
        found_endings = set( [item[-8:-5] for item in all_files] )

        needed_endings = set( ['c0f', 'c1f', 'c2f', 'c3f',
                               'c4f', 'c5f'] )
        
        return needed_endings.issubset( found_endings )


    def _get_data(self, filename):
        """Grab the data from the given file
        """

        return np.array( [ array for array in pyfits.open( filename )[0].data ] )


    def _align(self, window=None):
        """ Cross-correlate each FP-SPLIT by the 1st

        Wavelengths are updated in place.

        """

        ref_wave = self.wavelength[0]
        ref_flux = self.flux[0]

	if not window:
            window = (ref_wave.min(), ref_wave.max())

        for i, (wave, flux) in enumerate( zip( self.wavelength[1:], self.flux[1:] ) ):
            shift = cross_correlate(ref_flux, flux, ref_wave, wave, window=window)
            print shift
            self.wavelength[i] -= shift

    def _monotonize_all(self):
        """ Make sure all arrays are monotonically increasing with 
        wavelength.

        """

        sorted_index = np.argsort( self.wavelength )
        
        self.wavelength = self.wavelength[ sorted_index ]
        self.flux = self.flux[ sorted_index ]
        self.error = self.error[ sorted_index ]
        self.background = self.background[ sorted_index ]
        self.dq = self.dq[ sorted_index ]


    def _merge(self):
        """This is not very good and should be modified as soon as this
        data is actually needed


        """

        all_wavelengths = list(set(self.wavelength.ravel()))
        
        new_wavelength = []
        new_flux = []
        new_error = []
        new_background = []
        new_dq = []

        for w in all_wavelengths:
            index = np.where( self.wavelength == w )[0]

            new_wavelength.append( w )
            new_flux.append( np.mean( self.flux[index] ) )
            new_error.append( np.mean( self.error[index] ) )
            new_background.append( np.mean( self.background[index] ) )
            
            new_dq.append( self._bool_or( self.dq[index] ) )

        self.wavelength = np.array( new_wavelength )
        self.flux = np.array( new_flux )
        self.error = np.array( new_error )
        self.background = np.array( new_background )
        self.dq = np.zeros(self.flux.shape)
        #self.dq = np.array( new_dq )


    def _bool_or(self, bool_values):
        out_bool = 0
        
        for item in bool_values:
            out_bool = out_bool | item

        return out_bool
        

    def write(self, outname=None, clobber=False):
        """ Write out to FITS file
        """

        if isinstance( outname, str ):
            self.outname = outname

        hdu_out = pyfits.HDUList(pyfits.PrimaryHDU())

        keyword_list = ['INSTRUME', 'DETECTOR', 'GRATING', 'APERTURE',
                        'ROOTNAME', 'TARGNAME', 
                        'RA_TARG', 'DEC_TARG', 'DATE-OBS', 'TIME-OBS',
                        'EXPSTART', 'EXPEND', 'EXPTIME', 'OBSMODE', 
                        'PROPOSID', 'FP_SPLIT']

        for kw in keyword_list:
            hdu_out[0].header[kw] = self.hdu[0].header[kw]
 
        array_size = len(self.wavelength[0])

        dims = '{}D'.format(array_size)
        wavelength_col = pyfits.Column('wavelength', dims, 'second', array=self.wavelength)
        flux_col = pyfits.Column('flux', dims, 'ergs/s', array=self.flux)
        error_col = pyfits.Column('error', dims, 'counts', array=self.error)
        bkgnd_col = pyfits.Column('background', dims, 'cnts', array=self.background)
        dq_col = pyfits.Column('dq', dims, 'cnts', array=self.dq)

        tab = pyfits.new_table([wavelength_col, 
                               flux_col,
                               error_col,
                               bkgnd_col, 
                               dq_col], nrows=len(self.wavelength))

        hdu_out.append(tab)
        #hdu_out[1].header['NELEM'] = array_size

        hdu_out.writeto(self.outname, clobber=clobber)  

        iraf.splice(self.outname, 
                    self.outname.replace('x1d', 'x1dsum'), 
                    sdqflags=16, 
                    wl_name='wavelength', 
                    flux_name='flux', 
                    sw_name='',
                    wgt_name='', 
                    spacing='coarse')
